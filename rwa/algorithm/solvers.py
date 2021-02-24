import numpy as np
import math 
from rwa.algorithm.components import *
import cvxpy as cp
import scipy.sparse as sp
import warnings
# from oldnetwork import OldNetwork, NetModule

def ILP_2way_protected_solver_subroutine(network, available_wavelengths, demands,
                                         preoccupied_wavelength_on_links = None,
                                         preoccupied_wavelength_on_nodes = None, history_window = 0):
  if network.merging_demands:
    warnings.warn("The selected ILP subroutine is not capable of merging demands.")
    assert False
  # modulation = 'QPSK'
  # Extract all of possible pathes (with protection) from RegenOptions
  protected_path_list = [] # list of all possible pathes  
  for option in network.RegenOptionDict.keys():
      # if option[2] == modulation:
      for r in network.RegenOptionDict[option]:
        main_r, protect_r = r.main_option, r.protection_option
        protected_path = (main_r.path, protect_r.path)
        # regen_num = len(main_r.regen_nodes_index) + len(protect_r.regen_nodes_index)
        if protected_path not in protected_path_list:
          protected_path_list.append(protected_path)
          # regen_number_list.append(path_id, regen_num)
  # print(protected_path_list)
  wavelength_num = len(available_wavelengths)
  path_num = len(protected_path_list)
  demand_num = len(demands)
  G = network.graph.to_undirected()
  edge_num = len(G.edges)
  node_num = len(G.nodes)

  # assignment_matrix = np.zeros((demand_num, demand_num, path_num, wavelength_num))
  assignment_matrix_original_shape = (demand_num, demand_num, path_num, wavelength_num)
  assignment_matrix_reshaped_shape = (demand_num, demand_num * path_num * wavelength_num)
  row = []
  col = []
  for demand_id, demand in enumerate(demands):
    option = (demand.ingress_node.index, demand.egress_node.index, demand.modulation, demand.protection_type, demand.cluster_id)
    for path_id, (main_inlist, protection_inlist) in enumerate(protected_path_list):
      for r in network.RegenOptionDict[option]:
        main_r_path, protection_r_path = r.main_option.path, r.protection_option.path
        if main_inlist == main_r_path and protection_inlist == protection_r_path:
          for w_id, w in enumerate(available_wavelengths):
            # assignment_matrix[demand_id, demand_id, path_id, w_id] = 1
            ids = np.unravel_index(np.ravel_multi_index((demand_id, demand_id, path_id, w_id),
                                        assignment_matrix_original_shape), assignment_matrix_reshaped_shape)
            row.append(ids[0])
            col.append(ids[1])
  assignment_matrix_sparse = sp.coo_matrix((np.ones(len(row)), (row, col)), assignment_matrix_reshaped_shape)
  # assignment_matrix = assignment_matrix.reshape(demand_num, -1)          

  # link_occupation_matrix = np.zeros((edge_num, wavelength_num, demand_num, path_num, wavelength_num))
  link_occupation_matrix_original_shape = (edge_num, wavelength_num, demand_num, path_num, wavelength_num)
  link_occupation_matrix_reshaped_shape = (edge_num * wavelength_num, demand_num* path_num* wavelength_num)
  row = []
  col = []
  for demand_id, demand in enumerate(demands):
    option = (demand.ingress_node.index, demand.egress_node.index, demand.modulation, demand.protection_type, demand.cluster_id)
    for path_id, (main_inlist, protection_inlist) in enumerate(protected_path_list):
      for r in network.RegenOptionDict[option]:
        main_r_path, protection_r_path = r.main_option.path, r.protection_option.path
        if main_inlist == main_r_path and protection_inlist == protection_r_path:
          for path in [main_r_path, protection_r_path]:
            for i,node in enumerate(path):
              if i < len(path)-1:
                if (node,path[i+1]) in list(G.edges):
                  edge_id = list(G.edges).index((node,path[i+1]))
                else:
                  edge_id = list(G.edges).index((path[i+1], node))
                for w_id, w in enumerate(available_wavelengths):
                  # link_occupation_matrix[edge_id, w_id, demand_id, path_id, w_id] = 1
                  ids = np.unravel_index(np.ravel_multi_index((edge_id, w_id, demand_id, path_id, w_id),
                                        link_occupation_matrix_original_shape), link_occupation_matrix_reshaped_shape)
                  row.append(ids[0])
                  col.append(ids[1])
  # link_occupation_matrix = link_occupation_matrix.reshape(edge_num*wavelength_num, -1)
  link_occupation_matrix_sparse = sp.coo_matrix((np.ones(len(row)), (row, col)), link_occupation_matrix_reshaped_shape)


  # general_occupation_matrix = np.zeros((wavelength_num, edge_num, wavelength_num))/edge_num
  general_occupation_matrix_original_shape = (wavelength_num, edge_num, wavelength_num)
  general_occupation_matrix_reshaped_shape = (wavelength_num, edge_num * wavelength_num)
  row = []
  col = []
  for w_id, w in enumerate(available_wavelengths):
    for edge_id, edge in enumerate(G.edges):
      # general_occupation_matrix[w_id, edge_id, w_id] = 1
      ids = np.unravel_index(np.ravel_multi_index((w_id, edge_id, w_id),
                                general_occupation_matrix_original_shape), general_occupation_matrix_reshaped_shape)
      row.append(ids[0])
      col.append(ids[1])
  general_occupation_matrix_sparse = sp.coo_matrix((np.ones(len(row))/edge_num, (row, col)), general_occupation_matrix_reshaped_shape)
  # general_occupation_matrix = general_occupation_matrix.reshape(wavelength_num, -1)/edge_num

  regen_number_matrix = np.zeros((demand_num, path_num, wavelength_num))
  for demand_id, demand in enumerate(demands):
    option = (demand.ingress_node.index, demand.egress_node.index, demand.modulation, demand.protection_type, demand.cluster_id)
    for path_id, (main_inlist, protection_inlist) in enumerate(protected_path_list):
      for r in network.RegenOptionDict[option]:
        main_r_path, protection_r_path = r.main_option.path, r.protection_option.path
        if main_inlist == main_r_path and protection_inlist == protection_r_path:
          regen_number = len(r.main_option.regen_nodes_index)+len(r.protection_option.regen_nodes_index)
          for w_id, w in enumerate(available_wavelengths): 
            regen_number_matrix[demand_id, path_id, w_id] = regen_number
  regen_number_matrix = regen_number_matrix.reshape(-1)

  # roadm_occupation_matrix = np.zeros((demand_num, node_num, wavelength_num, demand_num, path_num, wavelength_num))
  roadm_occupation_matrix_original_shape = (demand_num, node_num, wavelength_num, demand_num, path_num, wavelength_num)
  roadm_occupation_matrix_reshaped_shape = (demand_num * node_num * wavelength_num, demand_num * path_num * wavelength_num)
  row = []
  col = []
  directionless_roadms = False
  for demand_id, demand in enumerate(demands):
    option = (demand.ingress_node.index, demand.egress_node.index, demand.modulation, demand.protection_type, demand.cluster_id)
    for node in [demand.ingress_node, demand.egress_node]:
      if node.roadm_type == "Directionless":
        directionless_roadms = True
        for path_id, (main_inlist, protection_inlist) in enumerate(protected_path_list):
          for r in network.RegenOptionDict[option]:
            main_r_path, protection_r_path = r.main_option.path, r.protection_option.path
            if main_inlist == main_r_path and protection_inlist == protection_r_path:
              for w_id, w in enumerate(available_wavelengths):
                n_id = network.node_index_list.index(node.index)  # node_list and node_index_list should have same ordering
                # roadm_occupation_matrix[demand_id, n_id, w_id, demand_id, path_id, w_id] = 1
                ids = np.unravel_index(np.ravel_multi_index((demand_id, n_id, w_id, demand_id, path_id, w_id),
                                roadm_occupation_matrix_original_shape), roadm_occupation_matrix_reshaped_shape)
                row.append(ids[0])
                col.append(ids[1])
  # roadm_occupation_matrix = roadm_occupation_matrix.reshape(demand_num*node_num*wavelength_num, -1)
  roadm_occupation_matrix_sparse = sp.coo_matrix((np.ones(len(row)), (row, col)), roadm_occupation_matrix_reshaped_shape)


  if directionless_roadms:
    # roadm_single_usage_matrix = np.zeros((node_num, wavelength_num, demand_num, node_num, wavelength_num))
    roadm_single_usage_matrix_original_shape = (node_num, wavelength_num, demand_num, node_num, wavelength_num)
    roadm_single_usage_matrix_reshaped_shape = (node_num * wavelength_num, demand_num * node_num * wavelength_num)
    row = []
    col = []
    for n_id, node in enumerate(network.node_list):
      if node.roadm_type == "Directionless":
        for demand_id, demand in enumerate(demands):
          for w_id, w in enumerate(available_wavelengths):
            # roadm_single_usage_matrix[n_id, w_id, demand_id, n_id, w_id] = 1
            ids = np.unravel_index(np.ravel_multi_index((n_id, w_id, demand_id, n_id, w_id),
                                roadm_single_usage_matrix_original_shape), roadm_single_usage_matrix_reshaped_shape)
            row.append(ids[0])
            col.append(ids[1])
    # roadm_single_usage_matrix = roadm_single_usage_matrix.reshape(node_num*wavelength_num, -1)
    roadm_single_usage_matrix_sparse = sp.coo_matrix((np.ones(len(row)), (row, col)), roadm_single_usage_matrix_reshaped_shape)

  X = cp.Variable((demand_num * path_num * wavelength_num), boolean=True)
  L = cp.Variable((edge_num * wavelength_num), boolean=True)
  if directionless_roadms:
    B = cp.Variable((demand_num*node_num*wavelength_num), boolean = True)
  F = cp.Variable((wavelength_num), boolean=True)
  Z = cp.Variable(1, integer=True)
  R = cp.Variable(1, integer=True)
  
  if preoccupied_wavelength_on_nodes is not None:
    B_previous = preoccupied_wavelength_on_nodes
  else:
    B_previous = np.zeros((demand_num *node_num*wavelength_num))

  if preoccupied_wavelength_on_links is not None:
    L_previous = preoccupied_wavelength_on_links
  else:
    L_previous = np.zeros((edge_num*wavelength_num))
  assignment_ones = np.ones((assignment_matrix_sparse.shape[0]))
  wavelength_ones = np.ones((wavelength_num))
  constraints = []
  constraints.append(assignment_matrix_sparse * X == assignment_ones) 
  constraints.append(link_occupation_matrix_sparse * X == L-L_previous) 
  constraints.append(L_previous <= L)
  constraints.append(general_occupation_matrix_sparse * L <= F) 
  if directionless_roadms:
    # Directionless ROADM constraints
    roadm_ones = np.ones((node_num*wavelength_num)) 
    constraints.append(roadm_occupation_matrix_sparse * X == B - B_previous) 
    constraints.append(roadm_single_usage_matrix_sparse * (B - B_previous) <= roadm_ones) 
    constraints.append(B_previous <= B)
  constraints.append(wavelength_ones * F == Z) 
  constraints.append(regen_number_matrix * X == R)

  print("======================================")
  problem = cp.Problem(cp.Minimize(Z*(network.alpha)+R*(1-network.alpha)), constraints) #+ (1-self.alpha)*R
  objective = problem.solve(verbose=False)
  total_wavelength_num = int(Z.value[0])
  print("ILP subroutine results: {} wavelengths and {} regenerators".format(total_wavelength_num, int(R.value[0])))

  # Rearrenge wavelengths so that index of used wavelengths be consequent
  # The indices of history should not be affected
  used_wavelengths_indicator = np.array(F.value)
  partial_sorted_wavelength_indices = used_wavelengths_indicator[history_window:].argsort()[::-1]+history_window
  sorted_wavelength_indices = np.arange(len(used_wavelengths_indicator))
  sorted_wavelength_indices[history_window:] = partial_sorted_wavelength_indices
  x_assignment = X.value.reshape(demand_num, path_num, -1)
  x_assignment = x_assignment[:,:,sorted_wavelength_indices]
  x_assignment = x_assignment[:,:, 0:total_wavelength_num]
  # print(B.value.reshape(demand_num, node_num, -1))
  # print(L.value.reshape(edge_num, -1))
  # print(np.matmul(roadm_type_matrix, L.value))

  node_wavelengths = [[] for _ in range(len(list(network.graph.nodes)))]
  used_wavelengths = [[] for _ in range(len(list(network.graph.edges)))]
  unused_wavelengths = [list(range(network.wavelength_num)) for _ in range(len(list(network.graph.edges)))]
  all_wavelengths = [available_wavelengths for _ in range(len(list(network.graph.edges)))]
  
  options_list = []
  for demand_id, demand in enumerate(demands):
    demand_assignment = x_assignment[demand_id]
    invalid_path_ids = list(range(path_num))
    option = (demand.ingress_node.index, demand.egress_node.index, demand.modulation, demand.protection_type, demand.cluster_id)
    for path_id, (main_inlist, protection_inlist) in enumerate(protected_path_list):
      for r in network.RegenOptionDict[option]:
        main_r_path, protection_r_path = r.main_option.path, r.protection_option.path
        if main_inlist == main_r_path and protection_inlist == protection_r_path:
          if path_id in invalid_path_ids:
            invalid_path_ids.remove(path_id)  # remove valid pathes from list of invalid pathes
    associated_assignment = np.where(demand_assignment == 1)
    associated_path_id = None
    associated_wavelength_id = None
    for p,w in zip(associated_assignment[0],associated_assignment[1]):
      if p not in invalid_path_ids:
        associated_path_id = p
        associated_wavelength_id = w
    if associated_path_id is None:
      print("ILP solver found invalid solution!")
      assert False

    main_path = protected_path_list[associated_path_id][0]
    protection_path = protected_path_list[associated_path_id][1]

    main_wavelength = available_wavelengths[associated_wavelength_id]
    protection_wavelength = available_wavelengths[associated_wavelength_id]

    main_modulation = demand.modulation
    protection_modulation = demand.modulation

    for r in network.RegenOptionDict[option]:
      main_r_path, protection_r_path = r.main_option.path, r.protection_option.path
      if main_path == main_r_path and protection_path == protection_r_path:
        main_segments = r.main_option.path_segments
        main_regen_nodes_index = r.main_option.regen_nodes_index
        protection_segments = r.protection_option.path_segments
        protection_regen_nodes_index = r.protection_option.regen_nodes_index

    use_this_wavelength = main_wavelength
    node_wavelengths[list(network.graph.nodes).index(demand.ingress_node.index)].append(use_this_wavelength)
    node_wavelengths[list(network.graph.nodes).index(demand.ingress_node.index)].sort()
    node_wavelengths[list(network.graph.nodes).index(demand.egress_node.index)].append(use_this_wavelength)
    node_wavelengths[list(network.graph.nodes).index(demand.egress_node.index)].sort()
    
    main_option = RegenOption(option, main_path, main_segments, main_wavelength, main_regen_nodes_index, True, main_modulation)
    protection_option = RegenOption(option, protection_path, protection_segments, protection_wavelength, protection_regen_nodes_index, True, protection_modulation)
    options_list.append(ProtectedRegenOption(main_option, protection_option))

    edge_indices = []
    for seg in (main_option.path_segments):
      for j in range(len(seg)-1):
        if unused_wavelengths[list(network.graph.edges).index((seg[j], seg[j+1]))]:
          edge_indices.append(list(network.graph.edges).index((seg[j], seg[j+1])))
          #### Reverse link
          edge_indices.append(list(network.graph.edges).index((seg[j+1], seg[j])))
        else:
          warnings.warn("ILP subroutine returns erroneous results!")
    for seg in (protection_option.path_segments):
      for j in range(len(seg)-1):
        if unused_wavelengths[list(network.graph.edges).index((seg[j], seg[j+1]))]:
          edge_indices.append(list(network.graph.edges).index((seg[j], seg[j+1])))
          #### Reverse link
          edge_indices.append(list(network.graph.edges).index((seg[j+1], seg[j])))
        else:
          warnings.warn("ILP subroutine returns erroneous results!")
    [used_wavelengths[i].append(use_this_wavelength) for i in edge_indices]
    [used_wavelengths[i].sort() for i in edge_indices]
    unused_wavelengths = [[w for w in all_wavelengths[j] if w not in used_wavelengths[j]] for j in range(len(used_wavelengths))]
  
  return options_list, objective, node_wavelengths, used_wavelengths, unused_wavelengths, total_wavelength_num
  # print(L.value.reshape(edge_num, wavelength_num))
  # print(X.value.reshape(demand_num, path_num, -1))

def solve_two_way_protected_windowed_ILP(network, history_wavelength_num = 4, demand_group_num = 6, max_new_wavelength_num = 6):
    indicator = 0
    start_wavelength = 0
    L_total = None # Shows which wavelength is occupied on which link
    B_total = None # Shows which wavelength is occupied on which node; Used for directionless ROADMs
    final_options_list = []
    history_wavelengths = []
    network.extractedLightpathlist = []
    network.node_wavelengths = [[] for _ in range(len(list(network.graph.nodes)))]
    network.used_wavelengths = [[] for _ in range(len(list(network.graph.edges)))]
    demand_number = len(network.demand_list)
    edge_num = len(network.graph.to_undirected().edges)
    node_num = len(network.graph.nodes)
    for indicator in range(math.ceil(demand_number/max_new_wavelength_num)):
      end_wavelength = start_wavelength+max_new_wavelength_num
      start_demand = indicator*demand_group_num
      end_demand = (indicator+1)*demand_group_num
      if end_demand > demand_number:
        end_demand = demand_number
      if end_wavelength - start_wavelength > end_demand - start_demand:
        end_wavelength = start_wavelength + end_demand - start_demand
      new_wavelengths = list(range(start_wavelength, end_wavelength))
      available_wavelengths = []
      available_wavelengths.extend(history_wavelengths)
      available_wavelengths.extend(new_wavelengths)

      demands = network.demand_list[start_demand: end_demand]
      L_previous = np.zeros((edge_num, len(available_wavelengths)))
      if L_total is not None:
        L_previous[:, 0:len(history_wavelengths)] = L_total[:, history_wavelengths]
      L_previous = L_previous.reshape(-1)

      B_previous = np.zeros((node_num, len(available_wavelengths)))
      if B_total is not None:
        B_previous[:, 0:len(history_wavelengths)] = B_total[:, history_wavelengths]
      B_previous = np.expand_dims(B_previous, axis=0)
      B_previous = np.repeat(B_previous, len(demands), axis = 0)
      B_previous = B_previous.reshape(-1)

      # Run windowed ILP subroitine
      options_list,_, node_wavelengths, used_wavelengths, _, subroutine_wavelength_num = ILP_2way_protected_solver_subroutine(network, available_wavelengths, demands, L_previous, B_previous, history_window = len(history_wavelengths))
      start_wavelength += subroutine_wavelength_num - len(history_wavelengths)
      # Gather the results
      [final_options_list.append(option) for option in options_list]

      for i in range(len(node_wavelengths)):
        [network.node_wavelengths[i].append(w) for w in node_wavelengths[i]]
        network.node_wavelengths[i] = list(set(network.node_wavelengths[i]))
        network.node_wavelengths[i].sort()

      B_total = np.zeros((node_num, start_wavelength)) 
      for node, wavelengths_on_node in enumerate(network.node_wavelengths):
        if network.node_list[node].roadm_type == "Directionless":
          B_total[node, wavelengths_on_node] = 1

      for i in range(len(list(network.graph.edges))):
        [network.used_wavelengths[i].append(w) for w in used_wavelengths[i]]
        network.used_wavelengths[i] = list(set(network.used_wavelengths[i]))
        network.used_wavelengths[i].sort()
      L_total = np.zeros((edge_num, start_wavelength)) # Link wavelength occupation matrix
      undirected_used_wavelengths = [[] for _ in range(len(list(network.graph.to_undirected().edges)))]
      for edge_index, edge in enumerate(network.graph.to_undirected().edges):
        directed_edge_index = list(network.graph.edges).index(edge)
        # print(directed_edge_index)
        undirected_used_wavelengths[edge_index] = network.used_wavelengths[directed_edge_index]
      # print(undirected_used_wavelengths)
      for link, wavelengths_on_link in enumerate(undirected_used_wavelengths):
        # print(wavelengths_on_link)
        L_total[link, wavelengths_on_link] = 1
      wavelengths_usage_on_links = np.sum(L_total, axis=0)
      sorted_occupied_wavelengths = sorted(range(len(wavelengths_usage_on_links)), key=lambda k: wavelengths_usage_on_links[k]) 
      if history_wavelength_num< len(sorted_occupied_wavelengths):
        history_wavelengths = sorted_occupied_wavelengths[0:history_wavelength_num]
      else:
        history_wavelengths = sorted_occupied_wavelengths[0:len(sorted_occupied_wavelengths)]

    all_wavelengths = [list(range(network.wavelength_num)) for _ in range(len(network.used_wavelengths))]
    network.unused_wavelengths = [[w for w in all_wavelengths[j] if w not in network.used_wavelengths[j]] for j in range(len(network.used_wavelengths))]
    
    for option, demand in zip(final_options_list, network.demand_list):
      demand.selected_regen_option = option
      network.extractedLightpathlist.append(ExtractedLightpath(option, demand, 
                                                            routed_type = demand.demand_type, modulation = demand.modulation))
    network.upper_bound = network.find_objective(network.used_wavelengths)
    return True


def LP_lower_bound_subroutine(network, available_wavelengths, demands,
                                         preoccupied_wavelength_on_links = None,
                                         preoccupied_wavelength_on_nodes = None, history_window = 0):
  if network.merging_demands:
    warnings.warn("The selected ILP subroutine is not capable of merging demands.")
    assert False
  modulation = 'QPSK'
  # Extract all of possible pathes (with protection) from RegenOptions
  protected_path_list = [] # list of all possible pathes  
  for option in network.RegenOptionDict.keys():
    if option[2] == modulation:
      for r in network.RegenOptionDict[option]:
        main_r, protect_r = r.main_option, r.protection_option
        protected_path = (main_r.path, protect_r.path)
        # regen_num = len(main_r.regen_nodes_index) + len(protect_r.regen_nodes_index)
        if protected_path not in protected_path_list:
          protected_path_list.append(protected_path)
          # regen_number_list.append(path_id, regen_num)
  # print(protected_path_list)
  wavelength_num = len(available_wavelengths)
  path_num = len(protected_path_list)
  demand_num = len(demands)
  G = network.graph.to_undirected()
  edge_num = len(G.edges)
  node_num = len(G.nodes)

  assignment_matrix = np.zeros((demand_num, demand_num, path_num, wavelength_num))
  for demand_id, demand in enumerate(demands):
    option = (demand.ingress_node.index, demand.egress_node.index, modulation, demand.protection_type, demand.cluster_id)
    for path_id, (main_inlist, protection_inlist) in enumerate(protected_path_list):
      for r in network.RegenOptionDict[option]:
        main_r_path, protection_r_path = r.main_option.path, r.protection_option.path
        if main_inlist == main_r_path and protection_inlist == protection_r_path:
          for w_id, w in enumerate(available_wavelengths):
            assignment_matrix[demand_id, demand_id, path_id, w_id] = 1
  assignment_matrix = assignment_matrix.reshape(demand_num, -1)          

  link_occupation_matrix = np.zeros((edge_num, wavelength_num, demand_num, path_num, wavelength_num))
  for demand_id, demand in enumerate(demands):
    option = (demand.ingress_node.index, demand.egress_node.index, modulation, demand.protection_type, demand.cluster_id)
    for path_id, (main_inlist, protection_inlist) in enumerate(protected_path_list):
      for r in network.RegenOptionDict[option]:
        main_r_path, protection_r_path = r.main_option.path, r.protection_option.path
        if main_inlist == main_r_path and protection_inlist == protection_r_path:
          for path in [main_r_path, protection_r_path]:
            for i,node in enumerate(path):
              if i < len(path)-1:
                if (node,path[i+1]) in list(G.edges):
                  edge_id = list(G.edges).index((node,path[i+1]))
                else:
                  edge_id = list(G.edges).index((path[i+1], node))
                for w_id, w in enumerate(available_wavelengths):
                  link_occupation_matrix[edge_id, w_id, demand_id, path_id, w_id] = 1
  link_occupation_matrix = link_occupation_matrix.reshape(edge_num*wavelength_num, -1)

  general_occupation_matrix = np.zeros((wavelength_num, edge_num, wavelength_num))/edge_num
  for w_id, w in enumerate(available_wavelengths):
    for edge_id, edge in enumerate(G.edges):
      general_occupation_matrix[w_id, edge_id, w_id] = 1
  general_occupation_matrix = general_occupation_matrix.reshape(wavelength_num, -1)/edge_num

  regen_number_matrix = np.zeros((demand_num, path_num, wavelength_num))
  for demand_id, demand in enumerate(demands):
    for path_id, (main_inlist, protection_inlist) in enumerate(protected_path_list):
      for r in network.RegenOptionDict[option]:
        main_r_path, protection_r_path = r.main_option.path, r.protection_option.path
        if main_inlist == main_r_path and protection_inlist == protection_r_path:
          regen_number = len(r.main_option.regen_nodes_index)+len(r.protection_option.regen_nodes_index)
          for w_id, w in enumerate(available_wavelengths): 
            regen_number_matrix[demand_id, path_id, w_id] = regen_number
  regen_number_matrix = regen_number_matrix.reshape(-1)

  roadm_occupation_matrix = np.zeros((demand_num, node_num, wavelength_num, demand_num, path_num, wavelength_num))
  directionless_roadms = False
  for demand_id, demand in enumerate(demands):
    option = (demand.ingress_node.index, demand.egress_node.index, modulation, demand.protection_type, demand.cluster_id)
    for node in [demand.ingress_node, demand.egress_node]:
      if node.roadm_type == "Directionless":
        directionless_roadms = True
        for path_id, (main_inlist, protection_inlist) in enumerate(protected_path_list):
          for r in network.RegenOptionDict[option]:
            main_r_path, protection_r_path = r.main_option.path, r.protection_option.path
            if main_inlist == main_r_path and protection_inlist == protection_r_path:
              for w_id, w in enumerate(available_wavelengths):
                n_id = network.node_index_list.index(node.index)  # node_list and node_index_list should have same ordering
                roadm_occupation_matrix[demand_id, n_id, w_id, demand_id, path_id, w_id] = 1
  roadm_occupation_matrix = roadm_occupation_matrix.reshape(demand_num*node_num*wavelength_num, -1)

  if directionless_roadms:
    roadm_single_usage_matrix = np.zeros((node_num, wavelength_num, demand_num, node_num, wavelength_num))
    for n_id, node in enumerate(network.node_list):
      if node.roadm_type == "Directionless":
        for demand_id, demand in enumerate(demands):
          for w_id, w in enumerate(available_wavelengths):
            roadm_single_usage_matrix[n_id, w_id, demand_id, n_id, w_id] = 1
    roadm_single_usage_matrix = roadm_single_usage_matrix.reshape(node_num*wavelength_num, -1)

  X = cp.Variable((demand_num * path_num * wavelength_num))
  L = cp.Variable((edge_num * wavelength_num))
  if directionless_roadms:
    B = cp.Variable((demand_num*node_num*wavelength_num))
  F = cp.Variable((wavelength_num), boolean=True)
  Z = cp.Variable(1)
  R = cp.Variable(1)
  
  if preoccupied_wavelength_on_nodes is not None:
    B_previous = preoccupied_wavelength_on_nodes
  else:
    B_previous = np.zeros((demand_num *node_num*wavelength_num))

  if preoccupied_wavelength_on_links is not None:
    L_previous = preoccupied_wavelength_on_links
  else:
    L_previous = np.zeros((edge_num*wavelength_num))
  assignment_ones = np.ones((assignment_matrix.shape[0]))
  wavelength_ones = np.ones((wavelength_num))
  L_upper_ones = np.ones((edge_num * wavelength_num))
  L_lower_zeros = np.zeros((edge_num * wavelength_num))
  F_upper_ones = np.ones((wavelength_num))
  F_lower_zeros = np.zeros((wavelength_num))
  if directionless_roadms:
    B_upper_ones = np.ones((demand_num*node_num*wavelength_num))
    B_lower_zeros = np.zeros((demand_num*node_num*wavelength_num))
  X_upper_ones = np.ones((demand_num * path_num * wavelength_num))
  X_lower_zeros = np.zeros((demand_num * path_num * wavelength_num))
  constraints = []
  constraints.append(L <= L_upper_ones)
  constraints.append(L_lower_zeros <= L)
  constraints.append(F <= F_upper_ones)
  constraints.append(F_lower_zeros <= F)
  if directionless_roadms:
    constraints.append(B_lower_zeros <= B)
    constraints.append(B <= B_upper_ones)
  constraints.append(X <= X_upper_ones)
  constraints.append(X_lower_zeros <= X)
  constraints.append(assignment_matrix * X == assignment_ones) 
  constraints.append(link_occupation_matrix * X == L-L_previous) 
  constraints.append(L_previous <= L)
  constraints.append(general_occupation_matrix * L <= F) 
  if directionless_roadms:
    # Directionless ROADM constraints
    roadm_ones = np.ones((node_num*wavelength_num)) 
    constraints.append(roadm_occupation_matrix * X == B - B_previous) 
    constraints.append(roadm_single_usage_matrix * (B - B_previous) <= roadm_ones) 
    constraints.append(B_previous <= B)
  constraints.append(wavelength_ones * F == Z) 
  constraints.append(regen_number_matrix * X == R)

  print("======================================")
  problem = cp.Problem(cp.Minimize(Z*(network.alpha)+R*(1-network.alpha)), constraints) #+ (1-self.alpha)*R
  objective = problem.solve(verbose=False)
  total_wavelength_num = int(Z.value[0])
  print("LP lower-bound results: {} wavelengths and {} regenerators".format(total_wavelength_num, int(R.value[0])))

  # Rearrenge wavelengths so that index of used wavelengths be consequent
  # The indices of history should not be affected
  # used_wavelengths_indicator = np.array(F.value)
  # partial_sorted_wavelength_indices = used_wavelengths_indicator[history_window:].argsort()[::-1]+history_window
  # sorted_wavelength_indices = np.arange(len(used_wavelengths_indicator))
  # sorted_wavelength_indices[history_window:] = partial_sorted_wavelength_indices
  # x_assignment = X.value.reshape(demand_num, path_num, -1)
  # x_assignment = x_assignment[:,:,sorted_wavelength_indices]
  # x_assignment = x_assignment[:,:, 0:total_wavelength_num]
  # print(B.value.reshape(demand_num, node_num, -1))
  # print(L.value.reshape(edge_num, -1))
  # print(F.value)
  # print(np.matmul(roadm_type_matrix, L.value))


def ILP_lower_bound_subroutine(network, available_wavelengths, demands,
                                         preoccupied_wavelength_on_links = None,
                                         preoccupied_wavelength_on_nodes = None, history_window = 0):
  if network.merging_demands:
    warnings.warn("The selected ILP subroutine is not capable of merging demands.")
    assert False
  modulation = 'QPSK'
  # Extract all of possible pathes (with protection) from RegenOptions
  protected_path_list = [] # list of all possible pathes  
  for option in network.RegenOptionDict.keys():
    if option[2] == modulation:
      for r in network.RegenOptionDict[option]:
        main_r, protect_r = r.main_option, r.protection_option
        protected_path = (main_r.path, protect_r.path)
        # regen_num = len(main_r.regen_nodes_index) + len(protect_r.regen_nodes_index)
        if protected_path not in protected_path_list:
          protected_path_list.append(protected_path)
          # regen_number_list.append(path_id, regen_num)
  # print(protected_path_list)
  wavelength_num = len(available_wavelengths)
  path_num = len(protected_path_list)
  demand_num = len(demands)
  G = network.graph.to_undirected()
  edge_num = len(G.edges)
  node_num = len(G.nodes)

  assignment_matrix = np.zeros((demand_num, demand_num, path_num))
  for demand_id, demand in enumerate(demands):
    option = (demand.ingress_node.index, demand.egress_node.index, modulation, demand.protection_type, demand.cluster_id)
    for path_id, (main_inlist, protection_inlist) in enumerate(protected_path_list):
      for r in network.RegenOptionDict[option]:
        main_r_path, protection_r_path = r.main_option.path, r.protection_option.path
        if main_inlist == main_r_path and protection_inlist == protection_r_path:
          assignment_matrix[demand_id, demand_id, path_id] = 1
  assignment_matrix = assignment_matrix.reshape(demand_num, -1)          

  link_lower_bound_matrix = np.zeros((edge_num, demand_num, path_num))
  for demand_id, demand in enumerate(demands):
    option = (demand.ingress_node.index, demand.egress_node.index, modulation, demand.protection_type, demand.cluster_id)
    for path_id, (main_inlist, protection_inlist) in enumerate(protected_path_list):
      for r in network.RegenOptionDict[option]:
        main_r_path, protection_r_path = r.main_option.path, r.protection_option.path
        if main_inlist == main_r_path and protection_inlist == protection_r_path:
          for path in [main_r_path, protection_r_path]:
            for i,node in enumerate(path):
              if i < len(path)-1:
                if (node,path[i+1]) in list(G.edges):
                  edge_id = list(G.edges).index((node,path[i+1]))
                else:
                  edge_id = list(G.edges).index((path[i+1], node))
                link_lower_bound_matrix[edge_id, demand_id, path_id] = 1
  link_lower_bound_matrix = link_lower_bound_matrix.reshape(edge_num, -1)

  regen_number_matrix = np.zeros((demand_num, path_num))
  for demand_id, demand in enumerate(demands):
    for path_id, (main_inlist, protection_inlist) in enumerate(protected_path_list):
      for r in network.RegenOptionDict[option]:
        main_r_path, protection_r_path = r.main_option.path, r.protection_option.path
        if main_inlist == main_r_path and protection_inlist == protection_r_path:
          regen_number = len(r.main_option.regen_nodes_index)+len(r.protection_option.regen_nodes_index)
          regen_number_matrix[demand_id, path_id] = regen_number
  regen_number_matrix = regen_number_matrix.reshape(-1)

  X = cp.Variable((demand_num * path_num), boolean=True)
  Z = cp.Variable(1)
  R = cp.Variable(1)
  
  assignment_ones = np.ones((assignment_matrix.shape[0]))
  # X_upper_ones = np.ones((demand_num * path_num * wavelength_num))
  # X_lower_zeros = np.zeros((demand_num * path_num * wavelength_num))
  edge_ones = np.ones(edge_num)
  constraints = []
  # constraints.append(X <= X_upper_ones)
  # constraints.append(X_lower_zeros <= X)
  constraints.append(assignment_matrix * X == assignment_ones) 
  constraints.append(regen_number_matrix * X == R)
  constraints.append(link_lower_bound_matrix*X <= Z*edge_ones)

  print("======================================")
  problem = cp.Problem(cp.Minimize(Z*(network.alpha)+R*(1-network.alpha)), constraints) #+ (1-self.alpha)*R
  objective = problem.solve(verbose=False)
  total_wavelength_num = int(Z.value[0])
  print("ILP lower-bound results: {} wavelengths and {} regenerators".format(total_wavelength_num, int(R.value[0])))


