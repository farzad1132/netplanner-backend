from grooming.adv_grooming.schemas import LineRate, MultiplexThreshold
import json
from grooming.grooming_worker import adv_grooming_worker

with open("tests/test_rwa/pt.json", "rb") as jfile:
    pt = json.loads(jfile.read())[0]

with open("tests/test_rwa/tm.json", "rb") as jfile:
    tm = json.loads(jfile.read())[0]

result = adv_grooming_worker(pt=pt,
                            tm=tm,
                            multiplex_threshold=MultiplexThreshold.t70,
                            line_rate=LineRate.t100,
                            clusters={"clusters": {}},
                            check_input_type=False)

print("hi")