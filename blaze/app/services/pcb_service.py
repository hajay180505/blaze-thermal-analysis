from app.services.database import db
from uuid import uuid4
from temperature_service import *

async def create_pcb_board(pcb_type, image_path):
    collection = db[pcb_type]
    care_areas = await get_care_areas()

    temperature_data = get_temperature_data(image_path, care_areas)
    id = str(uuid4())
    data = {
        "id" : id,
        "temperature_data" : temperature_data
    }
    result = await collection.insert_one(data)
    return result.inserted_id

async def get_pcbs(pcb_type):
    collection = db[pcb_type]
    return await collection.find().to_list(100)

async def get_pcb_types():
    # collection = db[pcb_type] 
    collection = "query1"
    return await collection.find().to_list(100)

async def create_pcb_type():
    # collection = db[pcb_type] 
    collection = "query1"
    return await collection.find().to_list(100)

async def get_care_areas(pcb_type):
    ...

