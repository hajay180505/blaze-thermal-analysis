import numpy as np
import supervision as sv



def assign_quadrants(bounding_boxes : sv.Detections):
    """
    Assigns bounding boxes to quadrants: Top-Left (TL), Top-Right (TR), Bottom-Left (BL), Bottom-Right (BR).
    
    Parameters:
        bounding_boxes (list of tuples): List of (x_min, y_min, x_max, y_max) bounding boxes.
    
    Returns:
        dict: Quadrants with assigned bounding boxes or None if a quadrant is empty.
    """
    
    bounding_boxes = [tuple(detection) for detection in bounding_boxes]
        
    if not bounding_boxes:
        return {"R1": None, "R2": None, "R3": None, "R4": None}

    bbs = []
    for xmin,xmax,ymin,ymax in bounding_boxes:
        if (0 <= xmin <= 10) or (0 <= ymin <= 10) or (65 <= xmax <= 70) or (25 <= ymin <= 30):
            continue
        bbs.append((xmin,xmax,ymin,ymax))
    bounding_boxes = bbs
    # Compute center points of bounding boxes
    centers = [((x_min + x_max) // 2, (y_min + y_max) // 2) for (x_min, y_min, x_max, y_max) in bounding_boxes]

    # Compute global cenR2oid (average center)
    avg_x = sum(x for x, y in centers) / len(centers)
    avg_y = sum(y for x, y in centers) / len(centers)

    # Initialize quadrant mappings
    quadrants = {"R1": None, "R2": None, "R3": None, "R4": None}

    for i, box in enumerate(bounding_boxes):
        x_c, y_c = centers[i]

        if x_c < avg_x and y_c < avg_y:
            quadrants["R1"] = box
        elif x_c >= avg_x and y_c < avg_y:
            quadrants["R2"] = box
        elif x_c < avg_x and y_c >= avg_y:
            quadrants["R3"] = box
        elif x_c >= avg_x and y_c >= avg_y:
            quadrants["R4"] = box 

    return quadrants

