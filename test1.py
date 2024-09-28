from roboflow import Roboflow

# Initialize Roboflow with your API key
rf = Roboflow(api_key="IcGWxHMLBlniIr6s24b2")

# Load your workspace and project
project = rf.workspace().project("your-project-name")
model = project.version(1).model
prediction = model.predict("bus.jpg")
print(prediction.json())
prediction.save("path/to/save/annotated_image.jpg")