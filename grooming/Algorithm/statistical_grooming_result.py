

def statistical_result(finalres,devicee):
    sum=0
    num=0
    for sbtmid in finalres["traffic"].keys():

        for lpid in finalres["traffic"][sbtmid]["lightpaths"].keys():
            sum = sum + finalres["traffic"][sbtmid]["lightpaths"][lpid]["capacity"]
        num = num + len(finalres["traffic"][sbtmid]["lightpaths"])
    sum = sum / num
    groomout_no = 0
    for sbtmid in finalres["traffic"].keys():
        for did in finalres["traffic"][sbtmid]["low_rate_grooming_result"]["demands"].keys():
            groomout_no = groomout_no + len(finalres["traffic"][sbtmid]["low_rate_grooming_result"]["demands"][did]["groomouts"])
    mp2x_no = 0
    tp1h_no = 0
    mp1h_no = 0
    for tmid in devicee.keys():
        for node in devicee[tmid].keys():
            mp2x_no = mp2x_no + len(devicee[tmid][node]["MP2X"])
            tp1h_no = tp1h_no + len(devicee[tmid][node]["TP1H"])
            mp1h_no = mp1h_no + len(devicee[tmid][node]["MP1H"])
    res={   "lightpath_no": num,
            "mean_lightpath_cap": sum,
            "groomout_no":groomout_no,
            "mp2x_no": mp2x_no,
            "tp1h_no": tp1h_no,
            "mp1h_no": mp1h_no
            }

    return res