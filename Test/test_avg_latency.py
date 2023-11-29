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
        response = requests.post(url_link, data=image_object)
        # print(response.text)
        end = perf_counter()

        avg_latency += (end - start)
    avg_latency /= num_requests
    print(avg_latency)
    return avg_latency


# Function Ananlysis
# Cost Analysis
# Find cost in AWS, Azure, GCP
def record_data(url_link):
    return [(num_requests, test_latency(num_requests, url_link)) for num_requests in [1, 10, 20, 30, 40, 50, 100]]        


if __name__ == "__main__":
    url_link = "https://xb28uuj612.execute-api.us-east-2.amazonaws.com/default/aws_lambda_classify_pytorch_wasm"
    print(url_link)

    print(record_data(url_link))