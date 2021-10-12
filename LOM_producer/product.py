from LOM_producer.NodeStructure import Nodestructureservices
from LOM_producer.NodeArchitecture import NodeArch
from grooming.Algorithm.id_generator import arashId, id_gen
from grooming.schemas import GroomingDBOut, GroomingResult
from physical_topology.schemas import PhysicalTopologyDB
from rwa.schemas import RWALightpathsOutput

def LOM_productioon(    device:GroomingDBOut, 
                        RWAres:RWALightpathsOutput, 
                        Physical_topology:PhysicalTopologyDB, 
                        grooming_res:GroomingResult, 
                        test=False):
    ArashId = arashId()
    if test == True:
        def uuid(): return id_gen(ArashId=ArashId, test=True)
    else:
        def uuid(): return id_gen(ArashId=ArashId, test=False)
    
    (NodeArch1, device_final, grooming_res) = Nodestructureservices(
            device, Physical_topology, grooming_res, state=None, percentage=[80, 90], uuid=uuid)
    
    Structure, Structure2, device_dict,LOMn = NodeArch(  Node_Structure = NodeArch1, device_dict_in= device_final, 
                                                                Physical_topology=Physical_topology, LightPath=RWAres, state=None, percentage=[90,100], uuid=uuid)
    return LOMn