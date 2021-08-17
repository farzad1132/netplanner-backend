"""
    This module contains RWA workers and their handlers
"""

import codecs
import pickle
import warnings

from celery import chain, group
from celery.app.task import Task
from celery.result import AsyncResult
from celery.utils import uuid
from celery_app import celeryapp
from clusters.schemas import ClusterDict
from database import session
from grooming.schemas import ClusteredTMs, GroomingResult
from physical_topology.schemas import PhysicalTopologySchema
from task_manager.schemas import ChainTaskID

from rwa.algorithm.components import Demand, Link, Node, RegenOption
from rwa.algorithm.oldnetwork import NetModule, OldNetwork
from rwa.models import RWAModel, RWARegisterModel
# from rwa.algorithm.planner import plan_network
from rwa.schemas import Lightpath, RoutingType, RWAForm, RWAResult
from rwa.utils import RWARepository


class RWAHandleFailure(Task):
    """
        Handles the failure of all RWA workers.
    """

    def on_failure(self, exc, task_id, *args, **kwargs):
        """
            If RWA worker runs fails celery runs this function.

            Responsibility if this function is to store exception into database

            :param exc: raised exception
            :param task_id: task id of instance
        """
        db = session()
        RWARepository.update_rwa_register(rwa_id=task_id,
                                          db=db,
                                          is_failed=True,
                                          exc=exc.__repr__())
        db.close()


class RWAHandle(RWAHandleFailure):
    """
        Handles the success of final phase of RWA multiprocess worker.
    """

    def on_success(self, retval, task_id, *args, **kwargs):
        """
            If RWA worker runs successfully after finishing worker celery runs this function.

            Responsibility if this function is to store results of RWA into database

            :param retval: return value of worker
            :param task_id: task id of instance
        """
        db = session()
        if (register := RWARepository.update_rwa_register(rwa_id=task_id, db=db, is_finished=True)):

            RWARepository.add_rwa(rwa_id=task_id,
                                  project_id=register.project_id,
                                  grooming_id=register.grooming_id,
                                  pt_id=register.pt_id,
                                  tm_id=register.tm_id,
                                  pt_version=register.pt_version,
                                  tm_version=register.tm_version,
                                  manager_id=register.manager_id,
                                  form=register.form,
                                  result=retval["result"],
                                  start_date=register.start_date,
                                  is_finished=True,
                                  db=db)
            db.close()


def run_rwa(physical_topology: PhysicalTopologySchema, cluster_info: ClusterDict,
            grooming_result: GroomingResult, rwa_form: RWAForm) -> ChainTaskID:
    """
        Background task that runs RWA algorithm with progress reports.

        : param physical_topology: The physical topology of the network
        : param cluster_info: The network cluster information
        : param grooming_result: The output of grooming algorithm
        : param rwa_form: Parameters required by RWA algorithm
        : type physical_topology: PhysicalTopologySchema
        : type cluster_info: ClusterDict
        : type grooming_result: GroomingResult
        : type rwa_form: RWAForm
        : return: returns the task IDs that can be used for progress report
        : rtype: ChainTaskID
    """
    chain_of_all_tasks, chain_task_id_info, _ = create_rwa_task_chain(physical_topology=physical_topology,
                                                                      cluster_info=cluster_info,
                                                                      grooming_result=grooming_result,
                                                                      rwa_form=rwa_form)
    chain_of_all_tasks_async = chain_of_all_tasks.apply_async()
    return ChainTaskID(**chain_task_id_info)


def create_rwa_task_chain(physical_topology: PhysicalTopologySchema, cluster_info: ClusterDict,
                          grooming_result: GroomingResult, rwa_form: RWAForm):
    """
        Assign an id to the entire rwa tasks submitted to the frontend.

        : param physical_topology: The physical topology of the network
        : param cluster_info: The network cluster information
        : param grooming_result: The output of grooming algorithm
        : param rwa_form: Parameters required by RWA algorithm
        : type physical_topology: PhysicalTopologySchema
        : type cluster_info: ClusterDict
        : type grooming_result: GroomingResult
        : type rwa_form: RWAForm
        : return: returns the required information to create ChainTaskID
    """
    demand_num = 0
    for sub_tm_id, grooming_output in grooming_result['traffic'].items():
        for demand in grooming_output['lightpaths'].values():
            demand_num += 1
    num_iterations = int(rwa_form["iterations"])
    algorithm = rwa_form["algorithm"]
    chain_task_id_info, preprocess_task_id, group_planner_id_list, finilize_task_id =\
        generate_rwa_task_info(
            demand_num, num_iterations, algorithm)
    chain_of_all_tasks = chain(rwa_preprocess.signature(args=(physical_topology, cluster_info,
                                                              grooming_result, rwa_form, demand_num),
                                                        options=({'task_id': preprocess_task_id})) |
                               rwa_group_planner.signature(
                                   args=(rwa_form, physical_topology, group_planner_id_list, finilize_task_id))
                               )
    return chain_of_all_tasks, chain_task_id_info, finilize_task_id


def run_rwa_test(physical_topology: PhysicalTopologySchema, cluster_info: ClusterDict,
                 grooming_result: GroomingResult, rwa_form: RWAForm):
    """
        This function is similar to run_rwa but returns the result instead of ids

        : param physical_topology: The physical topology of the network
        : param cluster_info: The network cluster information
        : param grooming_result: The output of grooming algorithm
        : param rwa_form: Parameters required by RWA algorithm
        : type physical_topology: PhysicalTopologySchema
        : type cluster_info: ClusterDict
        : type grooming_result: GroomingResult
        : type rwa_form: RWAForm
        : return:
    """
    chain_of_all_tasks, chain_task_id_info, finilize_task_id = create_rwa_task_chain(physical_topology=physical_topology,
                                                                                     cluster_info=cluster_info,
                                                                                     grooming_result=grooming_result,
                                                                                     rwa_form=rwa_form)
    rwa_result = chain_of_all_tasks()
    task_result = AsyncResult(finilize_task_id)
    # rwa_result = task_result.get()
    print(task_result.get())
    return


def generate_rwa_task_info(demand_number, num_iterations, algorithm):
    """
        Generates uuid for all RWA subtasks.

        In order to be able to track the progress of parallel and sequential tasks
        this function creates the uuid for all tasks before creation of the tasks
        in the chain. This function also estimates the total progress required by
        the RWA algorithm.

        : param demand_number: the total number of demands
        : param num_iterations: number of iterations for RWA algorithm
        : param algorithm: RWA algorithm type
        : type demand_number: int
        : type num_iterations: int
        : type algorithm: string
        : returns: chain_task_id_info, preprocess_task_id, group_planner_id_list, finilize_task_id
        : rtype: dict
    """
    # Chain id is now thw id of the final task
    finilize_task_id = uuid()
    chain_task_id_info = {
        'chain_id': finilize_task_id
    }
    chain_info = {}

    preprocess_task_id = uuid()
    preprocess_task_info = {
        'task_level': 0,
        'task_number': demand_number+7,
        'task_id_list': [{'id': preprocess_task_id}]
    }
    chain_info[0] = preprocess_task_info

    group_planner_id_list = [uuid() for _ in range(num_iterations)]
    group_planner_id_dict = [{'id': m_id} for m_id in group_planner_id_list]
    group_planner_task_info = {
        'task_level': 1,
        'task_number': num_iterations*demand_number,
        'task_id_list': group_planner_id_dict
    }
    if algorithm == "ILP":
        group_planner_task_info['task_number'] = 1
    chain_info[1] = group_planner_task_info

    finilize_task_info = {
        'task_level': 0,
        'task_number': 4,
        'task_id_list': [{'id': finilize_task_id}]
    }
    chain_info[2] = finilize_task_info

    chain_task_id_info['chain_info'] = chain_info
    return chain_task_id_info, preprocess_task_id, group_planner_id_list, finilize_task_id


@celeryapp.task(bind=True, base=RWAHandleFailure)
def rwa_preprocess(self, physical_topology: PhysicalTopologySchema, cluster_info: ClusterDict,
                   grooming_result: GroomingResult, rwa_form: RWAForm, demand_num):
    """
        This function performs the pre-process of the RWA algorithm.

        The preprocess includes the following steps:

            - The data is copied from the input schemas to internal network class of RWA algorithms.
            - Network graph is created using networkx.
            - Noise parametrs are estimated.
            - Candidate routing paths and regeneration options are calculated.

        : param physical_topology: The physical topology of the network
        : param cluster_info: The network cluster information
        : param grooming_result: The output of grooming algorithm
        : param rwa_form: Parameters required by RWA algorithm
        : param demand_num: Number of demands
        : type physical_topology: PhysicalTopologySchema
        : type cluster_info: ClusterDict
        : type grooming_result: GroomingResult
        : type rwa_form: RWAForm
        : type demand_num: int
        : return: {'result': pickled, 'current': total_steps, 'total': total_steps}

        .. note: : This function is a serial task in the celery chain.

        .. note:: Transferring data between the tasks should be serializable.
            Hence, the internal object of the rwa algorithm can't be used directly.
            To tackle this problem, the output is encoded as a base64 string.
            This string can be transferred between the tasks.
    """
    from grooming.schemas import ClusteredTMs, GroomingResult

    from rwa.algorithm.components import Demand, Link, Node, RegenOption
    from rwa.algorithm.oldnetwork import OldNetwork
    from rwa.algorithm.planner import plan_network
    from rwa.schemas import Lightpath, RoutingType, RWAResult

    print("\n Data received on the server for RWA!")
    total_steps = demand_num + 7
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': total_steps,
                                              'current_stage_info': 'Preprocess: Starting RWA Algorithm!'})

    print("\n Data received on the server for RWA!")
    self.update_state(state='PROGRESS', meta={
                      'current': 0, 'total': 100, 'status': 'Starting RWA Algorithm!'})
    Baud_rate = {
        'QPSK': 42.5e9,
        '8QAM': 42.5e9
    }

    reach_dict = {
        'QPSK': 800,  # Reach of this modulation
        '8QAM': 400
    }
    Snr_t = {
        'QPSK': 11.3,
        '8QAM': 16
    }

    Config = {
        'Pch': 2e-3,  # Launch Power (W)
        'Ls': 142,  # span length (Km)
        'gamma': 1.31,  # nonlinear parameter (W.km))^-1
        'beta2': 21.7,  # fiber dispersion (ps^2)/km
        'alpha_db': 0.2,  # fiber power attenuation (dB/km)
        'nu': 193,     # optical carrier frequency (THz)
        'baud_rate': Baud_rate,  # Symbol Rate
        'Nch': 80,     # Number of channels
        'deltaF': 100e9,  # Channel spacing
        'Bs': Baud_rate,  # Signal bandwidth
        'nsp': 1.77,    # spontaneous emission factor
        'booster_gain': 20,
        'inner_loss': 8  # loss inside the centers
    }

    # Standardizing the parameters
    Config['alpha_Np'] = (Config['alpha_db']/1000) / 8.685889638
    Config['gamma'] = Config['gamma'] * 1e-3
    Config['beta2'] = Config['beta2'] * 1e-27
    Config['Ls'] = Config['Ls'] * 1e3
    Config['nu'] = Config['nu'] * 1e12

    max_num_wavelengths = 80
    Config['Nch'] = max_num_wavelengths
    NET = OldNetwork(max_num_wavelengths, reach_dict,
                     snr_t=Snr_t, config=Config)
    self.update_state(state='PROGRESS', meta={'current': 1, 'total': total_steps,
                                              'current_stage_info': 'Preprocess: Reading nodes.'})
    for node in physical_topology["nodes"]:
        if node["roadm_type"] == "Directionless" or node["roadm_type"] == "CDC":
            roadm_type = node["roadm_type"]
        else:
            roadm_type = "CDC"
        NET.add_node(node["name"], (node["lat"], node["lng"]),
                     roadm_type=roadm_type)
    self.update_state(state='PROGRESS', meta={'current': 2, 'total': total_steps,
                                              'current_stage_info': 'Preprocess: Reading links.'})
    for link in physical_topology["links"]:
        #### EDITED UP TO HERE ###################################
        ##########################################################
        link_nodes = (link["source"], link["destination"])
        special = False
        # num_span = 1
        # if num_span > 1:
        #     special = True
        #     distance = []
        #     fiber = []
        #     loss = []
        #     for i in range(link.NumSpan):
        #         distance.append(link.SpanObjList[i].Length)
        #         link_fiber = Config.copy()
        #         link_fiber['beta2'] = link.SpanObjList[0].Dispersion
        #         link_fiber['gamma'] = link.SpanObjList[0].Gamma
        #         fiber.append(link_fiber)
        #         loss.append(link.SpanObjList[i].Loss)
        # else:
        fiber = Config.copy()
        # fiber['beta2'] = link.SpanObjList[0].Dispersion
        # fiber['gamma'] = link.SpanObjList[0].Gamma
        distance = link["length"]
        loss = 0.25
        NET.add_link(link_nodes, distance, loss,  fiber, special)

    # MERGING DEMANDS WILL BE ADDED LATER
    # if type(decoded_network.ParamsObj.merge) != type(True):
    #     print("INVALID value for merge, it should be either True or False.")
    # else:
    #     NET.merging_demands = decoded_network.ParamsObj.merge
    NET.merging_demands = False
    self.update_state(state='PROGRESS', meta={'current': 3, 'total': total_steps,
                                              'current_stage_info': 'Preprocess: Reading clusters.'})
    if cluster_info:
        for cluster_id in cluster_info['clusters'].keys():
            gateway = cluster_info['clusters'][cluster_id]['data']['gateways']
            subnode_list = cluster_info['clusters'][cluster_id]['data']['subnodes']
            NET.add_cluster(gateway, subnode_list, cluster_id)
    demand_info_list = []
    self.update_state(state='PROGRESS', meta={'current': 4, 'total': total_steps,
                                              'current_stage_info': 'Preprocess: Reading demands.'})
    for sub_tm_id, grooming_output in grooming_result['traffic'].items():
        for demand in grooming_output['lightpaths'].values():
            if demand["routing_type"] == "100GE":
                demand_type = '100G'
            else:
                print("INVALID demand type, using 100G instead.")
                demand_type = '100G'
            demand_info_list.append(demand_type)
            if demand["protection_type"] == "1+1_NodeDisjoint" or demand["protection_type"] == "NoProtection":
                protection_type = demand["protection_type"]
            else:
                protection_type = "1+1_NodeDisjoint"

            if demand["restoration_type"] == "JointSame" or demand["restoration_type"] == "AdvJointSame":
                restoration_type = demand["restoration_type"]
                has_restoration = True
            else:
                restoration_type = None
                has_restoration = False
            # protection_type = "NoProtection"
            cluster_id = grooming_output["cluster_id"]
            if cluster_id == 'main':
                cluster_id = 0
            previous_id = demand["id"]
            NET.add_demand(demand["source"],  demand["destination"], modulation=rwa_form["modulation_type"],
                           demand_type=demand_type, protection_type=protection_type,
                           cluster_id=cluster_id, previous_id=previous_id, restoration_type=restoration_type,
                           has_restoration=has_restoration)
    NET.print_demand_list()
    NET.alpha = float(rwa_form["trade_off"])
    # EON28.segment_diversity = True
    NET.segment_diversity = False
    NET.measure = 'osnr'  # 'osnr' 'distance'
    NET.margin = int(rwa_form["noise_margin"])
    self.update_state(state='PROGRESS', meta={'current': 5, 'total': total_steps,
                                              'current_stage_info': 'Preprocess: Generating network graph.'})
    NET.gen_graph()
    self.update_state(state='PROGRESS', meta={'current': 6, 'total': total_steps,
                                              'current_stage_info': 'Preprocess: Estimating parameters.'})
    if NET.measure == 'osnr':
        NET.estimate_reach(reach_step=50)
    k = int(rwa_form["shortest_path_k"])
    net_module = NetModule(NET, NET.lower_bound,
                           NET.upper_bound, k, is_root=True)
    net_module.estimate_link_noise()
    self.update_state(state='PROGRESS', meta={'current': 7, 'total': total_steps,
                                              'current_stage_info': 'Preprocess: Generating candidate lighpaths.'})
    net_module.gen_protected_lightpaths(k, celeryapp_instance=self)
    pickled = codecs.encode(pickle.dumps(net_module), "base64").decode()
    print(type(pickled))
    return {'result': pickled, 'current': total_steps, 'total': total_steps}


@celeryapp.task(bind=True, base=RWAHandleFailure)
def rwa_greedy_iteration(self, net_module_bytes, rwa_form):
    """One iteration of the Greedy RWA algorithm.

    : param net_module_bytes: pickled inner RWA object generated by preprocessing.
    : param rwa_form: RWA parameters
    : type net_module_bytes: base64
    : type rwa_form: RWAForm
    : returns: a pickled version of the inner class net_module (result_net)
    : rtype: dict
    """
    from rwa.algorithm.oldnetwork import random_shuffle_solver
    num_second_restoration_random_samples = 10
    net_module = pickle.loads(codecs.decode(
        net_module_bytes.encode(), "base64"))
    total_steps = len(net_module.demand_list)
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': total_steps,
                                              'current_stage_info': 'Starting RWA greedy algorithm.'})
    iterations = int(rwa_form["iterations"])
    if rwa_form["restoration_k"]:
        k_restoration = int(rwa_form["restoration_k"])
    else:
        print("INVALID k_restoration using default value")
        k_restoration = 2
    k_second_restoration = 1
    result_net = random_shuffle_solver(
        net_module, solver="Greedy",
        k_restoration=k_restoration,
        k_second_restoration=k_second_restoration,
        num_second_restoration_random_samples=num_second_restoration_random_samples,
        celeryapp_instance=self
    )
    pickled = codecs.encode(pickle.dumps(result_net), "base64").decode()
    return {'result': pickled, 'current': total_steps, 'total': total_steps}


@celeryapp.task(bind=True, base=RWAHandleFailure)
def rwa_gilp_iteration(self, net_module_bytes, rwa_form):
    """One iteration of the Group ILP RWA algorithm.

    : param net_module_bytes: pickled inner RWA object generated by preprocessing.
    : param rwa_form: RWA parameters
    : type net_module_bytes: base64
    : type rwa_form: RWAForm
    : returns: a pickled version of the inner class net_module (result_net)
    : rtype: dict
    """
    from rwa.algorithm.oldnetwork import random_shuffle_solver
    num_second_restoration_random_samples = 10
    net_module = pickle.loads(codecs.decode(
        net_module_bytes.encode(), "base64"))
    total_steps = len(net_module.demand_list)
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': total_steps,
                                              'current_stage_info': 'Starting RWA GILP algorithm.'})
    solver = "window_ILP"
    if rwa_form["restoration_k"]:
        k_restoration = int(rwa_form["restoration_k"])
    else:
        print("INVALID k_restoration using default value")
        k_restoration = 2
    k_second_restoration = 1
    GroupSize = int(rwa_form["group_size"])
    History = int(rwa_form["history_window"])
    result_net = random_shuffle_solver(
        net_module, solver="window_ILP",
        k_restoration=k_restoration,
        k_second_restoration=k_second_restoration,
        history_window=History,
        demand_group_size=GroupSize,
        max_new_wavelength_num=History,
        celeryapp_instance=self
    )
    pickled = codecs.encode(pickle.dumps(result_net), "base64").decode()
    return {'result': pickled, 'current': total_steps, 'total': total_steps}


@celeryapp.task(bind=True, base=RWAHandleFailure)
def rwa_ilp(self, net_module_bytes, rwa_form):
    """
        Runs the ILP based RWA algorithm.

        : param net_module_bytes: pickled inner RWA object generated by preprocessing.
        : param rwa_form: RWA parameters
        : type net_module_bytes: base64
        : type rwa_form: RWAForm
        : returns: a pickled version of the inner class net_module (result_net)
        : rtype: dict
    """
    from rwa.algorithm.oldnetwork import random_shuffle_solver
    self.update_state(state='PROGRESS', meta={
                      'current': 0, 'total': 1, 'current_stage_info': 'Starting RWA GILP algorithm.'})
    num_second_restoration_random_samples = 10
    net_module = pickle.loads(codecs.decode(
        net_module_bytes.encode(), "base64"))
    solver = "window_ILP"
    if rwa_form["restoration_k"]:
        k_restoration = int(rwa_form["restoration_k"])
    else:
        print("INVALID k_restoration using default value")
        k_restoration = 2
    k_second_restoration = 1
    GroupSize = int(rwa_form["group_size"])
    History = int(rwa_form["history_window"])
    net_module.solve_two_way_protected_ILP()
    result_net = net_module
    pickled = codecs.encode(pickle.dumps(result_net), "base64").decode()
    return {'result': pickled, 'current': 1, 'total': 1}


@celeryapp.task(bind=True, base=RWAHandleFailure)
def rwa_group_planner(self, preprocess_output, rwa_form, physical_topology,
                        group_planner_id_list, finilize_task_id):
    """Main function that runs the desired RWA algorithm described in rwa_form.

    : param preprocess_output: a dict containing the pickled inner RWA object generated by preprocessing.
    : param rwa_form: RWA parameters
    : param group_planner_id_list: RWA parameters
    : param finilize_task_id: the id of the last task(finilize) in the task chain
    : type net_module_bytes: base64
    : type rwa_form: RWAForm
    : type group_planner_id_list: list
    : type finilize_task_id: string
    """
    net_module_bytes = preprocess_output['result']
    algorithm = rwa_form["algorithm"]
    iterations = rwa_form["iterations"]
    if algorithm == "Greedy":
        return (group([rwa_greedy_iteration.signature(args=(net_module_bytes, rwa_form),
                                                      options=({'task_id': group_planner_id_list[i]}))
                       for i in range(iterations)]) |
                rwa_finilize_results.signature(args=(physical_topology,),
                                                options=({'task_id': finilize_task_id})))()

    elif algorithm == "GILP":
        return (group([rwa_gilp_iteration.signature(args=(net_module_bytes, rwa_form),
                                                    options=({'task_id': group_planner_id_list[i]}))
                       for i in range(iterations)]) |
                rwa_finilize_results.signature(args=(physical_topology,),
                                                options=({'task_id': finilize_task_id})))()
    elif algorithm == "ILP":
        iterations = 1
        return (group([rwa_ilp.signature(args=(net_module_bytes, rwa_form),
                                         options=({'task_id': group_planner_id_list[i]}))
                       for i in range(iterations)]) |
                rwa_finilize_results.signature(args=(physical_topology,),
                                                options=({'task_id': finilize_task_id})))()
    else:
        assert False


@celeryapp.task(bind=True, base=RWAHandle)
def rwa_finilize_results(self, result_dict_list, physical_topology):  # group_collected_results
    """Collects the results of all tasks and generates the output.


== == == =

    # if decoded_network.ParamsObj.numRandomChoices:
    #     num_random_choices = int(decoded_network.ParamsObj.numRandomChoices)
    # else:
    #     print("INVALID numRandomChoices using default value")
    num_random_choices = 10
    # assert False
    if algorithm == "Greedy":
        iterations = int(rwa_form["iterations"])
        print("Server is preparing the greedy RWA planner.")
        result_net = plan_network(NET, k=k, k_restoration=k_restoration, k_second_restoration=1, num_second_restoration_random_samples=num_random_choices,
                                  solver='Greedy', iterations=iterations, processors=processors)
    elif algorithm == "GroupILP":
        iterations = int(rwa_form["iterations"])
        GroupSize = int(rwa_form["group_size"])
        History = int(rwa_form["history_window"])
        print("Server is preparing the windowed Group ILP RWA planner.")
        result_net = plan_network(NET, k=k, solver='window_ILP', iterations=iterations, processors=processors,
                                  max_new_wavelength_num=GroupSize, history_window=History, demand_group_size=GroupSize)
    elif algorithm == "ILP":
        print("Server is preparing the Exact ILP RWA planner.")
        result_net = plan_network(
            NET, k=k, solver='ILP', processors=processors)
    else:
        print("INVALID SOLVER!")
        result_net = None
>>>>>> > master

    : param result_dict_list: a dict containing the pickled inner RWA object generated by preprocessing.
    : type result_dict_list: list
    : returns: the output of the RWA algorithm
    : rtype: dict containg RWAResult
    """
    from rwa.algorithm.Analysis import detect_wavelength_collisions
    from rwa.schemas import Lightpath, RWALightpathsOutput, RWAResult
    from rwa.utils import generate_RWA_general_info
    
    total_steps = 4
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': total_steps,
                                              'current_stage_info': 'Finalizing RWA results.'})
    for i in range(len(result_dict_list)):
        planned_net_module = pickle.loads(codecs.decode(
            result_dict_list[i]['result'].encode(), "base64"))
        objective = 100000
        if planned_net_module is not None:
            print("  -Objective in iteration {}: {:3.2f}".format(i,
                  planned_net_module.upper_bound))
            if planned_net_module.upper_bound < objective:
                objective = planned_net_module.upper_bound
                # print(objective)
                result_net = planned_net_module
                # print(result_net.total_num_wavelengths)
        else:
            warnings.warn("Solution of iteration {} is invalid".format(i))
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': total_steps,
                                              'current_stage_info': 'Re-calculating SNRs.'})
    result_net.exact_link_noise()
    result_net.assign_extracted_lightpath_osnr()
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': total_steps,
                                              'current_stage_info': 'Checking the lightpaths.'})
    detect_wavelength_collisions(result_net, print_collisions=True)
    output_lightpath_dict = {}
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': total_steps,
                                              'current_stage_info': 'Preparing the output.'})
    if result_net is not None:
        # result_net.print_results()
        # result_net.print_demand_list()
        for i, lightpath in enumerate(result_net.extractedLightpathlist):
            lightpath_dict = {}
            lightpath_dict['id'] = lightpath.demand.previous_id
            lightpath_dict['source'] = lightpath.demand.ingress_node.index
            lightpath_dict['destination'] = lightpath.demand.egress_node.index
            lightpath_dict['cluster_id'] = lightpath.demand.cluster_id
            lightpath_dict['routing_type'] = '100GE'  # RoutingType.GE100
            lightpath_dict['protection_type'] = lightpath.demand.protection_type
            if lightpath.demand.restoration_type is None:
                lightpath_dict['restoration_type'] = "None"
            else:
                lightpath_dict['restoration_type'] = lightpath.demand.restoration_type
            routing_info_dict = {}
            selected_wavelength = lightpath.selected_regen_option.main_option.path_wavelengths
            routing_info_dict['working'] = {
                'wavelength': [selected_wavelength]*len(lightpath.main_osnr),
                'path': lightpath.selected_regen_option.main_option.path,
                'regenerators': lightpath.selected_regen_option.main_option.regen_nodes_index,
                'snr': lightpath.main_osnr,
            }
            if lightpath.selected_regen_option.protection_option.path:
                routing_info_dict['protection'] = {
                    'wavelength': [lightpath.selected_regen_option.protection_option.path_wavelengths]*len(lightpath.protection_osnr),
                    'path': lightpath.selected_regen_option.protection_option.path,
                    'regenerators': lightpath.selected_regen_option.protection_option.regen_nodes_index,
                    'snr': lightpath.protection_osnr,
                }
            # filling the restoration output
            restorationPathList = []
            restorationPathRegenerators = []
            restorationSNRs = []
            restorationLengths = []
            restorationFailedLinks = []
            if lightpath.selected_regen_option.restoration_option_list:
                restorationSNRs = lightpath.restoration_osnrs
                restorationLengths = lightpath.restoration_lengths
                restorationPathList = lightpath.restoration_paths
                restorationPathRegenerators = lightpath.restoration_regens
                restorationFailedLinks = lightpath.restoration_failed_links
            if restorationPathList:
                restoration_info = []
                for restoration_index in range(len(restorationPathList)):
                    if isinstance(restorationSNRs[restoration_index], list):
                        for second_restoration_index in range(len(restorationPathList[restoration_index])):
                            snr = restorationSNRs[restoration_index][second_restoration_index]
                            if not isinstance(snr, list):
                                snr = [snr]
                            if restorationFailedLinks[restoration_index][second_restoration_index]:
                                restoration_info.append({
                                    'first_failure': restorationFailedLinks[restoration_index][second_restoration_index][0:2],
                                    'second_failure': restorationFailedLinks[restoration_index][second_restoration_index][2:4],
                                    'restoration_algorithm': 'Advanced',
                                    'info': {
                                        'wavelength': [selected_wavelength]*len(snr),
                                        'path': restorationPathList[restoration_index][second_restoration_index],
                                        'regenerators': restorationPathRegenerators[restoration_index][second_restoration_index],
                                        'snr': snr,
                                    }
                                })
                    elif restorationPathList[restoration_index] is not None:
                        snr = restorationSNRs[restoration_index]
                        if not isinstance(snr, list):
                            snr = [snr]
                        restoration_info.append({
                            'first_failure': restorationFailedLinks[restoration_index][0:2],
                            'restoration_algorithm': 'Basic',
                            'info': {
                                'wavelength': [selected_wavelength]*len(snr),
                                'path': restorationPathList[restoration_index],
                                'regenerators': restorationPathRegenerators[restoration_index],
                                'snr': snr,
                            }
                        })
                if restoration_info:
                    routing_info_dict['restoration'] = restoration_info
            # routing info is completed
            lightpath_dict['routing_info'] = routing_info_dict
            lightpath_output = Lightpath(**lightpath_dict)
            output_lightpath_dict[lightpath.demand.previous_id] = lightpath_output
    result_dict = {'lightpaths': output_lightpath_dict}
    rwa_lightpaths = RWALightpathsOutput(**result_dict).dict()
    general_info = generate_RWA_general_info(physical_topology=physical_topology, rwa_lightpaths=rwa_lightpaths) 
    result_dict["general_info"] = general_info.dict()
    rwa_result = RWAResult(**result_dict)
    # import json
    # print(json.dumps(rwa_result.dict(), indent=4))
    return {'result': rwa_result.dict(), 'current': total_steps, 'total': total_steps}
