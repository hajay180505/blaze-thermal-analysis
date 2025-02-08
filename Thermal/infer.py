from inference import get_model
import supervision as sv
import cv2


def get_inference(image_file :str, saveImage : bool = True) -> sv.Detections :
    
    print(image_file)

    # image_file = "/home/ajayh/Downloads/Resistors.v2i.yolov8/valid/images/IR_00414_jpg.rf.bb51e2fd4727b2c044c1d3a4d536321d.jpg"
    # image_file = "/home/ajayh/Downloads/IR_00486.jpg"
    image = cv2.imread(image_file)

    # load a pre-trained yolov8n model
    model = get_model(model_id="resistors-dooos/2")

    # run inference on our chosen image, image can be a url, a numpy array, a PIL image, etc.
    results = model.infer(image)[0]

    # load the results into the supervision Detections api
    detections = sv.Detections.from_inference(results)

    print(detections.xyxy)
    


    # create supervision annotators
    bounding_box_annotator = sv.BoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    # annotate the image with our inference results
    annotated_image = bounding_box_annotator.annotate(
        scene=image, detections=detections)
    # annotated_image = label_annotator.annotate(
    #     scene=annotated_image, detections=detections)

    # display the image
    # sv.plot_image(annotated_image)
    "sda".lstrip("./uploads/")
    
    output_path = f"./predictions/predicted_{image_file.lstrip('./uploads/')}"
    print(output_path)
    if saveImage : 
        print("About to save")
        cv2.imwrite(output_path, annotated_image )
        
    return detections

