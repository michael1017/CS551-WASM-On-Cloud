# Latency test
# Curl request (100) avg time
import random
import requests
import binascii
from time import perf_counter
import os


def convert_image_to_hex(file_name):
    hex_value = ""
    with open(file_name, 'rb') as f:
        content = f.read()
    hex_value = str(binascii.hexlify(content), encoding="utf-8")
    return hex_value

def test_latency(num_requests, url_link):
    avg_latency = 0
    image_hex = []
    times = []
    for (dir_path, dir_names, file_names) in os.walk("Images"):        
        for file_name in file_names:
            file_path = dir_path + "/" + file_name
            image_hex.append(convert_image_to_hex(file_path))

    for _ in range(num_requests):
        image_object = random.choice(image_hex)
        # DO NOT DELETE
        # query = f"curl -X POST {url_link} -d {image_object}"
        # os.system(query)
        start = perf_counter()
        # FOR GCP AND AZURE DO THE FOLLOWING SAME IN SCALE TEST
        # image_object = {"img": image_object}
        # response = requests.post(url_link,json=image_object)
        
        response = None
        if is_gcp_test:
            data = {
                "img": image_object
            }
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post(url_link, headers=headers, json=data)
        else:
            response = requests.post(url_link, data=image_object)
        # print(response.text)
        end = perf_counter()

        times.append((end - start))
        # avg_latency += (end - start)
    avg_latency = sum(times)
    # variance(times)
    avg_latency /= num_requests
    print(avg_latency)
    return avg_latency


# Function Ananlysis
# Cost Analysis
# Find cost in AWS, Azure, GCP
def record_data(url_link):
    return [(num_requests, test_latency(num_requests, url_link)) for num_requests in [1, 10, 20, 30, 40, 50, 100]]        


is_gcp_test = False
if __name__ == "__main__":
    # REPLACE URL with GCP and AZURE
    # url_link = "https://xb28uuj612.execute-api.us-east-2.amazonaws.com/default/aws_lambda_classify_pytorch_wasm"
    
    # AWS WASM
    # url_link = "https://51wrp9c8ya.execute-api.us-east-1.amazonaws.com/default/classify"

    # AZURE MOBILENET
    # url_link = "https://classifytf2.azurewebsites.net/api/classify"
    
    # GCP MOBILENET
    url_link = "https://us-central1-curious-context-406603.cloudfunctions.net/function-1"
    is_gcp_test = True

    print(url_link)
    print(record_data(url_link))
