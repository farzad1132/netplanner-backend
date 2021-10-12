import json
import copy
from LOM_producer.schemas import LOM
from grooming.schemas import GroomingDBOut, GroomingResult
from LOM_producer.product import LOM_productioon

with open("grooming.json", 'rb') as file:
    groom_res = json.loads(file.read())

with open("rwa.json", 'rb') as file:
    rwa_res = json.loads(file.read())

with open("pt.json", 'rb') as file:
    pt = json.loads(file.read())[0]

for cln in groom_res['traffic']:
    for lpid in groom_res['traffic'][cln]['lightpaths']:
        rwa_res['result']['lightpaths'][lpid].update({'service_id_list': copy.deepcopy(
            groom_res['traffic'][cln]['lightpaths'][lpid]['service_id_list'])})

#groom_res = GroomingDBOut.parse_obj(groom_res).dic()

print("5")
lom = LOM_productioon(
    device=groom_res['lom_outputs'],
    RWAres=rwa_res['result']['lightpaths'],
    Physical_topology=pt,
    grooming_res=groom_res
)

lom = LOM.parse_obj(lom).dict()

from grooming.utils import lom_excel_generator

lom_excel_generator(lom, pt, filename="lom.xlsx", project_name="kerman", grooming_algorithm="test")

print("test")
