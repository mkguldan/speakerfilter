"""
Google Secret Manager integration.
Fetches secrets from Google Cloud Secret Manager.
"""
import os
from google.cloud import secretmanager


def get_secret(secret_id, project_id="speakerfilter"):
    """
    Fetch a secret from Google Secret Manager.
    
    Args:
        secret_id: The ID of the secret (e.g., 'AIRTABLE_API_KEY')
        project_id: GCP project ID
        
    Returns:
        str: The secret value
    """
    # For local development, fall back to environment variables
    if os.getenv('USE_LOCAL_ENV') == 'true':
        return os.getenv(secret_id)
    
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        # Fallback to environment variable if Secret Manager fails
        print(f"Warning: Could not fetch secret {secret_id} from Secret Manager: {e}")
        print(f"Falling back to environment variable")
        return os.getenv(secret_id)



