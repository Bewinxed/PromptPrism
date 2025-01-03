from .src.prompt_parser import CharacterPromptParser, CharacterPromptMerger

NODE_CLASS_MAPPINGS = {
    "PromptParser": CharacterPromptParser,
    "PromptMerger": CharacterPromptMerger,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptParser": "Character Prompt Parser 🌈⃤",
    "PromptMerger": "Character Prompt Merger 🌈⃤",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
