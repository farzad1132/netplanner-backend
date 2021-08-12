from grooming.adv_grooming.schemas import LineRate, MultiplexThreshold
import json
from grooming.grooming_worker import adv_grooming_worker

with open("/home/farzad/Desktop/BProject/G2/G2_pt.json", "rb") as jfile:
    pt = json.loads(jfile.read())[0]

with open("/home/farzad/Desktop/BProject/G2/G2_tm.json", "rb") as jfile:
    tm = json.loads(jfile.read())[0]

print("test")

result = adv_grooming_worker(pt=pt,
                            tm=tm,
                            multiplex_threshold=MultiplexThreshold.t70,
                            clusters={"clusters": {}},
                            line_rate=LineRate.t40,
                            return_original_result=True)

print("test")