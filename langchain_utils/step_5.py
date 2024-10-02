from utils.product_vertex import create_table, get_description, save_description
from utils_vertexai.generative_model_wrapper import GenerativeModelWrapper
from utils_vertexai.chat_input import part_image_url
import json

def process_images_with_vertex_ai(title, image_urls):
    # Ensure the database table exists
    create_table()

    image_descriptions = []
    model_wrapper = GenerativeModelWrapper()

    for url in image_urls:
        # Check if the description already exists
        description = get_description(url)
        if description:
            # Use the existing description
            image_descriptions.append({'url': url, 'description': description})
            continue

        # If not, generate the description using AI
        contents = []
        image_content = part_image_url(url)
        contents.append(image_content)
        contents.append("Please describe what information you would like to extract from the image.")
        description = model_wrapper.generate_content(contents=contents)
        image_descriptions.append({'url': url, 'description': description})

        # Save the new description to the database
        save_description(url, description)

    return image_descriptions

def process_relevant_docs(relevant_docs):
    image_descriptions = []
    
    for doc in relevant_docs:
        content = json.loads(doc.page_content)
        title = content.get('title', '')
        image_urls = doc.metadata.get('image_urls', '').split(',')
        descriptions = process_images_with_vertex_ai(title, image_urls)
        image_descriptions.extend(descriptions)       
    return image_descriptions