from fastapi import FastAPI, Depends
import uvicorn
from rwa.routes import rwa_router
from grooming.routes import grooming_router
from users.routes import user_router
from dependencies import get_db, auth_user
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# version 2 of netplanner api
app = FastAPI(  version="2.0.0",
                title="Netplanner",
                dependencies=[Depends(get_db)])
#                servers=[{"url":"/api/v2"}])
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(rwa_router)
#                    prefix="/api/v2")
app.include_router(grooming_router)
app.include_router(user_router)

app.add_middleware(CORSMiddleware,
                    allow_origins=['*'],
                    allow_credentials=True,
                    allow_methods=['*'],
                    allow_headers=["*"]
                    )

if __name__ == "__main__":
    uvicorn.run("main:app", port=5020, reload=True)