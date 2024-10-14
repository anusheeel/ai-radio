import json
import re

def extract_relevant_information(api_response):
    """
    Extracts relevant information from the API response and returns it as a dictionary.
    Assumes input is of type <class 'dict'> or a JSON string.
    
    Parameters:
    - api_response (dict or str): The API response in JSON format or string.
    
    Returns:
    - dict: Dictionary of relevant fields to be stored in the database.
    """
    response_dict = None
    
    # Check if the input is a string (JSON), and convert to dict if needed
    if isinstance(api_response, str):
        try:
            # Fix single quotes by replacing them with double quotes for valid JSON
            api_response = re.sub(r"'", '"', api_response)  # Replace single quotes with double quotes
            response_dict = json.loads(api_response)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            raise ValueError("Invalid JSON string: Make sure the response is a valid JSON format.")
    elif isinstance(api_response, dict):
        response_dict = api_response
    else:
        raise ValueError("Unsupported response format: Only dict or JSON string is supported")

    # Proceed only if the response is properly parsed into a dictionary
    if response_dict is None:
        raise ValueError("The response could not be processed as a dictionary.")

    # Extract relevant information
    conversation_id = response_dict.get('id', '')
    provider = response_dict.get('provider', '')
    model = response_dict.get('model', '')
    object_type = response_dict.get('object', '')
    created_at = response_dict.get('created', '')
    message_content = response_dict['choices'][0]['message']['content'] if 'choices' in response_dict else ''
    prompt_tokens = response_dict['usage']['prompt_tokens'] if 'usage' in response_dict else 0
    completion_tokens = response_dict['usage']['completion_tokens'] if 'usage' in response_dict else 0
    total_tokens = response_dict['usage']['total_tokens'] if 'usage' in response_dict else 0

    # Return as a dictionary to store in the database
    relevant_data = {
        'conversation_id': conversation_id,
        'provider': provider,
        'model': model,
        'object_type': object_type,
        'created_at': created_at,
        'message_content': message_content,
        'prompt_tokens': prompt_tokens,
        'completion_tokens': completion_tokens,
        'total_tokens': total_tokens
    }

    return relevant_data
