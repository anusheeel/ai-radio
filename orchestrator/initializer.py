from database.connectSupaBase import get_supabase_client
import json
# Initialize Supabase client
supabase = get_supabase_client()
def cleanResponse(data):
    extracted_messages = []
    for entry in data:
        message = entry['message']
        speaker = entry['speaker']
        
        # Skip entries where message is "None"
        if message == "None":
            continue
        
        # Try to parse JSON-like string within the message
        try:
            # Replace single quotes with double quotes for proper JSON parsing
            json_message = message.replace("'", '"')
            parsed_message = json.loads(json_message)
            # Extract the actual message content
            content = parsed_message['choices'][0]['message']['content']
        except (json.JSONDecodeError, KeyError):
            # If parsing fails, it's a regular message
            content = message
        
        extracted_messages.append({
            'speaker': speaker,
            'message': content
        })
    
    return str(extracted_messages)
def get_most_recent_message():
    # Query to get the most recent row from the "context" table based on "Updated_At"
    response = supabase.table("context") \
                   .select("history") \
                   .filter("history", "neq", 'null').order("Updated_At", desc=True).limit(1).offset(1).execute()      
    print(f"This is the data I got from Supsbase{response}")
    clean_response = cleanResponse(response)
    # Print the full response for debugging
    #print("Full Response:", response)


    # Check if the response has data
    if hasattr(clean_response, 'data') and clean_response.data:
        print("Data found:", clean_response.data)  # Debugging step to show the data
        most_recent_message = clean_response.data[0].get("message", None)
        if most_recent_message:
            return str(most_recent_message)
        else:
            print("No 'message' field in the returned data.")
            return None
    else:
        print("No data found or empty response.")
        return None
def initialize():
    most_recent_message = get_most_recent_message()
    if most_recent_message:
        return most_recent_message
def cleanResonse(data):
    extracted_messages = []
    for entry in data:
        message = entry['message']
        speaker = entry['speaker']
        
        # Skip entries where message is "None"
        if message == "None":
            continue
        
        # Try to parse JSON-like string within the message
        try:
            # Replace single quotes with double quotes for proper JSON parsing
            json_message = message.replace("'", '"')
            parsed_message = json.loads(json_message)
            # Extract the actual message content
            content = parsed_message['choices'][0]['message']['content']
        except (json.JSONDecodeError, KeyError):
            # If parsing fails, it's a regular message
            content = message
        
        extracted_messages.append({
            'speaker': speaker,
            'message': content
        })
    print(f"Iam inside clean_response function {extracted_messages}")
    return str(extracted_messages)

# Extract the clean messages and remove any with "None"
