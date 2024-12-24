from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import pcb_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(pcb_router.router)
