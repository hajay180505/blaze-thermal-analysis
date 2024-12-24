from fastapi import APIRouter, Form, File, UploadFile, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil
from app.services.pcb_service import create_pcb, get_pcbs

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/upload")
async def upload_page(request: Request):
    pcb_types = ["Type A", "Type B", "Type C"]
    return templates.TemplateResponse("upload.html", {"request": request, "pcb_types": pcb_types})

@router.post("/upload")
async def upload_thermal_image(
    pcb_type: str = Form(...),
    desired_areas: str = Form(...),
    thermal_image: UploadFile = File(...)
):
    file_path = f"uploads/{thermal_image.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(thermal_image.file, buffer)

    await create_pcb(pcb_type, eval(desired_areas), file_path)
    return RedirectResponse(url="/", status_code=303)

@router.get("/view/{pcb_type}")
async def view_data(request: Request, pcb_type: str):
    pcb_data = await get_pcbs(pcb_type)
    return templates.TemplateResponse("view_data.html", {"request": request, "pcb_data": pcb_data})
