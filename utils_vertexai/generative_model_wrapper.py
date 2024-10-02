import vertexai
from vertexai.generative_models import GenerativeModel

class GenerativeModelWrapper:
    def __init__(self, model_id='gemini-1.5-flash'):
        self.model_id = model_id
        self.model = GenerativeModel(model_id)

    def generate_content(self, contents):
        response = self.model.generate_content(
            contents=contents
        )
        return response.text
