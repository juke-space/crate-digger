"""
    Server entry point
"""
import uvicorn
from fastapi import FastAPI

import query_api # DON'T REMOVE. Needed for API methods
from crate_server.apis.default_api import router

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
