# Latency test
# Curl request (100) avg time
import random
import requests
import binascii
from time import perf_counter
import os
import threading


def convert_image_to_hex(file_name):
    hex_value = ""
    with open(file_name, 'rb') as f:
        content = f.read()
    hex_value = str(binascii.hexlify(content), encoding="utf-8")
    return hex_value

def post_request(url_link, image):
    response = requests.post(url_link, data=image)

def scale_test(num_users, url_link):
    total_latency = 0
    image_hex = []
    for (dir_path, dir_names, file_names) in os.walk("Images"):        
        for file_name in file_names:
            file_path = dir_path + "/" + file_name
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


if __name__ == "__main__":
    url_link = "https://xb28uuj612.execute-api.us-east-2.amazonaws.com/default/aws_lambda_classify_pytorch_wasm"
    print(url_link)
    print(record_data(url_link))