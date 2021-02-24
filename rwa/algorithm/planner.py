import networkx as nx
import random
import itertools
from collections import Counter
import time
import numpy as np
import math 
import warnings

from rwa.algorithm.oldnetwork import OldNetwork, NetModule, random_shuffle_solver
from rwa.algorithm.Analysis import detect_wavelength_collisions
# from solvers import solve_two_way_protected_windowed_ILP, ILP_2way_protected_solver_subroutine



def plan_network(net, k=5,k_restoration=2, k_second_restoration=2, num_second_restoration_random_samples=10, solver='Greedy',
                 iterations = 10, processors = 8, max_new_wavelength_num = 6,
                 history_window = 4, demand_group_size = 6):
    """
    This function plots the Network `net`, generates `D` random demands and then
    solves the routing problem using greedy `k`-shortest path algorithm.
    If the basmap package is available, by setting `earth_map`, the function 
    also plots the network on the `earth_map`.
    `fig_size` is the size of displayed figure.
    
    returns a solved `Network`.
    """
    net.gen_graph()
    G = net.graph
    #net.print_demand_list()
    #net.add_demand('Warsaw', 'London', 1)
    start = time.time()
    
    print('Starting network pre-process:')
    print(' Estimating parameters ....')
    
    #net.estimate_protected_wavelength_num()
    #print(' -Maximum required number of wavelengths is {}'.format(net.wavelength_num))
    if net.measure == 'osnr':
        net.estimate_reach(reach_step = 50)
    print(' -Estimated reach for each modulation: {}'.format(net.reach_options))
    
    net_module = NetModule(net, net.lower_bound, net.upper_bound, k, is_root = True)
    net_module.estimate_link_noise()
    #net_module.print_demand_list()
    #print(net_module.link_noise_psds)
    
    if solver=='Greedy':
        print(' Generating lightpathes ....')
        net_module.gen_protected_lightpaths(k, processors)
        # net_module.print_lightpaths()
        # assert False
        duration = time.time()-start
        print('Pre-process finished in {:0.3f}s\n'.format(duration))
        print('Starting random shuffle solver for {} demands:'.format(len(net.demand_list)))
        ######### Multiprocess ##############
        result_net = net_module
        # print(net_module.RegenOptionDict)
        # net_module.print_options()
        # planned_net_module = random_shuffle_solver(net_module, solver, k_restoration)
        # print(planned_net_module)
        # planned_net_module.print_results()
        # assert False
        net_module_list = []
        for i in range(iterations):
            net_module_list.append(NetModule(net_module, net_module.lower_bound, net_module.upper_bound, k, is_root = False))
        results = {}
        for i,module in enumerate(net_module_list):
            results[i] = random_shuffle_solver(module, solver, k_restoration,
                                               k_second_restoration, num_second_restoration_random_samples)
        
        objective = 100000 #large number
        for i in range(iterations):
            planned_net_module = results[i]
            if planned_net_module is not None:
                print("  -Objective in iteration {}: {:3.2f}".format(i, planned_net_module.upper_bound))
                if planned_net_module.upper_bound < objective:
                    objective = planned_net_module.upper_bound
                    #print(objective)
                    result_net = planned_net_module
                    #print(result_net.total_num_wavelengths)
            else:
                warnings.warn("Solution of iteration {} is invalid".format(i))
        
        
        print(' - Num of used wavelengths: {}'.format(result_net.total_num_wavelengths))
        #print(' - Lower bound on wavelengths: {}'.format(result_net.lb_wavelength_num[0]))
        print(' - Num of used regenerators: {}'.format(result_net.total_regen_num))
        #print(' - Lower bound on regenerators: {}'.format(result_net.lb_regen_num[0]))
        print('Calculating more accurate OSNR on links ....')
       
        result_net.exact_link_noise()
        result_net.assign_extracted_lightpath_osnr()
        detect_wavelength_collisions(result_net, print_collisions=True)

        # result_net.print_results()
        print('Done.')
        duration = time.time()-start
        print('RWA finished in {:0.3f}s.'.format(duration))
        
        # start = time.time()
        # result_net.find_LP_lower_bound()
        # duration = time.time()-start
        # print('LP lower-bound finished in {:0.3f}s.'.format(duration))
        # start = time.time()
        # result_net.find_ILP_lower_bound()
        # duration = time.time()-start
        # print('ILP lower-bound finished in {:0.3f}s.'.format(duration))
        return result_net


    elif solver == "ILP":
        print(' Generating lightpathes ....')
        net_module.gen_protected_lightpaths(k, processors)
        #net_module.print_lightpaths()
        duration = time.time()-start
        print('Pre-process finished in {:0.3f}s\n'.format(duration))
        print('Starting exact ILP solver for {} demands:'.format(len(net.demand_list)))
        net_module.solve_two_way_protected_ILP()
        result_net = net_module
        print(' - Num of used wavelengths: {}'.format(result_net.total_num_wavelengths))
        #print(' - Lower bound on wavelengths: {}'.format(result_net.lb_wavelength_num[0]))
        print(' - Num of used regenerators: {}'.format(result_net.total_regen_num))
        #print(' - Lower bound on regenerators: {}'.format(result_net.lb_regen_num[0]))
        print('Calculating more accurate OSNR on links ....')
        result_net.exact_link_noise()
        result_net.assign_extracted_lightpath_osnr()
        # result_net.print_results()
        print('Done.')
        duration = time.time()-start
        print('RWA finished in {:0.3f}s.'.format(duration))
        return result_net

    elif solver == "window_ILP":
        print(' Generating lightpathes ....')
        net_module.gen_protected_lightpaths(k, processors)
        #net_module.print_lightpaths()
        duration = time.time()-start
        print('Pre-process finished in {:0.3f}s\n'.format(duration))
        print('Starting random shuffle windowed ILP solver for {} demands:'.format(len(net.demand_list)))
        result_net = net_module
        # solve_two_way_protected_windowed_ILP(result_net, history_wavelength_num = history_window,
        #                      demand_group_num = demand_group_size, max_new_wavelength_num =  max_new_wavelength_num)
        # def random_shuffle_window_ILP(network, history_window = 4, demand_group_size = 6, max_new_wavelength_num =  6):
        #   solve_two_way_protected_windowed_ILP(network, history_wavelength_num = history_window,
        #                      demand_group_num = demand_group_size, max_new_wavelength_num =  max_new_wavelength_num)
        # random_shuffle_solver(result_net, solver, history_window = history_window,
        #                          demand_group_size = demand_group_size, max_new_wavelength_num = max_new_wavelength_num)                     
        # random_shuffle_solver(result_net, solver, history_window,
        #                           demand_group_size, max_new_wavelength_num)
        # assert False
        ######### Multiprocess ##############
        net_module_list = []
        for i in range(iterations):
            net_module_list.append(NetModule(net_module, net_module.lower_bound, net_module.upper_bound, k, is_root = False))

        results = {}
        for i,module in enumerate(net_module_list):
            results[i] = random_shuffle_solver(module, solver, k_restoration,  k_second_restoration, history_window,
                                                demand_group_size, max_new_wavelength_num)
        
        objective = 100000 #large number
        for i in range(iterations):
            planned_net_module = results[i]
            if planned_net_module is not None:
                print("  -Objective in iteration {}: {:3.2f}".format(i, planned_net_module.upper_bound))
                if planned_net_module.upper_bound < objective:
                    objective = planned_net_module.upper_bound
                    #print(objective)
                    result_net = planned_net_module
                    #print(result_net.total_num_wavelengths)
            else:
                warnings.warn("Solution of iteration {} is invalid".format(i))
        print(' - Num of used wavelengths: {}'.format(result_net.total_num_wavelengths))
        #print(' - Lower bound on wavelengths: {}'.format(result_net.lb_wavelength_num[0]))
        print(' - Num of used regenerators: {}'.format(result_net.total_regen_num))
        #print(' - Lower bound on regenerators: {}'.format(result_net.lb_regen_num[0]))
        print('Calculating more accurate OSNR on links ....')
        result_net.exact_link_noise()
        result_net.assign_extracted_lightpath_osnr()
        # result_net.print_results()
        print('Done.')
        duration = time.time()-start
        print('RWA finished in {:0.3f}s.'.format(duration))
        return result_net
        
        
        print(' - Num of used wavelengths: {}'.format(result_net.total_num_wavelengths))
        #print(' - Lower bound on wavelengths: {}'.format(result_net.lb_wavelength_num[0]))
        print(' - Num of used regenerators: {}'.format(result_net.total_regen_num))
        #print(' - Lower bound on regenerators: {}'.format(result_net.lb_regen_num[0]))
        print('Calculating more accurate OSNR on links ....')
        result_net.exact_link_noise()
        result_net.assign_extracted_lightpath_osnr()
        detect_wavelength_collisions(result_net, print_collisions=True)

        # result_net.print_results()
        print('Done.')
        duration = time.time()-start
        print('RWA finished in {:0.3f}s.'.format(duration))
        return result_net

    else:
        return None

