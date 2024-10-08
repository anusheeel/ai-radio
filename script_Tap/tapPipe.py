import re
import json

def tapPipe(data):
    # Check if data is a string or dictionary-like structure
    if not isinstance(data, str):
        print(f"Expected a string but got {type(data).__name__}")
        return None

    try:
        # Attempt to find the 'content' field within the input string
        content_match = re.search(r"'content':\s*['\"](.*?)['\"](?=\s*[,}])", data, re.DOTALL)

        if content_match:
            # Extract the content part
            content = content_match.group(1)

            # Further clean up the text by handling common formatting issues
            cleaned_script_dialogue = (
                content.strip()
                .replace('\\n', '\n')  # Handle newlines
                .replace('\\"', '"')    # Handle escaped double quotes
                .replace('\\\\', '\\')  # Handle escaped backslashes
            )

            # Return the fully cleaned dialogue
            return cleaned_script_dialogue

        else:
            raise ValueError("Content field not found")

    except Exception as e:
        print(f"Error while extracting content: {e}")
        return None
