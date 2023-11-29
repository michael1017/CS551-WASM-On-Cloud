import functions_framework
import datetime
import json
import logging
from time import perf_counter

import os
import tensorflow as tf
import numpy as np
from PIL import Image
import requests
import io
import matplotlib.pyplot as plt
import sys

def solve(input_string):
    # Load the model
    model_path = 'classify/mobilenet_v1_1.0_224_quant.tflite'
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Load labels
    labels_path = 'classify/labels_mobilenet_quant_v1_224.txt'
    with open(labels_path, 'r') as f:
        labels = f.read().splitlines()

    # Read Image from URL
    # url = input_string
    # response = requests.get(url)
    # img = Image.open(io.BytesIO(response.content))

    # Read Image from input
    image_bytes = bytes.fromhex(input_string)
    img = Image.open(io.BytesIO(image_bytes))

    # Preprocess the image
    img = img.resize((224, 224))
    img = img.convert('RGB')
    img_array = np.array(img)

    # Prepare input tensor
    input_tensor = np.expand_dims(img_array, axis=0).astype(np.uint8)

    # Set input tensor
    input_details = interpreter.get_input_details()
    interpreter.set_tensor(input_details[0]['index'], input_tensor)

    # Run inference
    start_inference = perf_counter()
    interpreter.invoke()
    end_inference = perf_counter()
    print(f"model inference: {end_inference - start_inference} seconds")

    # Get output tensor
    output_details = interpreter.get_output_details()
    output_tensor = interpreter.get_tensor(output_details[0]['index'])

    # Process output tensor
    max_index = np.argmax(output_tensor)
    max_value = np.max(output_tensor)

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

    # Display result
    if max_value > 0.196:  # Adjust threshold as needed
        return f"It {confidence} a <a href='https://www.google.com/search?q={class_name}'>{class_name}</a> in the picture"

    return "It does not appear to be any food item in the picture."


@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    start_time = perf_counter()
    if request_json and 'img' in request_json:
        result = solve(request_json['img'])
    elif request_args and 'img' in request_args:
        result = solve(request_args['img'])
    else:
        result = 'No Match Handler'
    end_time = perf_counter()
    
    print(f"total time: {end_time - start_time}")
    return '{}'.format(result)
