import uuid
from database.connectSupaBase import get_supabase_client

supabase = get_supabase_client()

# Template for generating AI prompts
DEFAULT_PROMPT_TEMPLATE = (
    "This is the context: {history}. "
    "Now, you are a co-host. Based on the context provided, generate a swift, short, and engaging reply."
)

def create_context(personality_name,AI_PERSONALITIES):
    context_id = str(uuid.uuid4())
    initial_context = {
        "history": [],
        "current_topic": " ",
        "turn": " ",
        "personality_profile": {
            "name": personality_name,
            "traits": AI_PERSONALITIES[personality_name],
            "memory": []  # List of past interactions, feedback
        }
    }
    data = {
        "id": context_id,
        **initial_context
    }
    response = supabase.table("context").insert(data).execute()
    return response.data[0]

def get_context(context_id):
    response = supabase.table("context").select("*").eq("id", context_id).execute()
    if response.data:
        return response.data[0]
    return None

def update_context(context_id, updated_data):
    context = get_context(context_id)
    if context:
        try:
            # Append to memory if there's relevant feedback or context
            memory_update = updated_data.get("guidance", "")
            if memory_update:
                context["personality_profile"]["memory"].append(memory_update)
            
            # Update other context elements
            new_data = {**context, **updated_data}
            
            response = supabase.table("context").update(new_data).eq("id", context_id).execute()
            
            # Check for an error in the response object properly
            if hasattr(response, 'error') and response.error:
                raise ValueError(f"Error updating context: {response.error}")

        except Exception as e:
            print(f"Failed to update context with id {context_id}: {e}")
    else:
        print(f"Context with id {context_id} not found.")
def generate_prompt(context):
    history = " ".join([f"{message['speaker']}: {message['message']}" for message in context["history"]])
    prompt = DEFAULT_PROMPT_TEMPLATE.format(history=history)
    return prompt
