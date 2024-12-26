from fastapi import APIRouter, Form, File, UploadFile, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
from app.services.pcb_service import *

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/upload")
async def upload_page(request: Request):
    # pcb_types = ["Type A", "Type B", "Type C"]
    pcb_types = await get_pcb_types()
    return templates.TemplateResponse("upload.html", {"request": request, "pcb_types": pcb_types})

@router.post("/upload")
async def upload_thermal_image(
    pcb_type: str = Form(...),
    thermal_image: UploadFile = File(...)
):
    file_path = f"uploads/{thermal_image.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(thermal_image.file, buffer)

    await create_pcb_board(pcb_type, file_path)
    return RedirectResponse(url="/", status_code=303)

@router.get("/view-pcb-types/}")
async def view_data(request: Request):
    pcb_data = await get_pcbs()
    return templates.TemplateResponse("view_data.html", {"request": request, "pcb_data": pcb_data})


@router.post("/create-pcb-types/}")
async def view_data(
    pcb_name : str = Form(...),
    care_areas : str = Form(...)
):
    pcb_data = await get_pcbs()
    return templates.TemplateResponse("view_data.html", {"request": request, "pcb_data": pcb_data})
