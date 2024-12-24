from app.services.database import db

async def create_pcb(pcb_type, desired_areas, image_path):
    collection = db[pcb_type]
    data = {
        "image_path": image_path,
        "desired_areas": desired_areas,
    }
    result = await collection.insert_one(data)
    return result.inserted_id

async def get_pcbs(pcb_type):
    collection = db[pcb_type]
    return await collection.find().to_list(100)
