# Pull the base image with python 3.8 as a runtime for your Lambda
FROM public.ecr.aws/lambda/python:3.8


# Copy the earlier created requirements.txt file to the container
COPY requirements.txt ./

# Install the python requirements from requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
# Replace Pillow with Pillow-SIMD to take advantage of AVX2

# Copy the earlier created app.py file to the containerworkspace/aws-lambda-wasm-runtime/api/Dockerfile
COPY hello.py ./
COPY labels_mobilenet_quant_v1_224.txt ./
COPY mobilenet_v1_1.0_224_quant.tflite ./

CMD [ "hello.lambda_handler" ]
