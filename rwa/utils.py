from physical_topology.schemas import PhysicalTopologySchema
from rwa.schemas import RWAResult, RWAGeneralInfo
import json

def generate_RWA_general_info(physical_topology: PhysicalTopologySchema, rwa_result:RWAResult)-> RWAGeneralInfo:
    
    
    def extract_path_general_info(routing_path, node_state, link_state, wavelength_state, lightpath_state,
                                  total_lambda_link, average_lambda_capacity_usage):
        if routing_path is not None:
            lightpath_links = len(routing_path["path"])-1
            lightpath_state[lightpath["id"]]= {
                'lambda_link': lightpath_links
            }
            total_lambda_link += lightpath_links
            average_lambda_capacity_usage += lightpath_links * lightpath["capacity"]/100
            
            path_segment = 0

            for node_id, path_node in enumerate(routing_path["path"]):
                wavelength = routing_path["wavelength"][path_segment]
                if wavelength not in wavelength_state: 
                    wavelength_state[wavelength] = {
                        "wavelength": wavelength,
                        "links": [],
                        "signal_nodes": [],
                        "pass_nodes": []
                    }
                if path_node in routing_path["regenerators"] or path_node in [lightpath["source"], lightpath["destination"]]:
                    wavelength_state[wavelength]["signal_nodes"].append(path_node)
                else:
                    wavelength_state[wavelength]["pass_nodes"].append(path_node)
                node_state[path_node]["wavelengths"].append(wavelength)

                if node_id < len(routing_path["path"])-1:
                    link = routing_path["path"][node_id] + "-" + routing_path["path"][node_id+1]
                    if link in link_state:
                        link_info = {
                            "source": routing_path["path"][node_id],
                            "destination": routing_path["path"][node_id+1]
                        }
                    else:
                        link = routing_path["path"][node_id+1] + "-" + routing_path["path"][node_id]
                        link_info = {
                            "source": routing_path["path"][node_id+1],
                            "destination": routing_path["path"][node_id]
                        }
                    link_state[link]["wavelengths"].append(wavelength)
                    wavelength_state[wavelength]["links"].append(link_info)
        return node_state, link_state, wavelength_state, lightpath_state, \
                total_lambda_link, average_lambda_capacity_usage
    
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
        routing_path = lightpath["routing_info"]["working"]
        node_state, link_state, wavelength_state, lightpath_state, \
                total_lambda_link, average_lambda_capacity_usage = extract_path_general_info(routing_path, node_state, link_state, wavelength_state, lightpath_state,
                                  total_lambda_link, average_lambda_capacity_usage)

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

    # for Protetion path
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
        routing_path = lightpath["routing_info"]["protection"]
        node_state, link_state, wavelength_state, lightpath_state, \
                total_lambda_link, average_lambda_capacity_usage = extract_path_general_info(routing_path, node_state, link_state, wavelength_state, lightpath_state,
                                  total_lambda_link, average_lambda_capacity_usage)

    average_lambda_capacity_usage = average_lambda_capacity_usage/ total_lambda_link   
    general_info_dict['protection'] = {
        'link_state': link_state,
        'node_state': node_state,
        'wavelength_state': wavelength_state,
        'lightpath_state': lightpath_state,
        'total_lambda_link': total_lambda_link,
        'average_lambda_capacity_usage': average_lambda_capacity_usage
    }
    general_info = RWAGeneralInfo(**general_info_dict)

    # for Restoration path
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
        if lightpath["routing_info"]["restoration"]:
            for restoration_path in lightpath["routing_info"]["restoration"]:
                routing_path = restoration_path["info"]
                node_state, link_state, wavelength_state, lightpath_state, \
                        total_lambda_link, average_lambda_capacity_usage = extract_path_general_info(routing_path, node_state, link_state, wavelength_state, lightpath_state,
                                        total_lambda_link, average_lambda_capacity_usage)

    average_lambda_capacity_usage = average_lambda_capacity_usage/ total_lambda_link   
    general_info_dict['restoration'] = {
        'link_state': link_state,
        'node_state': node_state,
        'wavelength_state': wavelength_state,
        'lightpath_state': lightpath_state,
        'total_lambda_link': total_lambda_link,
        'average_lambda_capacity_usage': average_lambda_capacity_usage
    }
    general_info = RWAGeneralInfo(**general_info_dict)
    return general_info
                
    