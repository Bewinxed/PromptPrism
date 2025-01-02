from .src.prompt_parser import (
    CharacterPromptParser,
)

NODE_CLASS_MAPPINGS = {"PromptParser": CharacterPromptParser}

NODE_DISPLAY_NAME_MAPPINGS = {"PromptParser": "Character Prompt Parser"}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
