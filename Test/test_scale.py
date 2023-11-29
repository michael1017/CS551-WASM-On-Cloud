# Latency test
# Curl request (100) avg time
import random
import requests
import binascii
from time import perf_counter
import os
import threading
import base64

def convert_image_to_base64(file_name):
    base64_img = ""
    with open(file_name, 'rb') as img_file:
        # Read the image file
        img_data = img_file.read()
        # Encode image data to base64 string
        base64_img = base64.b64encode(img_data).decode('utf-8')
    return base64_img

def convert_image_to_hex(file_name):
    hex_value = ""
    with open(file_name, 'rb') as f:
        content = f.read()
    hex_value = str(binascii.hexlify(content), encoding="utf-8")
    return hex_value

def post_request(url_link, image):
    response = None
    if is_gcp_test:
        data = {
            "img": image
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url_link, headers=headers, json=data)
    else:
        response = requests.post(url_link, data=image)
    # print(response.text)

def scale_test(num_users, url_link):
    total_latency = 0
    image_hex = []
    for (dir_path, dir_names, file_names) in os.walk("Images"):        
        for file_name in file_names:
            file_path = dir_path + "/" + file_name
            if is_base64:
                image_hex.append(convert_image_to_base64(file_path))
            else:
                image_hex.append(convert_image_to_hex(file_path))

    threads = []

    start = perf_counter()
    for _ in range(num_users):
        image_object = random.choice(image_hex)
        thread = threading.Thread(post_request(url_link, image_object))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    end = perf_counter()
    total_latency = end - start
    
    # DO NOT DELETE
    # query = f"curl -X POST {url_link} -d {image_object}"
    # os.system(query)
    # print(response.text)

    print(total_latency)
    return total_latency

def record_data(url_link):
    return [(num_users, scale_test(num_users, url_link)) for num_users in [1, 10, 20, 30, 40, 50, 100]]        


is_gcp_test = False
is_base64 = False
if __name__ == "__main__":
    # AWS PYTHON
    # url_link = "https://xb28uuj612.execute-api.us-east-2.amazonaws.com/default/aws_lambda_classify_pytorch_wasm"
    
    # AWS WASM
    # url_link = "https://51wrp9c8ya.execute-api.us-east-1.amazonaws.com/default/classify"

    # AZURE MOBILENET
    # url_link = "https://classifytf2.azurewebsites.net/api/classify"
    
    # AZURE RESNET
    url_link = "https://newtestresnet.azurewebsites.net/api/httptrigger?code=ZrcylRyiNsbpXhkGnrPxideuF-QFwGh2e_iYlRqc3qBiAzFu3wfK_Q%3D%3D"
    is_gcp_test = True
    is_base64 = True
    
    # GCP 
    # url_link = "https://us-central1-curious-context-406603.cloudfunctions.net/function-1"
    # is_gcp_test = True

    print(url_link)
    print(record_data(url_link))
