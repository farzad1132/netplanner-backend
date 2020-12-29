from fastapi import FastAPI, Depends
import uvicorn
from rwa import routes
from dependencies import get_db, auth_user

# version 2 of netplanner api
app = FastAPI(version="2.0.0",
                title="Netplanner",
                dependencies=[Depends(get_db), Depends(auth_user)])

app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)