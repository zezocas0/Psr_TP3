#!/usr/bin/env python3

# import required packages
import cv2
import argparse
import numpy as np

def load_model(config_file, weights_file, classes_file):
    print("[INFO] loading network...")

    # load the model from disk
    net = cv2.dnn.readNet(weights_file, config_file)

    # set neural network parameters
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1/255)

    # load the classes from disk
    with open(classes_file, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    print("[INFO] network loaded successfully...")
    return model, net, classes

# function to get the output layer names 
# in the architecture
def get_output_layers(net):
    
    layer_names = net.getLayerNames()

    output_layers = []
    for i in net.getUnconnectedOutLayers():
        idx = i[0]
        output_layers.append(layer_names[idx-1])

    return output_layers

# function to draw bounding box on the detected object with class name
def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h, COLORS, classes):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return img

# YOLO V4 TINY APPROACH
def detect(image, model, net, classes):    
        print("[INFO] detecting objects...")
    
        # generate different colors for different classes 
        COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
    
        # detect objects in the input image
        class_ids, confidences, boxes = model.detect(image, confThreshold=0.1, nmsThreshold=0.2)
        print("class_id: ", class_ids)
        print("confidence: ", confidences)
        print("box: ", boxes)
        # draw bounding box on the detected object with class name
        for (class_id, confidence, box) in zip(class_ids, confidences, boxes):
            class_id = class_id[0]
            print("class_id: ", class_id)
            print("confidence: ", confidence)
            print("box: ", box)
            label = "%s : %f" % (classes[class_id], confidence)
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            left, top, width, height = box
            top = max(top, labelSize[1])
            image = draw_bounding_box(image, class_id, confidence, left, top, left + width, top + height, COLORS, classes)
    
        return image

# YOLO V3 APPROACH
# def detect(image, model, net, classes):
#     image = cv2.imread("YOLO/text.png")
#     print("[INFO] detecting objects...")

#     Width = image.shape[1]
#     Height = image.shape[0]
#     scale = 0.00392

#     # generate different colors for different classes 
#     COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

#     # create input blob 
#     blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

#     # set input blob for the network
#     net.setInput(blob)

#     # run inference through the network
#     # and gather predictions from output layers
#     outs = net.forward(get_output_layers(net))

#     # initialization
#     class_ids = []
#     confidences = []
#     boxes = []
#     conf_threshold = 0.5
#     nms_threshold = 0.4

#     # for each detetion from each output layer 
#     # get the confidence, class id, bounding box params
#     # and ignore weak detections (confidence < 0.5)
#     for out in outs:
#         for detection in out:
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]
#             if confidence > 0.5:
#                 center_x = int(detection[0] * Width)
#                 center_y = int(detection[1] * Height)
#                 w = int(detection[2] * Width)
#                 h = int(detection[3] * Height)
#                 x = center_x - w / 2
#                 y = center_y - h / 2
#                 class_ids.append(class_id)
#                 confidences.append(float(confidence))
#                 boxes.append([x, y, w, h])

#     # apply non-max suppression
#     indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

#     # go through the detections remaining
#     # after nms and draw bounding box
#     for i in indices:
#         i = i[0]
#         box = boxes[i]
#         x = box[0]
#         y = box[1]
#         w = box[2]
#         h = box[3]

#         image = draw_bounding_box(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h), COLORS, classes)
    
#     return image
    
#     # # display output image    
#     # cv2.imshow("object detection", image)

#     # # wait until any key is pressed
#     # cv2.waitKey()