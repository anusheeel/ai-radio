# personalities/claude.py
from base_personality import AIPersonality

class Claude(AIPersonality):
    def __init__(self):
        super().__init__("Claude", "thoughtful and introspective")
