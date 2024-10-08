# personalities/base_personality.py
import random
from database.context_manager import create_context, get_context, update_context, generate_prompt
import json
from personalities.director_client import RadioDirector  # Assuming `director.py` is where `RadioDirector` is defined

AI_PERSONALITIES = {
    "humanGPT": {
        "style": "Playful, energetic, humorous.",
        "traits": {
            "positivity": 7,
            "curiosity": 8,
            "seriousness": 3
        }
    },
    "humanClaude": {
        "style": "Reflective, calm, insightful.",
        "traits": {
            "positivity": 5,
            "curiosity": 6,
            "seriousness": 8
        }
    },
    # Add more personalities as required
}


PROMPT_TEMPLATES = {
    "Introduction": (
        "This is the context: {history}. "
        "Now, introduce yourself and engage in a welcoming and friendly tone."
    ),
    "Debate": (
        "This is the context: {history}. "
        "Take a side in the conversation, adding humor or passion as needed."
    ),
    "Light Chat": (
        "This is the context: {history}. "
        "Continue the conversation in a relaxed and friendly manner."
    )
}
# Define roles for each AI personality
roles = {
    "AI1": "Radio Host (RH): Introduce topics, guide the conversation, and engage the audience.",
    "AI2": "Guest (PJ): Share insights, respond to the host, and contribute to discussions naturally."
}
def trim_context(history, max_length=500):
    """Trim the conversation history to the last 'max_length' characters."""
    return history[-max_length:]

# Initialize RadioDirector
director = RadioDirector()
def generate_prompt(context, guidance=None):
    # Trim conversation history to last 5 exchanges or a maximum of 500 characters
    history_text = " ".join([f"{message['speaker']}: {message['message']}" for message in context["history"][-5:]])
    trimmed_history = trim_context(history_text, max_length=500)
    
    # Use RadioDirector to mediate and analyze the conversation
    director_output = director.mediate_conversation(context)
    current_guidance = director_output.get("guidance", {})
    current_topic = director_output.get("current_topic", "General Discussion")
    next_turn = director_output.get("turn", "AI1")

    # Check if any specific guidance was provided in function call
    if guidance:
        current_guidance["additional"] = guidance
    # Determine the next speaker's role based on director's output or current context
    next_speaker = "humanGPT" if next_turn == "AI1" else "humanClaude"
    
    # Build the prompt based on context, guidance, and topic
    prompt = f"This is the context of the conversation on the topic '{current_topic}': {trimmed_history}\n"
    prompt += f"Guidance: {current_guidance}\n"
    # In the generate_prompt function
    prompt += f"{next_speaker}, you are the next speaker. Only respond as {next_speaker} and do not attempt to generate content for other speakers.\n"
    
    # Add a cue for the next speaker to respond
    cue = director.provide_role_specific_cue(next_speaker, context)
    prompt += f"{next_speaker}, {cue}\n" 
    return prompt
def start_conversation(personality_name):
    context = create_context(personality_name,AI_PERSONALITIES)
    context_id = context["id"]
    return context_id

import json
import re
import json
import re

import json

def sanitize_message_content(content):
    """Sanitize and clean up message content for proper processing."""
    if isinstance(content, str):
        # Trim whitespaces, remove special characters if needed
        content = content.strip()
    return content

def handle_ai_response(context_id, ai_response, speaker):
    current_context = get_context(context_id)
    #print(f"Current context before update: {current_context}")
    
    # Log the raw AI response for debugging
    #print(f"Raw AI response: {ai_response}")
    ai_response = normalize_ai_response(ai_response)
    
    try:
        # Check if ai_response is a dict (expected structured response)
        if isinstance(ai_response, dict) and "choices" in ai_response:
            # Extract the 'content' from the 'choices' field
            choices = ai_response['choices']
            if len(choices) > 0 and 'message' in choices[0]:
                message_content = choices[0]['message']['content']
            else:
                raise ValueError("AI response 'choices' array is empty or missing 'message'.")
        
        # If ai_response is plain text, treat it directly as content
        elif isinstance(ai_response, str):
            message_content = ai_response.strip()

        else:
            raise ValueError("AI response structure is not as expected.")

        # Append the relevant message content to context history
        new_message = {"speaker": speaker, "message": message_content}
        current_context["history"].append(new_message)

        # Toggle turn: Assuming '0' for humanGPT and '1' for humanClaude
        next_turn = 0 if current_context.get("turn") == 1 else 1

        # Update context with the new history and turn
        updated_data = {
            "history": current_context["history"],
            "turn": next_turn
        }

        # Save the updated context
        update_context(context_id, updated_data)
        #print(f"Context after update: {get_context(context_id)}")

    except (KeyError, IndexError, ValueError) as e:
        # Handle error with parsing and provide a default error message
        print(f"Failed to parse AI response JSON: {e}")
        # Append an error message to the context history
        current_context["history"].append({"speaker": "system", "message": "ERROR: Failed to parse AI response."})
        update_context(context_id, {"history": current_context["history"]})

def normalize_ai_response(ai_response):
    # If ai_response is a string, wrap it in a dict structure
    if isinstance(ai_response, str):
        return {
            "choices": [
                {
                    "message": {
                        "content": ai_response.strip()
                    }
                }
            ]
        }
    elif isinstance(ai_response, dict) and "choices" in ai_response:
        # Check for message content presence in choices
        for choice in ai_response['choices']:
            if 'message' not in choice or 'content' not in choice['message']:
                return {
                    "choices": [
                        {
                            "message": {
                                "content": "ERROR: Invalid AI response format."
                            }
                        }
                    ]
                }
        return ai_response
    else:
        # Return a default error structure if the response is unexpected
        return {
            "choices": [
                {
                    "message": {
                        "content": "ERROR: Unrecognized AI response format."
                    }
                }
            ]
        }


    
def determine_topic(history):
    """Simple function to determine conversation topic based on history."""
    if any("debate" in msg["message"].lower() for msg in history):
        return "Debate"
    return "Light Chat"