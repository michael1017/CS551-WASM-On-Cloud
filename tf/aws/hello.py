import os
import tensorflow as tf
import numpy as np
from PIL import Image
import requests
import io
import matplotlib.pyplot as plt
import sys
import json

def solve(input_string):
    input_string = input_string[1:-1]
    print(input_string[:10])
    # Load the model
    model_path = 'mobilenet_v1_1.0_224_quant.tflite'
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Load labels
    labels_path = 'labels_mobilenet_quant_v1_224.txt'
    with open(labels_path, 'r') as f:
        labels = f.read().splitlines()

    # Read Image from input
    image_bytes = bytes.fromhex(input_string)
    img = Image.open(io.BytesIO(image_bytes))
    print('img')
    print(img)

    # Preprocess the image
    img = img.resize((224, 224))
    img = img.convert('RGB')
    img_array = np.array(img)
    print("img_array")
    print(img_array)

    # Prepare input tensor
    input_tensor = np.expand_dims(img_array, axis=0).astype(np.uint8)
    
    # Set input tensor
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]['index'], input_tensor)

    # Run inference
    interpreter.invoke()

    # Get output tensor
    output_details = interpreter.get_output_details()
    output_tensor = interpreter.get_tensor(output_details[0]['index'])

    # Process output tensor
    max_index = np.argmax(output_tensor)
    max_value = np.max(output_tensor)
    print("max_value")
    print(max_value)

    # Determine confidence
    confidence = "could be"
    if max_value > 0.784:  # Adjust confidence thresholds based on your needs
        confidence = "is very likely"
    elif max_value > 0.49:
        confidence = "is likely"
    elif max_value > 0.196:
        confidence = "could be"

    # Get class name
    class_name = labels[max_index]
    print("class_name")
    print(class_name)

    # Display result
    if max_value > 0.196:  # Adjust threshold as needed
        return f"It {confidence} a <a href='https://www.google.com/search?q={class_name}'>{class_name}</a> in the picture"

    return "It does not appear to be any food item in the picture."

def lambda_handler(event, context):
    # TODO implement
    temp = str(json.dumps(event['body'])).strip()
    print(temp)
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT"
        },
        'body': solve(temp)
    }
