import requests
from vertexai.generative_models import Part

def part_image_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        file_type = response.headers['Content-Type']
        data = response.content
        part = Part.from_data(data=data, mime_type=file_type)
    else:
        print(f"Failed to retrieve image from {image_url}")   
    return part
