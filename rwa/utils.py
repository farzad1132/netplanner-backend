from physical_topology.schemas import PhysicalTopologySchema
from rwa.schemas import RWAResult, RWAGeneralInfo

def generate_RWA_general_info(physical_topology: PhysicalTopologySchema, rwa_result:RWAResult)-> RWAGeneralInfo:
    node_state = {}
    link_state = {}
    wavelength_state = {}

    for node in physical_topology["nodes"]:
        node_state[node] = {
            "node": node,
            "wavelengths": []
        }
    for link in physical_topology["links"]:
        link = link["source"]+ "-" + link["destination"]
        link_state[link] = {
            "source": link["source"],
            "destination": link["destination"],
            "wavelengths": []
        }

    for lightpath in rwa_result[lightpaths].values():
        working_info = lightpath["routing_info"]["working"]
        working_segment = 0

        for working_node, node_id in enumerate(working_info["path"]):
            wavelength = working_info["wavelength"][working_segment]
            if wavelength not in wavelength_state: 
                wavelength_state[wavelength] = {
                    "wavelength": wavelength,
                    "links": [],
                    "signal_nodes": [],
                    "pass_nodes": []
                }
            if working_node in working_info["regenerators"] or working_node in [lightpath["source"], lightpath["destination"]]:
                wavelength_state[wavelength]["signal_nodes"].append(working_node)
            else:
                wavelength_state[wavelength]["pass_nodes"].append(working_node)
            node_state[working_node]["wavelengths"].append(wavelength)

            if node_id < len(working_info["path"])-1:
                link = working_info["path"][node_id] + "-" + working_info["path"][node_id+1]
                if link in link_state:
                    link_info = {
                        "source": working_info["path"][node_id],
                        "destination": working_info["path"][node_id+1]
                    }
                else:
                    link = working_info["path"][node_id+1] + "-" + working_info["path"][node_id]
                    link_info = {
                        "source": working_info["path"][node_id+1],
                        "destination": working_info["path"][node_id]
                    }
                link_state[link]["wavelengths"].append(wavelength)
                wavelength_state[wavelength]["links"].append(link_info)
    general_info_dict = {
        'link_state': link_state,
        'node_state': node_state,
        'wavelength_state': wavelength_state,
    }
    general_info = RWAGeneralInfo(**general_info_dict)
    return general_info
                
