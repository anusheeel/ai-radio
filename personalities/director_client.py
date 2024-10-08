import json
import os
import random
from database.context_manager import get_context, update_context
from database.connectSupaBase import get_supabase_client

supabase = get_supabase_client()

class RadioDirector:
    def __init__(self, knowledge_base_dir="knowledgeBase/"):
        self.knowledge_base_dir = knowledge_base_dir
        self.knowledge = self.load_knowledge()

    def load_knowledge(self):
        knowledge = {}
        for filename in os.listdir(self.knowledge_base_dir):
            file_path = os.path.join(self.knowledge_base_dir, filename)
            if filename.endswith(".json"):
                with open(file_path, "r") as file:
                    knowledge[filename[:-5]] = json.load(file)  # Remove .json extension
            elif filename.endswith(".txt"):
                with open(file_path, "r") as file:
                    knowledge[filename[:-4]] = file.read()  # Remove .txt extension
        return knowledge

    def mediate_conversation(self, current_context):
        """
        Use the current context and knowledge base to guide the conversation.
        Identify the current segment and provide guidance on transitioning to the next one.
        """
        segment_info = self.knowledge.get('segment_structuring', {})
        last_topic = current_context.get("current_topic", "")
        conversation_history = current_context.get("history", [])
        
        # Check if it's time to transition to a new segment based on context
        if self.should_transition(last_topic, conversation_history):
            next_segment = self.select_next_segment()
            guidance = self.knowledge.get('guidance_by_segment', {}).get(next_segment, {})
            return {
                "current_topic": next_segment,
                "guidance": guidance,
                "turn": "AI1"  # Decide which AI will start the new segment
            }
        return {
            "current_topic": last_topic,
            "guidance": segment_info.get(last_topic, {}),
            "turn": current_context.get("turn", "AI1")
        }

    def should_transition(self, last_topic, conversation_history):
        """
        Decide if a conversation should transition to a new segment.
        You can enhance this logic based on length, content, or specific cues.
        """
        # Transition every 5 exchanges or based on cues
        if len(conversation_history) >= 5:
            return True
        
        # Other logic: keyword detection, content analysis
        # Example: Check for keywords indicating completion of a segment
        segment_endings = self.knowledge.get('segment_endings', [])
        for message in conversation_history[-5:]:
            if any(ending in message['message'].lower() for ending in segment_endings):
                return True
        
        return False

    def select_next_segment(self):
        """
        Select the next segment or theme based on predefined logic.
        Randomly pick a segment from the knowledge base or fallback to 'general_discussion'.
        """
        segment_list = list(self.knowledge.get('segment_structuring', {}).keys())
        return random.choice(segment_list) if segment_list else "general_discussion"

    def get_guidance_for_host(self, host_role):
        """
        Provide specific guidance to each host based on their role and traits.
        """
        traits = self.knowledge.get('host_traits', {})
        return traits.get(host_role, traits.get('default', {}))
    
    def provide_role_specific_cue(self, host_role, context):
        """
        Provide a specific cue or nudge for a host to steer the conversation.
        """
        role_guidance = self.get_guidance_for_host(host_role)
        cues = role_guidance.get('cues', [])
        return random.choice(cues) if cues else "Keep the conversation flowing naturally."

    def analyze_conversation_flow(self, context):
        """
        Perform analysis on the flow of the conversation, ensuring it aligns with intended dynamics.
        Identify if a host is monopolizing the conversation or if certain themes are being over-discussed.
        """
        history = context.get("history", [])
        speaker_count = {msg.get("speaker"): 0 for msg in history}

        # Count speaker occurrences
        for message in history:
            speaker = message.get("speaker", "unknown")
            speaker_count[speaker] += 1

        dominant_speaker = max(speaker_count, key=speaker_count.get)
        if speaker_count[dominant_speaker] > len(history) * 0.6:
            return f"Balance the conversation by allowing the other host to speak more."

        return "The conversation flow is balanced."

    def analyze_and_evolve_personality(self, context_id):
        context = get_context(context_id)
        history = context.get("history", [])
        speaker_count = {msg.get("speaker"): 0 for msg in history}

        # Count occurrences of each speaker
        for message in history:
            speaker = message.get("speaker", "unknown")
            speaker_count[speaker] += 1

        # Identify dominant speaker
        dominant_speaker = max(speaker_count, key=speaker_count.get)
        if speaker_count[dominant_speaker] > len(history) * 0.6:
            return "Balance the conversation by allowing the other host to speak more."

        return "The conversation flow is balanced."

    def update_personality_traits(self, context_id, feedback):
        context = get_context(context_id)
        personality_profile = context.get("personality_profile", {})
        traits = personality_profile.get("traits", {})
        
        # Modify personality traits based on feedback
        if feedback == "positive":
            traits["style"] += ", more friendly"
        elif feedback == "negative":
            traits["style"] += ", more reflective"
        
        # Update the context in the database
        updated_data = {"personality_profile": {"traits": traits}}
        update_context(context_id, updated_data)
