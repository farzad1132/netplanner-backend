from models import TrafficMatrixModel, TrafficMatrixUsersModel
from typing import Optional, List, Tuple
from dependencies import auth_user, get_current_user, get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, File
from users.schemas import User
from traffic_matrix.schemas import TrafficMatrixDB, TrafficMatrixSchema
from physical_topology.schemas import methods
from pandas import ExcelFile, read_excel

class GetTM:
    def __init__(self, mode: methods = methods.get):
        self.mode = mode

    def __call__(self, id: str, version: Optional[int] = None,
                user: User = Depends(get_current_user),
                 db: Session = Depends(get_db)) -> List[TrafficMatrixDB]:
        user_id = user.id
        if version is None:
            tm_list = db.query(TrafficMatrixModel).filter_by(id=id, is_deleted=False).all()
        else:
            tm_list = db.query(TrafficMatrixModel).filter_by(id=id, version=version, is_deleted=False).all()
        
        if not tm_list:
            raise HTTPException(status_code=404, detail="traffic matrix not found")
        elif user_id == tm_list[0].owner_id:
            return tm_list
        elif self.mode in ("DELETE", "SHARE"):
            raise HTTPException(status_code=401, detail="not authorized")
    
        if db.query(TrafficMatrixUsersModel).filter_by(tm_id=id, user_id=user_id, is_deleted=False).one_or_none() is None:
            raise HTTPException(status_code=401, detail="not authorized")
        else:
            return tm_list

def check_tm_name_conflict(user_id: str, name: str, db: Session):
    id_list = get_user_tms_id(user_id, db)
    if db.query(TrafficMatrixModel).filter_by(name=name, owner_id=user_id, version=1, is_deleted=False)\
        .filter(TrafficMatrixModel.id.in_(id_list)).one_or_none() is not None:
        raise HTTPException(status_code=409, detail=f"name of the traffic matrix '{name}' has conflict with another record")

def get_user_tms_id(user_id: str, db: Session, all: Optional[bool]= True)\
 -> List[str]:
    id_list = []
    if all is True:
        owned_tms = db.query(TrafficMatrixModel)\
                    .filter_by(owner_id=user_id, is_deleted=False)\
                    .distinct(TrafficMatrixModel.id)\
                    .order_by(TrafficMatrixModel.id.desc()).all()
        for tm in owned_tms:
            id_list.append(tm.id)
    
    shared_tms = db.query(TrafficMatrixUsersModel).filter_by(user_id=user_id, is_deleted=False).all()
    for tm in shared_tms:
        id_list.append(tm.tm_id)
    
    return id_list

def get_tm_last_version(id: str, db: Session) -> TrafficMatrixDB:
    tm = db.query(TrafficMatrixModel).filter_by(id=id, is_deleted=False)\
            .distinct(TrafficMatrixModel.version)\
            .order_by(TrafficMatrixModel.version.desc()).first()
    return tm

def excel_to_tm(tm_binary: bytes) -> Tuple[bool, TrafficMatrixSchema]:
    GENERAL_COLUMNS = ['ID', 'Source', 'Destination','Restoration_Type',"Protection_Type"]
    SERVICE_HEADERS = ['Quantity_E1', 'Quantity_STM1 Electrical', 'Quantity_STM1 Optical', 'Quantity_STM4', 'Quantity_STM16', 
                        'Quantity_STM64', 'Quantity_FE', 'Quantity_GE', 'Quantity_10GE', 'Quantity_100GE']

    def service_quantity_check(cell):
        try:
            if str(cell) == 'nan':
                return 0
            else:
                return int(float(cell))
        except:
            return None

    tm = {}
    excel = ExcelFile(tm_binary)
    data = excel.parse(header=1, skipfooter=0)
    for header in GENERAL_COLUMNS:
        if not header in data:
            raise HTTPException(status_code=400, detail=f"there is no {header} column")

    #demands_list = []
    demands_dict = {}
    demand_id = 1
    flag = True
    service_id = 1
    for row in data["ID"].keys():
        demand = {}
        id = demand_id
        demand["id"] = demand_id
        demand_id += 1

        demand["source"] = str(data["Source"][row]).strip()
        demand["destination"] = str(data["Destination"][row]).strip()
        demand["type"] = None

        demand["protection_type"] = str(data["Protection_Type"][row]).strip()
        if not demand["protection_type"] in ("NoProtection", "1+1_NodeDisjoint"):
            #return {"error_msg" : f"wrong entry for ProtectionType, ID = {row}"}, 400
            flag = False
            demand["protection_type_error"] = "err_code:6, 'protection_type' must be in ('NoProtection', '1+1_NodeDisjoint')"

        demand["restoration_type"] = str(data["Restoration_Type"][row]).strip()
        if not demand["restoration_type"] in ("JointSame", "None", "AdvJointSame"):
            #return {"error_msg" : f"wrong entry for RetorationType, ID = {row}"}, 400
            flag = False
            demand["restoration_type_error"] = "err_code:7, 'restoration_type' must be from ('JointSame', 'None', 'AdvJointSame')"
        
        demand["services"] = []
        for service in SERVICE_HEADERS:
            quantity = service_quantity_check(data[service][row])
            if quantity is not None:
                if quantity != 0:
                    demand["services"].append({
                        "type": service[9::],
                        "quantity": quantity,
                        "service_id_list": [i for i in range(service_id, service_id + quantity)]
                    })
                    service_id += quantity
            else:
                #return {"error_msg" : f"wrong entry of quantity at ID = {row} and service {service[9::]}"}, 400
                flag = False
                demand["services"].append({
                    "type": service[9::],
                    "quantity": data[service][row],
                    "quantity_error": "err_code:8, 'quantity' must be integer",
                    "service_id_list": []
                })
        
        #demands_list.append(demand)
        demands_dict[id] = demand

    tm["demands"] = demands_dict
    return flag, tm