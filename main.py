from fastapi import FastAPI, Depends
import uvicorn
from rwa.routes import rwa_router
from grooming.routes import grooming_router
from users.routes import user_router
from dependencies import get_db, PREFIX
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import base, engine
from physical_topology.routes import pt_router
from projects.routes import project_router
from traffic_matrix.routes import tm_router
from clusters.routes import cluster_router
from sharings.routes import sharing_router

base.metadata.create_all(bind=engine)

# version 2 of netplanner api
app = FastAPI(  version="2.0.0",
                title="NetPlanner",
                dependencies=[Depends(get_db)])
#                servers=[{"url":"/api/v2"}])
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(rwa_router,
                    prefix=PREFIX)
app.include_router(grooming_router,
                    prefix=PREFIX)
app.include_router(user_router,
                    prefix=PREFIX)
app.include_router(pt_router,
                    prefix=PREFIX)
app.include_router(project_router,
                    prefix=PREFIX)
app.include_router(tm_router,
                    prefix=PREFIX)
app.include_router(cluster_router,
                    prefix=PREFIX)
app.include_router(sharing_router,
                    prefix=PREFIX)

app.add_middleware(CORSMiddleware,
                    allow_origins=['*'],
                    allow_credentials=True,
                    allow_methods=['*'],
                    allow_headers=["*"]
                    )

if __name__ == "__main__":
    uvicorn.run("main:app", port=5020, reload=True, host='0.0.0.0')