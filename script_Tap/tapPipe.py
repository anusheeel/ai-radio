import re
from api_clients.meloTransformer import speaker1
def tapPipe(data):
    # Ensure the input is a string
    if not isinstance(data, str):
        print(f"Expected a string but got {type(data).__name__}")
        return None

    # Use a regular expression to find the 'content' value within the string
    try:
        # Regular expression to find the 'content' field and extract the value inside quotes
        content_match = re.search(r"'content':\s*\"(.*?)\"", data, re.DOTALL)

        if content_match:
            content = content_match.group(1)
            # Clean up any potential escaped characters or formatting issues
            cleaned_script_dialogue = content.strip().replace('\\n', '\n').replace('\\"', '"')
            return cleaned_script_dialogue
        else:
            raise ValueError("Content field not found")

    except Exception as e:
        print(f"Error while extracting content: {e}")
        return None
