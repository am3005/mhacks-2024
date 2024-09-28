# import the inference-sdk
from inference_sdk import InferenceHTTPClient

# initialize the client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="IcGWxHMLBlniIr6s24b2"
)

# infer on a local image
result = CLIENT.infer("chanterelle.jpg", model_id="intro-mushroom-classification/1")
print(result)