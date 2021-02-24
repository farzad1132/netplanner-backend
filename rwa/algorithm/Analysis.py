from rwa.algorithm.components import Collision
from collections import Counter

def get_path_edge_indices(graph, path_segments):
    edge_indices = []
    edge_indices_on_segments = []
    for seg_index, seg in enumerate(path_segments):
        local_edge_indices = []
        for j in range(len(seg) - 1):
            if (seg[j], seg[j + 1]) in list(graph.edges):
                local_edge_indices.append(list(graph.edges).index((seg[j], seg[j + 1])))
            else:
                #### Reverse link
                local_edge_indices.append(list(graph.edges).index((seg[j + 1], seg[j])))
        edge_indices_on_segments.append(local_edge_indices)
        edge_indices += local_edge_indices
    return edge_indices, edge_indices_on_segments

def analyse_link_assignment(link, link_id, wavelength, option_type, lightpath, shared_wavelengths,
                            dedicated_wavelengths, shared_lightpaths, dedicated_lightpaths,
                            invalid_wavelengths_set_on_failed_link, invalid_lightpaths_dict_on_failed_link,
                            main_wavelengths, collision_dict):

    def add_collision(link, wavelength, lightpath, option_type, collision_dict, collision_with):
        if (link, wavelength) not in collision_dict.keys():
            collision_dict[(link, wavelength)] = Collision(link, wavelength)
            if collision_with == "Dedicated":
                collision_dict[(link, wavelength)].add_collision(dedicated_lightpaths[link_id][wavelength][0], option_type="Dedicated")
            elif collision_with == "Shared":
                collision_dict[(link, wavelength)].add_collision(shared_lightpaths[link_id][wavelength][0], option_type="Restoration")
            elif collision_with == "Invalid":
                collision_dict[(link, wavelength)].add_collision(invalid_lightpaths_dict_on_failed_link[link_id][wavelength][0], option_type="Restoration")
        collision_dict[(link, wavelength)].add_collision(lightpath, option_type)

    def add_list_element_to_dict(lightpath_dict, wavelength, lightpath):
        if wavelength not in lightpath_dict.keys():
            lightpath_dict[wavelength] = [lightpath]
        else:
            lightpath_dict[wavelength].append(lightpath)

    no_collision = True
    if option_type == "Restoration" and \
        wavelength in dedicated_wavelengths[link_id]-main_wavelengths[link_id]:
        add_collision(link, wavelength, lightpath, option_type, collision_dict, collision_with="Dedicated")
        no_collision = False
    if option_type == "Restoration" and \
        wavelength in invalid_wavelengths_set_on_failed_link[link_id]:
        add_collision(link, wavelength, lightpath, option_type, collision_dict, collision_with="Invalid")
        no_collision = False
    elif option_type != "Restoration" and \
        wavelength in dedicated_wavelengths[link_id]:
        add_collision(link, wavelength, lightpath, option_type, collision_dict, collision_with="Dedicated")
        no_collision = False
    elif option_type != "Restoration" and \
        wavelength in shared_wavelengths[link_id]:
        add_collision(link, wavelength, lightpath, option_type, collision_dict, collision_with="Shared")
        no_collision = False
    # Update everything
    if option_type == "Restoration":
        shared_wavelengths[link_id].add(wavelength)
        invalid_wavelengths_set_on_failed_link[link_id].add(wavelength)
        add_list_element_to_dict(shared_lightpaths[link_id], wavelength, lightpath)
        add_list_element_to_dict(invalid_lightpaths_dict_on_failed_link[link_id], wavelength, lightpath)
    else:
        dedicated_wavelengths[link_id].add(wavelength)
        add_list_element_to_dict(dedicated_lightpaths[link_id], wavelength, lightpath)
    return no_collision


def detect_wavelength_collisions(network, print_collisions=True):
    from rwa.algorithm.components import RegenOption
    graph = network.graph.copy()
    graph = graph.to_undirected()
    num_used_wavelengths = len(
                list(Counter([item for sublist in network.used_wavelengths for item in sublist]).keys()))
    shared_wavelengths = [set() for _ in range(len(list(graph.edges)))]
    dedicated_wavelengths = [set() for _ in range(len(list(graph.edges)))]
    shared_lightpaths = [{} for _ in range(len(list(graph.edges)))]
    dedicated_lightpaths = [{} for _ in range(len(list(graph.edges)))]
    invalid_wavelengths_dict = {}
    for link in list(graph.edges):
        invalid_wavelengths_dict[link] = [set() for _ in range(len(list(graph.edges)))]
    invalid_lightpaths_dict = {}
    for link in list(graph.edges):
        invalid_lightpaths_dict[link] = [{} for _ in range(len(list(graph.edges)))]
    collision_dict = {}
    for lightpath in network.extractedLightpathlist:
        main_wavelengths = [set() for _ in range(len(list(graph.edges)))]
        protection_wavelengths = [set() for _ in range(len(list(graph.edges)))]
        working_option = lightpath.selected_regen_option.main_option
        option_type = "Working"
        _ , edge_indices_on_segments = get_path_edge_indices(graph, working_option.path_segments)
        for seg_id, seg in enumerate(edge_indices_on_segments):
            wavelength = working_option.path_wavelengths
            for link_id in seg:
                invalid_wavelengths_set_on_failed_link = None
                invalid_lightpaths_dict_on_failed_link = None
                main_wavelengths[link_id].add(wavelength)
                link = list(graph.edges)[link_id]
                analyse_link_assignment(link, link_id, wavelength, option_type, lightpath, shared_wavelengths,
                            dedicated_wavelengths, shared_lightpaths, dedicated_lightpaths,
                            invalid_wavelengths_set_on_failed_link, invalid_lightpaths_dict_on_failed_link,
                            main_wavelengths, collision_dict)
        protection_option = lightpath.selected_regen_option.protection_option
        option_type = "Protection"
        _ , edge_indices_on_segments = get_path_edge_indices(graph, protection_option.path_segments)
        for seg_id, seg in enumerate(edge_indices_on_segments):
            wavelength = protection_option.path_wavelengths
            for link_id in seg:
                invalid_wavelengths_set_on_failed_link = None
                invalid_lightpaths_dict_on_failed_link = None
                protection_wavelengths[link_id].add(wavelength)
                link = list(graph.edges)[link_id]
                analyse_link_assignment(link, link_id, wavelength, option_type, lightpath, shared_wavelengths,
                            dedicated_wavelengths, shared_lightpaths, dedicated_lightpaths,
                            invalid_wavelengths_set_on_failed_link, invalid_lightpaths_dict_on_failed_link,
                            protection_wavelengths, collision_dict)

        option_type = "Restoration"
        if lightpath.selected_regen_option.restoration_option_list is not None:
            restoration_option_list = lightpath.selected_regen_option.restoration_option_list
        else:
            restoration_option_list = []
        for failed_link_id, restoration_option in enumerate(restoration_option_list):
            if isinstance(restoration_option, RegenOption):
                failed_link_temp = (lightpath.selected_regen_option.main_option.path[failed_link_id],
                            lightpath.selected_regen_option.main_option.path[failed_link_id + 1])
                if failed_link_temp in list(graph.edges):
                    failed_link = failed_link_temp
                else:
                    failed_link = (failed_link_temp[1], failed_link_temp[0])
                _ , edge_indices_on_segments = get_path_edge_indices(graph, restoration_option.path_segments)
                for seg_id, seg in enumerate(edge_indices_on_segments):
                    wavelength = restoration_option.path_wavelengths[seg_id]
                    for link_id in seg:
                        invalid_wavelengths_set_on_failed_link = invalid_wavelengths_dict[failed_link]
                        invalid_lightpaths_dict_on_failed_link = invalid_lightpaths_dict[failed_link]
                        link = list(graph.edges)[link_id]
                        analyse_link_assignment(link, link_id, wavelength, option_type, lightpath, shared_wavelengths,
                                    dedicated_wavelengths, shared_lightpaths, dedicated_lightpaths,
                                    invalid_wavelengths_set_on_failed_link, invalid_lightpaths_dict_on_failed_link,
                                    main_wavelengths, collision_dict)
        if lightpath.selected_regen_option.protection_restoration_option_list is not None:
            protection_restoration_option_list = lightpath.selected_regen_option.protection_restoration_option_list
        else:
            protection_restoration_option_list = []
        for failed_link_id, restoration_option in enumerate(protection_restoration_option_list):
            if isinstance(restoration_option, RegenOption):
                failed_link_temp = (lightpath.selected_regen_option.protection_option.path[failed_link_id],
                            lightpath.selected_regen_option.protection_option.path[failed_link_id + 1])
                if failed_link_temp in list(graph.edges):
                    failed_link = failed_link_temp
                else:
                    failed_link = (failed_link_temp[1], failed_link_temp[0])
                _ , edge_indices_on_segments = get_path_edge_indices(graph, restoration_option.path_segments)
                for seg_id, seg in enumerate(edge_indices_on_segments):
                    wavelength = restoration_option.path_wavelengths[seg_id]
                    for link_id in seg:
                        invalid_wavelengths_set_on_failed_link = invalid_wavelengths_dict[failed_link]
                        invalid_lightpaths_dict_on_failed_link = invalid_lightpaths_dict[failed_link]
                        link = list(graph.edges)[link_id]
                        analyse_link_assignment(link, link_id, wavelength, option_type, lightpath, shared_wavelengths,
                                    dedicated_wavelengths, shared_lightpaths, dedicated_lightpaths,
                                    invalid_wavelengths_set_on_failed_link, invalid_lightpaths_dict_on_failed_link,
                                    protection_wavelengths, collision_dict)
    if print_collisions == True:
        for collision in collision_dict.values():
            print(collision)
        if not collision_dict:
            print("     NO WAVELENGTH Collisions found!\n Avanced restorations not checked!")
        print("-----------------------------------------------------")
    else:
        if collision_dict:
            print("WARNING: WAVELENGTH Collisions found!")
        if not collision_dict:
            print("     NO WAVELENGTH Collisions found!\n Avanced restorations not checked!")
        print("-----------------------------------------------------")

