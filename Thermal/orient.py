import numpy as np
import supervision as sv

IMAGE_WIDTH = 240
IMAGE_HEIGHT = 320

def assign_quadrants(bounding_boxes : sv.Detections) -> dict[str,tuple[int,...]]:
    """
    Assigns bounding boxes to quadrants: Top-Left (TL), Top-Right (TR), Bottom-Left (BL), Bottom-Right (BR).
    
    Parameters:
        bounding_boxes (list of tuples): List of (x_min, y_min, x_max, y_max) bounding boxes.
    
    Returns:
        dict: Quadrants with assigned bounding boxes or None if a quadrant is empty.
    """
    
    bounding_boxes = [tuple(detection) for detection in bounding_boxes]
        
    # print(f"{bounding_boxes=}")
    if not bounding_boxes:
        return {"R1": None, "R2": None, "R3": None, "R4": None}

    bbs = []
    for xmin,ymin,xmax,ymax in bounding_boxes:
        # print("NO    : ",xmin,xmax,ymin,ymax)
        # print("Booleans",(xmin <= 52),(ymin <= 71),(xmax >= 240),(ymax >= 187))
        if (xmin <= 52) or (ymin <= 71) or (xmax >= 240) or (ymax >= 187):
            print("Problem : ",xmin,xmax,ymin,ymax)
            continue
        bbs.append((xmin,ymin,xmax,ymax))
    bounding_boxes :list[tuple[int,...]] = bbs
    # Compute center points of bounding boxes
    centers = [((x_min + x_max) // 2, (y_min + y_max) // 2) for (x_min, y_min, x_max, y_max) in bounding_boxes]
    
    # Compute global centroid (average center)
    # avg_x = sum(x for x, y in centers) / len(centers)
    # avg_y = sum(y for x, y in centers) / len(centers)
    avg_y = IMAGE_WIDTH // 2
    avg_x = IMAGE_HEIGHT // 2

    # print(f"{avg_x=} {avg_y=}")
    # Initialize quadrant mappings
    quadrants :dict[str, tuple[int,...]]= {"R1": None, "R2": None, "R3": None, "R4": None}

    for i, box in enumerate(bounding_boxes):
        x_c, y_c = centers[i]
        # print(f"{x_c=} {y_c=}", end=" -> ")

        if x_c < avg_x and y_c < avg_y:
            # print("R1")
            quadrants["R1"] = box
        elif x_c >= avg_x and y_c < avg_y:
            # print("R2")
            quadrants["R2"] = box
        elif x_c < avg_x and y_c >= avg_y:
            # print("R3")
            quadrants["R3"] = box
        elif x_c >= avg_x and y_c >= avg_y:
            # print("R4")
            quadrants["R4"] = box 

    return quadrants

