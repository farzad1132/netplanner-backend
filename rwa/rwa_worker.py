from celery_app import celeryapp
from celery.app.task import Task
from physical_topology.schemas import PhysicalTopologySchema
from clusters.schemas import ClusterDict
from grooming.schemas import GroomingResult
from rwa.schemas import RWAForm, RWAResult
from database import session
from rwa.models import RWAModel, RWARegisterModel

class RWAHandle(Task):
    def on_success(self, retval, task_id, *args, **kwargs):
        db = session()
        if (register:=db.query(RWARegisterModel)\
            .filter_by(id=task_id, is_deleted=False).one_or_none()):
            rwa_res = RWAModel( id=task_id,
                                project_id=register.project_id,
                                grooming_id=register.grooming_id,
                                pt_id=register.pt_id,
                                tm_id=register.tm_id,
                                pt_version=register.pt_version,
                                tm_version=register.tm_version,
                                manager_id=register.manager_id,
                                form=register.form,
                                lightpaths=retval["lightpaths"],
                                start_date=register.start_date)
            db.add(rwa_res)
            db.commit()
            db.close()

    def on_failure(self, exc, task_id, *args, **kwargs):
        db = session()
        if (register:=db.query(RWARegisterModel)\
            .filter_by(id=task_id).one_or_none()) is not None:
            register.is_failed = True
            register.exception = exc.__repr__()

            db.add(register)
            db.commit()
            db.close()


@celeryapp.task(bind=True, base=RWAHandle)
def rwa_task(self, physical_topology: PhysicalTopologySchema, cluster_info: ClusterDict,
    grooming_result: GroomingResult, rwa_form: RWAForm) -> RWAResult:
    """
    Background task that runs RWA algorithm with progress reports.
    Inputs:
        rwa_form: RWAForm
        rwa_input: RWAResult (without routing info!)
        physical_topology: PhysicalTopology
    output:
        rwa_result: RWAResult
    """
    from rwa.algorithm.components import Node, Link, Demand, RegenOption
    from rwa.algorithm.oldnetwork import OldNetwork
    from rwa.algorithm.planner import plan_network
    from rwa.schemas import RWAResult, Lightpath, RoutingType
    from grooming.schemas import GroomingResult, ClusteredTMs
    
    print("\n Data received on the server for RWA!")
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': 100, 'status': 'Starting RWA Algorithm!'})
    Baud_rate = {
        'QPSK' : 42.5e9,
        '8QAM': 42.5e9
    }

    reach_dict = {
        'QPSK' : 800, # Reach of this modulation
        '8QAM' : 400
    }
    Snr_t = {
        'QPSK':11.3,
        '8QAM':16
    }
    
    Config = {
        'Pch': 2e-3, # Launch Power (W)
        'Ls': 142, # span length (Km)
        'gamma': 1.31, # nonlinear parameter (W.km))^-1
        'beta2': 21.7, # fiber dispersion (ps^2)/km
        'alpha_db': 0.2, # fiber power attenuation (dB/km)
        'nu': 193,     # optical carrier frequency (THz)
        'baud_rate': Baud_rate,  # Symbol Rate
        'Nch': 80,     # Number of channels
        'deltaF': 100e9, # Channel spacing
        'Bs': Baud_rate,  # Signal bandwidth
        'nsp': 1.77,    # spontaneous emission factor
        'booster_gain': 20,
        'inner_loss': 8 #loss inside the centers
    }

    # Standardizing the parameters
    Config['alpha_Np'] = (Config['alpha_db']/1000)/ 8.685889638
    Config['gamma'] = Config['gamma'] * 1e-3
    Config['beta2'] = Config['beta2'] * 1e-27
    Config['Ls'] = Config['Ls'] * 1e3
    Config['nu'] = Config['nu'] * 1e12

    max_num_wavelengths = 80
    Config['Nch'] = max_num_wavelengths
    NET = OldNetwork(max_num_wavelengths,reach_dict,snr_t=Snr_t, config = Config)
    for node in physical_topology["nodes"]:
        if node["roadm_type"] == "Directionless" or node["roadm_type"] == "CDC":
            roadm_type = node["roadm_type"]
        else:
            roadm_type = "CDC"
        NET.add_node(node["name"], (node["lat"], node["lng"]), roadm_type= roadm_type)
      
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
        NET.add_link(link_nodes,distance,loss,  fiber, special)     
    
    # MERGING DEMANDS WILL BE ADDED LATER
    # if type(decoded_network.ParamsObj.merge) != type(True):
    #     print("INVALID value for merge, it should be either True or False.")
    # else:
    #     NET.merging_demands = decoded_network.ParamsObj.merge
    NET.merging_demands = False
    if cluster_info:
        for cluster_id in cluster_info['clusters'].keys():
            gateway = cluster_info['clusters'][cluster_id]['data']['gateways']
            subnode_list = cluster_info['clusters'][cluster_id]['data']['subnodes']
            NET.add_cluster(gateway, subnode_list, cluster_id)
    demand_info_list = []
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
            NET.add_demand(demand["source"],  demand["destination"], modulation = rwa_form["modulation_type"],
                            demand_type = demand_type, protection_type= protection_type,
                            cluster_id=cluster_id, previous_id = previous_id, restoration_type=restoration_type,
                            has_restoration=has_restoration)
    NET.print_demand_list()    
    NET.alpha = float(rwa_form["trade_off"])
    # EON28.segment_diversity = True
    NET.segment_diversity = False
    NET.measure = 'osnr' #'osnr' 'distance'
    NET.margin = int(rwa_form["noise_margin"])
    # D is the number of demands.
    # k determines the k-shortest path.
    # end_depth controls the number of demand order changes.
    algorithm = rwa_form["algorithm"]
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': 100, 'status': 'Algorithm Finished'})

    # D is the number of demands.
    # k determines the k-shortest path.
    # end_depth controls the number of demand order changes.
    algorithm = rwa_form["algorithm"]
    # print(algorithm)
    k = int(rwa_form["shortest_path_k"])
    processors = 2
    if rwa_form["restoration_k"]:
        k_restoration = int(rwa_form["restoration_k"])
    else:
        print("INVALID k_restoration using default value")
        k_restoration = 2
    
    # if decoded_network.ParamsObj.numRandomChoices:
    #     num_random_choices = int(decoded_network.ParamsObj.numRandomChoices)
    # else:
    #     print("INVALID numRandomChoices using default value")
    num_random_choices = 10
    # assert False
    if algorithm == "Greedy":
        iterations = int(rwa_form["iterations"])
        print("Server is preparing the greedy RWA planner.")
        result_net = plan_network(NET, k=k,k_restoration=k_restoration,k_second_restoration=1, num_second_restoration_random_samples= num_random_choices,
                                solver='Greedy', iterations = iterations, processors = processors) 
    elif algorithm == "GroupILP":
        iterations = int(rwa_form["iterations"])
        GroupSize = int(rwa_form["group_size"])
        History = int(rwa_form["history_window"])
        print("Server is preparing the windowed Group ILP RWA planner.")
        result_net = plan_network(NET, k=k, solver='window_ILP', iterations = iterations, processors = processors,
                             max_new_wavelength_num = GroupSize, history_window = History, demand_group_size = GroupSize)     
    elif algorithm == "ILP":
        print("Server is preparing the Exact ILP RWA planner.")
        result_net = plan_network(NET, k=k, solver='ILP', processors =processors)
    else:
        print("INVALID SOLVER!")
        result_net = None 

    output_lightpath_dict = {}
    if result_net is not None:
        # result_net.print_results()
        # result_net.print_demand_list()
        for i,lightpath in enumerate(result_net.extractedLightpathlist):
            lightpath_dict = {}
            lightpath_dict['id'] = lightpath.demand.previous_id
            lightpath_dict['source'] = lightpath.demand.ingress_node.index
            lightpath_dict['destination'] = lightpath.demand.egress_node.index
            lightpath_dict['cluster_id'] = lightpath.demand.cluster_id
            lightpath_dict['routing_type'] = '100GE' #RoutingType.GE100
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
            restorationPathList=[]
            restorationPathRegenerators=[]
            restorationSNRs=[]
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
    rwa_result = RWAResult(**result_dict)
    import json
    print(json.dumps(rwa_result.dict(), indent=4))
    self.update_state(state='SUCCESS', meta={'current': 100, 'total': 100, 'status':'RWA finished. Sending back the results'})
    return rwa_result.dict()

