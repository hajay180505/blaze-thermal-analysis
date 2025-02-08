import streamlit as st
from PIL import Image
import os
from infer import *
from orient import *

def draw_bounding_boxes(image_path, detections_dict):
    image = cv2.imread(image_path)
    print(f"{detections_dict=}")
    for tag, (xmin, ymin, xmax, ymax) in detections_dict.items():
        print("{tag=}, {xmin=}, {ymin=}, {xmax=}, {ymax=}")
        # Draw the bounding box (color: green, thickness: 2)
        cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)

        # Add label above the bounding box (font: 0, scale: 0.7, color: white)
        cv2.putText(image, tag, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    return image


# Set the path where processed images are stored
PROCESSED_IMAGE_PATH = "processed_images/output.png"

st.title("Image Analysis App")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    
    file_path = os.path.join("./uploads/", uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    image = Image.open(uploaded_file)
    
    st.image(image, caption="Uploaded Image", use_container_width=True)
    
    detections = get_inference(image_file=file_path, saveImage= True)
    
    st.write("Detections coords : ", detections.xyxy)
    
    bb_image = Image.open(f"./predictions/predicted_{uploaded_file.name}")
    
    st.title("Labelled image")
    
    st.image(bb_image, caption="Labelled image", use_container_width=True)
    
    quadrants = assign_quadrants(detections.xyxy)
    
    problems = []
    q_new = {}
    for quadrant, box in quadrants.items():
        if box is None:
            problems.append(f"Resistor {quadrant} is missing")
            continue
        q_new[quadrant] = box

    img = draw_bounding_boxes(f"./uploads/{uploaded_file.name}", q_new)
    
    st.image(img,caption="Identified labels", use_container_width=True)
    
    if problems:
        st.title("Missing resistors") 
        for problem in problems:
            st.write(problem)    
        
        print(f"{quadrant}: {box}")
    

        
    


