import unittest
from grooming.Algorithm.validation import manual_grooming_validation
from grooming.schemas import GroomingResult, ClusteredTMs, ServiceMapping
import json
class GroomingErrorTestCase(unittest.TestCase):
        
    def test_groomout_Source(self):
        with open(r'tests\test_grooming\validation_tests\groomout_Source.json') as json_file2:
            input2 = json.load(json_file2)

        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
        #self.assertRaises(Exception) 
                  
        #self.assertEqual(result,response)
    def test_groomout_destination(self):
        with open(r'tests\test_grooming\validation_tests\groomout_destination.json') as json_file2:
            input3 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input3['res'], Trafficmatrix=input3['tm'], cluster=input3['cl'])
    def test_groomout_stypemp2x(self):
        with open(r'tests\test_grooming\validation_tests\groomout_stypemp2x.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])

    def test_groomout_2smp2x(self):
        with open(r'tests\test_grooming\validation_tests\groomout_2smp2x.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    
    def test_groomout_stypeps6x(self):
        with open(r'tests\test_grooming\validation_tests\groomout_stypeps6x.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_groomout_2sps6x(self):
        with open(r'tests\test_grooming\validation_tests\groomout_2sps6x.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    
    
    def test_groomout_overloadcapmp2x(self):
        with open(r'tests\test_grooming\validation_tests\groomout_overloadcapmp2x.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    
    def test_groomout_overloadsumcapmp2x(self):
        with open(r'tests\test_grooming\validation_tests\groomout_overloadsumcapmp2x.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    
    def test_lightpath_1servicein2lightpath(self):
        with open(r'tests\test_grooming\validation_tests\lightpath_1servicein2lightpath.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_lightpath_lowservicein_nonc_lightpath(self):
        with open(r'tests\test_grooming\validation_tests\lowservicein_nonc_lightpath.json') as json_file2:
            input2 = json.load(json_file2)  
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl']) 
    def test_lightpath_lowservice_in_lightpath(self):
        with open(r'tests\test_grooming\validation_tests\lowservice_in_lightpath.json') as json_file2:
            input2 = json.load(json_file2)
      
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl']) 

    def test_lightpath_groomout_in_2lightpath(self):
        with open(r'tests\test_grooming\validation_tests\groomout_in_2lightpath.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])

    def test_lightpath_differ_cap_lightpath(self):
        with open(r'tests\test_grooming\validation_tests\differ_cap_lightpath.json') as json_file2:
            input2 = json.load(json_file2)
      
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl']) 
    def test_lightpath_groomout_in_2lightpath(self):
        with open(r'tests\test_grooming\validation_tests\groomout_in_2lightpath.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])    
    def test_lightpath_more_cap_lightpath(self):
        with open(r'tests\test_grooming\validation_tests\more_cap_lightpath.json') as json_file2:
            input2 = json.load(json_file2)   
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl']) 

    def test_lightpath_more_cap_lightpathnon(self):
        with open(r'tests\test_grooming\validation_tests\more_cap_lightpathnon.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])  
    
    
    def test_remaining_service_in_lightpath(self):
        with open(r'tests\test_grooming\validation_tests\remaining_service_in_lightpath.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])  
    def test_remaining_groomout_in_lightpath(self):

        with open(r'tests\test_grooming\validation_tests\remaining_groomout_in_lightpath.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception):
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])    
    def test_device_subtm_mp2x(self):
        with open(r'tests\test_grooming\validation_tests\device_subtm_mp2x.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception):
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])

        
        
          
    def test_device_groomout_mp2x_l1(self):
        with open(r'tests\test_grooming\validation_tests\device_groomout_mp2x_l1.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])

    def test_device_demand_mp2x_l1(self):
        with open(r'tests\test_grooming\validation_tests\device_demand_mp2x_l1.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_device_groomout_mp2x_l2(self):
        with open(r'tests\test_grooming\validation_tests\device_groomout_mp2x_l2.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl']) 
    
    def test_device_demand_mp2x_l2(self):
        with open(r'tests\test_grooming\validation_tests\device_demand_mp2x_l2.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    
    def test_device_rep_mp2x_l2(self):
        with open(r'tests\test_grooming\validation_tests\device_rep_mp2x_l2.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception):
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
         
    
    def test_device_rep_mp2x_l1(self):
        with open(r'tests\test_grooming\validation_tests\device_rep_mp2x_l1.json') as json_file2:
            input2 = json.load(json_file2)
         
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])

   
    def test_device_subtm_mp1h(self):
        with open(r'tests\test_grooming\validation_tests\device_subtm_mp1h.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl']) 
    
    def test_device_Lpid_mp1h(self):
        with open(r'tests\test_grooming\validation_tests\device_Lpid_mp1h.json') as json_file2:
            input2 = json.load(json_file2)
       
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl']) 
    
    def test_device_subtm_Tp1h(self):
        with open(r'tests\test_grooming\validation_tests\device_subtm_Tp1h.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_device_Lpid_Tp1h(self):
        with open(r'tests\test_grooming\validation_tests\device_Lpid_Tp1h.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_device_TMid_TP2X_ch1(self):
        with open(r'tests\test_grooming\validation_tests\device_TMid_TP2X_ch1.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_device_LPid_TP2X_ch1(self):
        with open(r'tests\test_grooming\validation_tests\device_LPid_TP2X_ch1.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_device_TMid_TP2X_ch2(self):
        with open(r'tests\test_grooming\validation_tests\device_TMid_TP2X_ch2.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    
    def test_device_LPid_TP2X_ch2(self):
        with open(r'tests\test_grooming\validation_tests\device_LPid_TP2X_ch2.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_device_tmid_TPAX_ch1(self):
        with open(r'tests\test_grooming\validation_tests\device_tmid_TPAX_ch1.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_device_LPid_TPAX_ch1(self):
        with open(r'tests\test_grooming\validation_tests\device_LPid_TPAX_ch1.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_device_demandid_TPAX_ch1(self):
        with open(r'tests\test_grooming\validation_tests\device_demandid_TPAX_ch1.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    
    def test_device_tmid_TPAX_ch2(self):
        with open(r'tests\test_grooming\validation_tests\device_tmid_TPAX_ch2.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_device_demand_TPAX_ch2(self):
        with open(r'tests\test_grooming\validation_tests\device_demand_TPAX_ch2.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_device_Lp_TPAX_ch2(self):
        with open(r'tests\test_grooming\validation_tests\device_Lp_TPAX_ch2.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
    def test_clusteredTM(self):
        with open(r'tests\test_grooming\validation_tests\clusteredTM.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])   
    def test_SERVICEMAP_demand_original(self):
        with open(r'tests\test_grooming\validation_tests\SERVICEMAP_demand_original.json') as json_file2:
            input2 = json.load(json_file2)
    	                
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])	

    def test_SERVICEMAP_service_original(self):
        with open(r'tests\test_grooming\validation_tests\SERVICEMAP_service_original.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])    


    def test_SERVICEMAP_tmid_original(self):
        
        with open(r'tests\test_grooming\validation_tests\SERVICEMAP_tmid_original.json') as json_file2:
            input2 = json.load(json_file2)
                                                                                                                                             
						
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])                                                                                            
    def test_SERVICEMAP_srvm_original(self):
        
        with open(r'tests\test_grooming\validation_tests\SERVICEMAP_srvm_original.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])    
    def test_SERVICEMAP_did_original(self):
        with open(r'tests\test_grooming\validation_tests\SERVICEMAP_did_original.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])

    def test_SERVICEMAP_wrongmap_original(self):
        
        with open(r'tests\test_grooming\validation_tests\SERVICEMAP_wrongmap_original.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])                                                                                                                                                           
    def test_SERVICEMAP_notvalidtrafficmatrix(self):
        
        with open(r'tests\test_grooming\validation_tests\SERVICEMAP_notvalidtrafficmatrix.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl']) 

    def test_SERVICEMAP_notvaliddemand(self):
        
        with open(r'tests\test_grooming\validation_tests\SERVICEMAP_notvaliddemand.json') as json_file2:
            input2 = json.load(json_file2)
                                                                                                                                                   
		
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])                                                                                                                                                           
    def test_SERVICEMAP_notvalidservice(self):
        
        with open(r'tests\test_grooming\validation_tests\SERVICEMAP_notvalidservice.json') as json_file2:
            input2 = json.load(json_file2)
    
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])    

    def test_table_test_NO_split(self):
        with open(r'tests\test_grooming\validation_tests\table_test_NO_split.json') as json_file2:
                input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
                          
    def test_table_test_NO_end(self):
        with open(r'tests\test_grooming\validation_tests\table_test_NO_end.json') as json_file2:
            input2 = json.load(json_file2)
        with self.assertRaises(Exception): 
            manual_grooming_validation(groomingresult=input2['res'], Trafficmatrix=input2['tm'], cluster=input2['cl'])
if __name__ == '__main__':
    unittest.main()