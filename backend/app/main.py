from fastapi import FastAPI

from app.api.routes.items import router as items_router
from app.api.routes.root import router as root_router

app = FastAPI()

app.include_router(root_router)
app.include_router(items_router)
