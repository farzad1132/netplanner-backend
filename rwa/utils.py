from physical_topology.schemas import PhysicalTopologySchema
from rwa.schemas import RWAResult, RWAGeneralInfo
import json

def generate_RWA_general_info(physical_topology: PhysicalTopologySchema, rwa_result:RWAResult)-> RWAGeneralInfo:
    # for working path
    node_state = {}
    link_state = {}
    wavelength_state = {}
    lightpath_state = {}
    total_lambda_link = 0
    average_lambda_capacity_usage = 0

    for node in physical_topology["nodes"]:
        node_state[node["name"]] = {
            "node": node["name"],
            "wavelengths": []
        }
    for link in physical_topology["links"]:
        link_text = link["source"]+ "-" + link["destination"]
        link_state[link_text] = {
            "source": link["source"],
            "destination": link["destination"],
            "wavelengths": []
        }
    
    for lightpath in rwa_result["lightpaths"].values():
        working_info = lightpath["routing_info"]["working"]
        lightpath_links = len(working_info["path"])
        lightpath_state[lightpath["id"]]= {
            'lambda_link': lightpath_links
        }
        total_lambda_link += lightpath_links
        average_lambda_capacity_usage += lightpath_links * lightpath["capacity"]/100
        
        working_segment = 0

        for node_id, working_node in enumerate(working_info["path"]):
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

    average_lambda_capacity_usage = average_lambda_capacity_usage/ total_lambda_link   
    general_info_dict = {}
    general_info_dict['working'] = {
        'link_state': link_state,
        'node_state': node_state,
        'wavelength_state': wavelength_state,
        'lightpath_state': lightpath_state,
        'total_lambda_link': total_lambda_link,
        'average_lambda_capacity_usage': average_lambda_capacity_usage
    }
    general_info = RWAGeneralInfo(**general_info_dict)
    return general_info
                
    