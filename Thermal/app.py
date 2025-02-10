import streamlit as st
from PIL import Image
import os
from infer import *
from orient import *
from thermal import *
from lifetime import *

ALLOWABLE_THRESHOLDS = [50,50,50,50]

def extract(coords_og):
    
    thermals = {
        k : (v[0]+35, v[1], v[2]+35, v[3]) for k,v in coords_og.items()
    }
    
    print(f"{thermals=}")
    print(f"{coords_og=}")
    coords = [(xmin, ymin, xmax - xmin, ymax - ymin) for xmin, ymin, xmax, ymax in coords_og.values()]
    therm_coords = [(xmin, ymin, xmax - xmin, ymax - ymin) for xmin, ymin, xmax, ymax in thermals.values()]
    thermal_file = st.file_uploader("Upload corresponding thermal image", type=["png", "jpg", "jpeg"])
    
    if thermal_file:
        file_path = os.path.join("./uploads/", thermal_file.name)
    
        with open(file_path, "wb") as f:
            f.write(thermal_file.getbuffer())
        
        st.subheader("Uploaded image with annotations")
        
        img = draw_bounding_boxes(f"./uploads/{thermal_file.name}", thermals)
    
        st.image(img,caption="Thermal images", use_container_width=True)
        
        rois = [(103,54,27,11), (191,54,27,11)] #130,65
        rois_corner = [(282,6,30,16), (282,201,30,16)] #312,22
        
        minimum_temperature = 0
        maximum_temperature = 0
        try:
            minimum_temperature, maximum_temperature = get_min_max_temperatures("./uploads/"+thermal_file.name, rois, rois_corner)
        except ValueError:
            st.toast("An error occurred!", icon="❌")
            minimum_temperature = st.text_input("Enter your minimum temperature:", min_value=1, max_value=100)
            maximum_temperature = st.text_input("Enter your maximum temperature:", min_value=1, max_value=100)
        
        temperatures = extract_temperature_from_ironbow("./uploads/"+thermal_file.name, therm_coords, maximum_temperature, minimum_temperature)
            
        peaks = []
        for (resistor, temperature) in zip(thermals, temperatures):
            st.write(f"{resistor} : Mean = {temperature[0]} peak = {temperature[1]}") 
            peaks.append(temperature[1])   
            if resistor == "R1":
                if temperature[1]<ALLOWABLE_THRESHOLDS[0]  or (temperature[0]<ALLOWABLE_THRESHOLDS[0]) :
                    st.markdown("<p style='color: red;'>R1 might be open</p>", unsafe_allow_html=True)
            elif resistor == "R2":
                if temperature[1]<ALLOWABLE_THRESHOLDS[1]  or (temperature[0]<ALLOWABLE_THRESHOLDS[1]):
                    st.markdown("<p style='color: red;'>R2 might be open</p>", unsafe_allow_html=True)
            elif resistor == "R3":
                if temperature[1]<ALLOWABLE_THRESHOLDS[2]  or (temperature[0]<ALLOWABLE_THRESHOLDS[2]):
                    st.markdown("<p style='color: red;'>R3 might be open</p>", unsafe_allow_html=True)
            elif resistor == "R4":
                if (temperature[1]<ALLOWABLE_THRESHOLDS[3]) or (temperature[0]<ALLOWABLE_THRESHOLDS[3]):
                    st.markdown("<p style='color: red;'>R4 might be open</p>", unsafe_allow_html=True)

        return peaks
    
def draw_bounding_boxes(image_path, detections_dict):
    image = cv2.imread(image_path)
    print(f"{detections_dict=}")
    for tag, (xmin, ymin, xmax, ymax) in detections_dict.items():
        # print("{tag=}, {xmin=}, {ymin=}, {xmax=}, {ymax=}")
        # Draw the bounding box (color: green, thickness: 2)
        cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)

        # Add label above the bounding box (font: 0, scale: 0.7, color: white)
        cv2.putText(image, tag, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    return image


# Set the path where processed images are stored
PROCESSED_IMAGE_PATH = "processed_images/output.png"

st.title("Blaze")

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
        #ignore
        st.title("Missing resistors") 
        for problem in problems:
            # st.write(problem)
            st.markdown(f"<p style='color: red;'>{problem}</p>", unsafe_allow_html=True)
        print(f"{quadrant}: {box}")
        
    else:
        st.text("All resistors are available!\nProceeding to extraction of temperature")
        
        peaks = extract(q_new)
        r = 1
        
        st.title("Estimated lifetimes of resistors")
        for temperature in peaks:
        # operating_temperature = st.text_input("Enter operating temperature in Celsius: ")
            T_use = float(temperature)
            estimated_life = estimate_resistor_life(T_use)
            hours_per_year = 365.25 * 24
            years = estimated_life / hours_per_year
            st.write(f"Resistor {r} : {years:.2f} years")
            r+=1
            
    # Assuming 1 year = 365.25 days (including leap years)
            





