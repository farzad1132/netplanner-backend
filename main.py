from fastapi import FastAPI
import uvicorn
from rwa import routes

# version 2 of netplanner api
app = FastAPI(version="2.0.0",
                title="Netplanner")

app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, reload=True)