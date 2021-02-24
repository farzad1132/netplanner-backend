import networkx as nx


class ROADM(object):
    def __init__(self, colorless, directionless, contentionless):
        self.colorless = colorless
        self.directionless = directionless
        self.contentionless = contentionless
    
    @classmethod
    def CDC_ROADM(cls):
        return cls(colorless=True, directionless=True, contentionless=True)

    def __str__(self):
        return f"ROADM- colorless:{self.colorless}, directionless:{self.directionless}, contentionless:{self.contentionless}"

class Node(object):
  """
  Stores node parameters for the network. 
  location: nodes will be displayed on this location
  index: node name
  """
  def __init__(self, index, location, roadm_type = "CDC", roadm=ROADM.CDC_ROADM()):
    self.roadm = roadm
    self.roadm_type = roadm_type  # Directionless/ CDC # TODO: roadm_type WILL BE DEPRICATED
    if self.roadm_type == "Directionless":
        self.roadm.contentionless = False
    self.location = location
    self.index = index
    
  def __str__(self):
    #return "Node {} @ position {}".format(self.index, self.location)
    return "Node {}".format(self.index)
    
  def get_node_position(self):
    return self.location
    
  
  
class Link(object):
  """
  Stores link parameters for the network. 
  Links are directional.
  in_node: Input node
  out_node: Output node
  distance: Will be used by k-shortest path algorithm
  """
  def __init__(self, in_node, out_node, distance, loss_db, fiber_config, special=False, capacity=1):
    self.in_node = in_node
    self.out_node = out_node
    #self.is_directional = is_directional
    self.capacity = capacity
    self.special = special
    self.distance_list = []
    if not special:
      self.distance = distance
      self.config = fiber_config.copy()
      self.config['alpha_Np'] = (loss_db/1000)/ 8.685889638
      self.config['alpha_db'] = loss_db
    else:
      # we have several fibers concatenated
      self.distance_list = distance
      self.distance = 0
      self.config = []
      for i, config in enumerate(fiber_config):
        self.distance += distance[i]
        new_config = config.copy()
        new_config['alpha_Np'] = (loss_db[i]/1000)/ 8.685889638
        new_config['alpha_db'] = loss_db[i]
        self.config.append(new_config)
    #self.used_wavelengths = []
    
  def __str__(self):
    return "Directional link between {} and {}".format(self.in_node, self.out_node)
    
class Cluster(object):
  def __init__(self, gateway, subnode_list, Id):
    self.gateway = gateway
    self.subnode_list = subnode_list
    self.Id = Id
    self.graph = None
    
class Demand(object):
  """
  Each memeber of this class is a demand to be routed in the network
  ingress_node: Input node for a Demand
  egress_node: Destination of the Demand


  selected_option: Will be set after running the routing algorithm
  demand_options: An OptionsForDemand object which stores a list of valid RoutnigOptions
  path_list: List of valid pathes
  """
  def __init__(self, ingress_node, egress_node, modulation = '8QAM',demand_type =None,
              protection_type = "1+1_NodeDisjoint", cluster_id=0, previous_id = None,
              has_restoration=True, restoration_type="AdvJointSame", protection_restoration=False, capacity = 1):
    self.ingress_node = ingress_node
    self.egress_node = egress_node
    self.capacity = capacity
    self.modulation = modulation
    self.selected_regen_option = None # Will be updated after solving the problem
    self.demand_type =demand_type 
    self.protection_type = protection_type # "1+1_NodeDisjoint" and "NoProtection"
    self.cluster_id = cluster_id
    self.previous_id = previous_id

    self.restoration_type = restoration_type # "AdvJointSame" and "JointSame"
    self.has_restoration = has_restoration
    if not restoration_type:
      self.has_restoration = False
    self.protection_restoration = protection_restoration
    
    self.demand_options = None # Stores valid lightpathes (RegenOptionsForDemand)
    self.path_list = [] # Stores valid pathes
    self.protected_path_list = []
    self.forbidden_path_list = []
    self.must_go_path = []
    
  def __str__(self):
    if self.selected_regen_option:
      #return "ROUTED demand with capacity {} from {} to {}".format(self.capacity, self.ingress_node, self.egress_node)
      return "ROUTED demand from {} to {} on cluster {} restoration:{}".format(self.ingress_node, self.egress_node, self.cluster_id, self.has_restoration)
    else:
      #return "A demand with capacity {} from {} to {}".format(self.capacity, self.ingress_node, self.egress_node)
      return "A {} demand from {} to {} on cluster {} restoration:{}".format(self.demand_type, self.ingress_node, self.egress_node, self.cluster_id, self.has_restoration)
  
class RegenOption(object):
  """
  Each memeber of this class should be a valid regeneration option
  path_segments: is a list of lists where each list is a segment
                 of a path
  path_wavelengths: is a list of wavelengths on each segment
  path_modulation: will be modulation type
  """
  def __init__(self, option, path, path_segments, path_wavelengths, regen_nodes_index = None,
              option_is_valid=True, path_modulation= None, failed_link = None, second_failed_link = "all"):
    self.option = option  #option = (ingress_node, egress_node, modulation)
    self.path = path
    self.path_segments = path_segments
    self.path_wavelengths = path_wavelengths
    self.regen_nodes_index = regen_nodes_index
    self.option_is_valid = option_is_valid
    self.path_modulation = path_modulation
    self.failed_link = failed_link
    self.second_failed_link = second_failed_link

    self.shared_regen_nodes_id={}
    for regen_node in self.regen_nodes_index:
        self.shared_regen_nodes_id[regen_node] = 0
  def __str__(self):
    # ingress_node, egress_node, modulation, protection, cluster_id = self.option
    return "w {}| {} | path {} | regens: {}".format(self.path_wavelengths, self.path_modulation, self.path, self.regen_nodes_index)

class ProtectedRegenOption(object):
  def __init__(self, main_option, protection_option):
    self.main_option = main_option
    self.protection_option = protection_option
    self.restoration_option_list = None
    self.protection_restoration_option_list = None

  def __str__(self):
    if self.main_option.option[3] == "NoProtection":
      if self.restoration_option_list:
        text = f"Main:      {self.main_option}\n"
        text += "-------------------- Restoration for Working links --------------------\n"
        for link_id, restoration_option in enumerate(self.restoration_option_list):
            text += f"Restoration ({self.main_option.path[link_id]},{self.main_option.path[link_id + 1]}):      {restoration_option}\n"
        if self.protection_restoration_option_list:
            text += "------------------ Restoration for Protection links ------------------\n"
            for link_id, restoration_option in enumerate(self.protection_restoration_option_list):
                text += f"Restoration ({self.protection_option.path[link_id]},{self.protection_option.path[link_id + 1]}):      {restoration_option}\n"
        return text
      else:
          return f"Main:      {self.main_option}\n"
    else:
      if self.restoration_option_list:
          text = f"Main:      {self.main_option}\nProtection:{self.protection_option}\n"
          text += "-------------------- Restoration for Working links --------------------\n"
          for link_id, restoration_option in enumerate(self.restoration_option_list):
              if isinstance(restoration_option, RegenOption):
                  text += f"Restoration ({self.main_option.path[link_id]},{self.main_option.path[link_id + 1]}):      {restoration_option}\n"
              elif restoration_option is not None:
                  for second_option in restoration_option:
                      if second_option is not None:
                          text += f"Restoration {second_option.failed_link},{second_option.second_failed_link}:      {second_option}\n"
              else:
                  text += f"Restoration ({self.main_option.path[link_id]},{self.main_option.path[link_id + 1]}):      {restoration_option}\n"
          if self.protection_restoration_option_list:
              text += "------------------ Restoration for Protection links ------------------\n"
              for link_id, restoration_option in enumerate(self.protection_restoration_option_list):
                  text += f"Restoration ({self.protection_option.path[link_id]},{self.protection_option.path[link_id + 1]}):      {restoration_option}\n"
          return text
      else:
          return f"Main:      {self.main_option}\nProtection:{self.protection_option}\n"

class ExtractedLightpath(object):
    def __init__(self, protectedRegenOption, demand, routed_type, modulation):
        self.selected_regen_option = protectedRegenOption
        self.demand = demand
        self.routed_type = routed_type
        self.modulation = modulation
        self.protection_length = 0
        self.main_length = 0
        self.protection_osnr = None
        self.main_osnr = None

        self.restoration_osnrs = []
        self.restoration_lengths = []
        self.restoration_paths = []
        self.restoration_regens = []
        self.restoration_failed_links = []
        
    def __str__(self):
      if self.demand.protection_type == "NoProtection":
          return "#######################################################################\n" + "Extracting a {} lightpath ({}) from {} to {} with No protection\n{}Main:       length {} | OSNR  {}".format(
              self.routed_type, self.modulation, self.demand.ingress_node, self.demand.egress_node,
              self.selected_regen_option, self.main_length, self.main_osnr)
      elif self.demand.protection_type == "1+1_NodeDisjoint":
          return "#######################################################################\n" + "Extracting a {} lightpath ({}) from {} to {}  with 1+1 Node Disjoint protection\n{}Main:       length {} | OSNR  {}\nProtection: length {} | OSNR {}".format(
              self.routed_type, self.modulation, self.demand.ingress_node, self.demand.egress_node,
              self.selected_regen_option, self.main_length, self.main_osnr, self.protection_length,
              self.protection_osnr)
      elif self.demand.protection_type == "1+1_LinkDisjoint":
          return "#######################################################################\n" + "Extracting a {} lightpath ({}) from {} to {}  with 1+1 Link Disjoint protection\n{}Main:       length {} | OSNR  {}\nProtection: length {} | OSNR {}".format(
              self.routed_type, self.modulation, self.demand.ingress_node, self.demand.egress_node,
              self.selected_regen_option, self.main_length, self.main_osnr, self.protection_length,
              self.protection_osnr)

class RegenOptionsForDemand(object):
  """
  Stores a list of valid options for a Demand.
  """
  def __init__(self, demand, regen_option_list):
    self.regen_option_list = regen_option_list
    self.demand = demand

class Collision(object):
    def __init__(self, link, wavelength):
        self.link = link
        self.wavelength = wavelength
        self.lightpath_list = []
        self.option_type = []

    def add_collision(self, lightpath, option_type):
        self.lightpath_list.append(lightpath)
        self.option_type.append(option_type)

    def __str__(self):
        text = "!!!!!!!!---------------COLLISION----------------!!!!!!!!\n"
        text += f"           {self.wavelength},  {self.link}, {self.option_type} \n\n"
        for lightpath in self.lightpath_list:
            text += f"{lightpath}\n"
        return text