from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="IcGWxHMLBlniIr6s24b2"
)

image_url = "https://source.roboflow.com/pwYAXv9BTpqLyFfgQoPZ/u48G0UpWfk8giSw7wrU8/original.jpg"
result = CLIENT.infer("bus.jpg", model_id="soccer-players-5fuqs/1")
print(result)
# "american-sign-language-letters/6"