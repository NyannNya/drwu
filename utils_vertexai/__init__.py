import vertexai
from google.oauth2 import service_account
from config import Config

# Load credentials from the service account JSON file
credentials = service_account.Credentials.from_service_account_file(Config.GOOGLE_APPLICATION_CREDENTIALS)

# Initialize Vertex AI with custom credentials
vertexai.init(
    project=Config.BIGQUERY_PROJECT_ID,
    location='us-central1',
    credentials=credentials
)
