from fastapi import APIRouter, Depends
from projects.schemas import ProjectSchema
from projects.utils import GetProject

project_router = APIRouter(
    prefix="/projects",
    tags=["Project"]
)

get_project_mode_get = GetProject(mode="GET")
@project_router.get('/', status_code=200)
def read_project(project: ProjectSchema = Depends(get_project_mode_get)):
    return {"pt_id": project.physical_topology.id,
            "tm_id": project.traffic_matrix.id,
            "current_pt_version": project.current_pt_version,
            "current_tm_version": project.current_tm_version}