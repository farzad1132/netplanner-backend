

def statistical_result(finalres):
    sum=0
    num=0
    for sbtmid in finalres["traffic"].keys():

        for lpid in finalres["traffic"][sbtmid]["lightpaths"].keys():
            sum = sum + finalres["traffic"][sbtmid]["lightpaths"][lpid]["capacity"]
        num = num + len(finalres["traffic"][sbtmid]["lightpaths"])
    sum = sum / num
    res={   "lightpath_no": num,
            "mean_lightpath_cap": sum}
    return res