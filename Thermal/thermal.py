from roboflow import Roboflow

import cv2
import numpy as np

import pytesseract


def get_min_max_temperatures(image_path, rectangles, secondary):
    """
    Extracts text from specified rectangular regions in an image.

    :param image_path: Path to the image.
    :param rectangles: List of rectangles [(x, y, width, height)].
    :param secondary: List of rectangles [(x, y, width, height)].
    :return: List of extracted text strings for each rectangle.
    """
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image could not be loaded. Check the path and format.")

    extracted_texts = []
    
    for rect, sec in zip(rectangles, secondary):
        x, y, w, h = rect
        roi = image[y:y+h, x:x+w] 

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        config = "--oem 3 --psm 6"
        config += " -c tessedit_char_whitelist=0123456789"

        text = pytesseract.image_to_string(gray, config=config)

        
        if len(text.strip()) <3:
            # print(f"here {text=}")
            x, y, w, h = sec
            roi = image[y:y+h, x:x+w] 

            # gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            # _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            config = "--oem 3 --psm 13"
            config += " -c tessedit_char_whitelist=0123456789"

            text = pytesseract.image_to_string(roi, config=config)


        extracted_texts.append(text.strip())

    print(f"{extracted_texts=}")
    return parse_tesseract(extracted_texts)

def parse_tesseract(extracted_texts):
    op = []
    for text in extracted_texts:
        # if len(text) != 3:
        #     raise ValueError("Oops, an error occured, enter the temperature manually")
        text = int(text) / 10
        op.append(text)
    return op

def extract_temperature_from_ironbow(image_path, rectangles, temp_min, temp_max):

    """
    Extracts approximate temperature values from non-radiometric thermal images using Ironbow colormap.

    :param image_path: Path to the thermal image.
    :param rectangles: List of rectangles [(x, y, width, height)].
    :param temp_min: Minimum temperature in the scene (known from the thermal camera).
    :param temp_max: Maximum temperature in the scene (known from the thermal camera).
    :return: List of (mean_temperature, peak_temperature) for each rectangle.
    """
    # Load the Ironbow-colored thermal image
    print(f"{temp_min=}, {temp_max=}")
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image could not be loaded. Check the path and format.")

    # Convert Ironbow color to grayscale (assuming brightness ~ temperature)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Normalize grayscale intensity to temperature range
    temperature_image = np.interp(gray, (0, 255), (temp_min, temp_max))

    results = []

    for rect in rectangles:
        x, y, w, h = rect
        print(f"{x=},{y=},{w=},{h=}")
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)
        roi = temperature_image[y:y+h, x:x+w]  # Extract ROI

        mean_temp = np.mean(roi)
        peak_temp = np.max(roi)

        results.append((mean_temp, peak_temp))

    return results
    
def main():
    images = [
    "IR_00331.jpg","IR_00340.jpg", "IR_00339.jpg", "IR_00338.jpg", "IR_00337.jpg", 
    "IR_00336.jpg", "IR_00335.jpg", "IR_00334.jpg", "IR_00333.jpg", "IR_00332.jpg",
    "IR_00331.jpg"
    ]
    
    for image in images:
        # coords = get_resistor_coords( image)
        print(f"IMAGE : {image}")
        rois = [(103,54,27,11), (191,54,27,11)] #130,65
        rois_corner = [(282,6,30,16), (282,201,30,16)] #312,22
        try:
            # bounds = get_min_max_temperatures("og/"+image, rois_corner, rois )
            # print(bounds)
            
            coords = [(227,143,3,10),]
            # temperatures = extract_temperature_from_ironbow(image, coords, bounds[1], bounds[0])
            temperatures = extract_temperature_from_ironbow("/home/ajayh/Downloads/IR_00346.jpg", coords, 76.2, 27.3)

            for i, (mean_temp, peak_temp) in enumerate(temperatures):
                print(f"Region {i+1}: Mean Temp = {mean_temp:.2f}°C, Peak Temp = {peak_temp:.2f}°C")
        except ValueError as v:
            print(v)

        print("Done")

if __name__ == "__main__":
    main() 