import networkx as nx
import numpy as np
import scipy.constants as const
from itertools import islice
import math 
import warnings

def gen_restoration_on_link_for_demand(network, failed_link, selected_regen_option, k):
    import math
    from rwa.algorithm.components import RegenOption, ProtectedRegenOption
    import itertools

    option = selected_regen_option.main_option.option
    ingress_node, egress_node, modulation, protection_type, cluster_id = option

    G = network.graph.copy()

    #create auxiliary graph 
    if cluster_id == 0:
        G = network.graph.copy()
    else:
        G = network.cluster_dict[cluster_id].graph.copy()

    G.remove_edge(failed_link[0], failed_link[1])
    G.remove_edge(failed_link[1], failed_link[0])
    if protection_type == "1+1_NodeDisjoint":
        protection_path = selected_regen_option.protection_option.path
        for node_id in range(len(protection_path) - 1):
            if (protection_path[node_id], protection_path[node_id + 1]) in G.edges:
                G.remove_edge(protection_path[node_id], protection_path[node_id + 1])
            if (protection_path[node_id + 1], protection_path[node_id]) in G.edges:
                G.remove_edge(protection_path[node_id + 1], protection_path[node_id])
    try:
        paths = k_shortest_paths(G, ingress_node, egress_node, k, "distance")
    except:
        warnings.warn(f"No path between {ingress_node} and {egress_node}")
        return None
    if not paths:
        return None
    regen_option_list = []
    # print(paths)
    for restoration_path in paths:
        # print(restoration_path)
        if len(restoration_path) > 2:
            trunc_restoration_path = restoration_path[1:-1]
        else:
            trunc_restoration_path = []
        current_restoration_path_length = get_path_length(G, restoration_path, weight='distance')
        max_num = math.floor(current_restoration_path_length / min(network.reach_options.values())) + 1
        min_req_regens = 0
        limited_max_regens = max_num
        restoration_regens = []
        for L in range(min_req_regens, min(limited_max_regens + 1, len(restoration_path) - 1)):
            for restoration_regen in itertools.combinations(trunc_restoration_path, L):
                option_is_valid, segments, regen_nodes, path_modulation = network.check_regen_path_fixed_modulation(
                    option, restoration_regen, restoration_path)
                # print(option_is_valid, restoration_path)
                if option_is_valid:
                    regen_wavelengths = []
                    restoration_option = RegenOption(option, restoration_path, segments, regen_wavelengths,
                                                     regen_nodes, option_is_valid, path_modulation, failed_link)
                    regen_option_list.append(restoration_option)
    return regen_option_list


def find_worst_snr(network):
    if network.extractedLightpathlist:
        worst_snr_value = network.extractedLightpathlist[0].main_osnr[0]
        for lightpath in network.extractedLightpathlist:
            for snr in lightpath.main_osnr:
                if worst_snr_value > snr:
                  worst_snr_value = snr
            for snr in lightpath.protection_osnr:
                if worst_snr_value > snr:
                  worst_snr_value = snr
        return worst_snr_value
    else:
        return None


def get_path_length(G, path, weight='distance'):
    """
    Returns the length of a path.
    path: A list of nodes.
    G: A networkx.graph object
    """
    length = 0
    if len(path) > 1:
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            length += G.edges[u,v].get(weight, 1)
    return length 

def k_shortest_paths(G, source, target, k, weight=None):
  """
  Run a k-shortest path algorithm from source node to target node 
  on networkx.graph object G using weights.
  """
  return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))

    
def find_ASE_noise(config, modulation = 'QPSK'):
  G = config['booster_gain']
  Bs = config['Bs'][modulation]
  nu = config['nu']
  nsp = config['nsp']
  h = const.Planck
  return Bs * 2 * (G-1) * h * nu * nsp

def find_ASE_center_noise(config, path, modulation = 'QPSK'):
  G = config['inner_loss']
  Bs = config['Bs'][modulation]
  nu = config['nu']
  nsp = config['nsp']
  h = const.Planck
  return Bs * 2 * (G-1) * h * nu * nsp *len(path)

def ign_osnr(length, config, used_wavelengths, modulation = 'QPSK'):
  Ls = config['Ls']
  Ns = math.ceil(length/Ls)
  Leff = [(1-math.exp(-2*config['alpha_Np']*config['Ls']))/(2*config['alpha_Np']) for _ in range(Ns-1)]
  Leff.append((1-math.exp(-2*config['alpha_Np']*(length - (Ns-1)*config['Ls'])))/(2*config['alpha_Np']))
  Leff_a = 1/(2*config['alpha_Np'])
  alpha_Np = config['alpha_Np'] 
  Rs = config['baud_rate'][modulation]
  deltaF = config['deltaF']
  Nch = config['Nch']
  gamma = config['gamma']
  beta2 = config['beta2']
  pi = const.pi
  Bs = config['Bs'][modulation]
  nu = config['nu']
  nsp = config['nsp']
  h = const.Planck
  Pch = config['Pch']
  
  Gch = np.zeros(Nch)
  G = Pch/Rs
  for i in used_wavelengths:
    Gch[i] = G 
  
  fch = []
  freq = nu
  for i in range(Nch):
    fch.append(freq)
    freq += deltaF
    
  def delta(n,i):
    if n == i:
      return 1
    else:
      return 0
    
  def psi(n,i):
    if n==i:
      return np.arcsinh(pi**2/2 * Leff_a * beta2 * Bs**2) / (2*pi * Leff_a * beta2)
    else:
      psi_1  = np.arcsinh(pi**2 * Leff_a * beta2 * (fch[n] - fch [i] + Bs/2)*Bs) / (4*pi * Leff_a * beta2)
      psi_2  = np.arcsinh(pi**2 * Leff_a * beta2 * (fch[n] - fch [i] - Bs/2)*Bs) / (4*pi * Leff_a * beta2)
      return psi_1-psi_2
  
  GNLI = []
  for i in range(Nch):
    summation = 0
    for ns in range(Ns):
      aux = 1 
      aux_sum = 0
      # Uncomment if attenuation is not compensated completely
      #for k in range(ns-1):
      #  aux *= Gamma**3 * math.exp(-6*alpha_NP*Ls)
      #for k in range(ns-1, Ns):
      #  aux *= Gamma * math.exp(-2*alpha_NP*Ls)
      aux_2 = 0
      for n in range(Nch):
        #print(psi(n,i))
        if (Gch[n]!=0 and Gch[i]!=0):
          aux_2 += Gch[n]**2 * Gch[i] * (2-delta(n,i)) * psi(n,i)
          
      summation += Leff[ns]**2 * aux * aux_2
      
 
    GNLI.append(16/27 * gamma**2 * summation * Rs)
  
  
  #print(GNLI)
  ASE = Bs*2*(math.exp(2*alpha_Np*Ls)-1)*h*nu*nsp*(Ns-1)+Bs*2*(math.exp(2*alpha_Np*(length-(Ns-1)*Ls))-1)*h*nu*nsp # ns-span
  
  OSNR_dB = []
  for i in range(Nch):
    NLI = GNLI[i]
    if Gch[i]==0:
      OSNR_dB.append(None)
    else:
      OSNR = Gch[i]*Rs/((ASE+NLI))
      OSNR_db = 10 * math.log10(OSNR)
      OSNR_dB.append(OSNR_db)
  return OSNR_dB, GNLI, ASE
        
def approximate_osnr(length, config, modulation = 'QPSK'):
  Ls = config['Ls']
  Ns = math.ceil(length/Ls)
  Leff = (1-math.exp(-2*config['alpha_Np']*config['Ls']))/(2*config['alpha_Np'])
  Leff_a = 1/(2*config['alpha_Np'])
  alpha_Np = config['alpha_Np'] 
  Rs = config['baud_rate'][modulation]
  deltaF = config['deltaF']
  Nch = config['Nch']
  gamma = config['gamma']
  beta2 = config['beta2']
  pi = const.pi
  Pch = config['Pch']
  
  eta = 8/27 * gamma**2 * Leff**2/ (pi * beta2 * Rs**2 * Leff_a) * np.arcsinh(pi**2/2 * beta2 * Leff_a * Rs**2 * Nch**(2*Rs/deltaF) )
  NLI = eta * Pch**3 # 1-span
 
  Bs = config['Bs'][modulation]
  nu = config['nu']
  nsp = config['nsp']
  h = const.Planck
  ASE = Bs * 2 * (math.exp(2*alpha_Np*Ls)-1) * h * nu * nsp # 1-span
  
  OSNR = Pch/((ASE+NLI)*Ns)
  OSNR_db = 10 * math.log10(OSNR)
  return(OSNR_db)


#print(ign_osnr(90*1e3, CONFIG, [1,2,3], modulation = 'BPSK'))