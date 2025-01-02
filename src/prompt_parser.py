from typing import Dict, List, Optional, Literal
from instructor import OpenAISchema, from_litellm
from pydantic import Field
import json
from openai import OpenAI
from litellm import acompletion
from pydantic import BaseModel

Providers = Literal["openai", "anthropic", "deepseek", "ollama"]
ProviderToModels: Dict[str, List[str]] = {
    "openai": [
        "o1-mini",
        "o1-preview",
        "gpt-4o-mini",
        "gpt-4o-mini-2024-07-18",
        "gpt-4o",
        "gpt-4o-2024-08-06",
        "gpt-4o-2024-05-13",
        "gpt-4-turbo",
        "gpt-4-0125-preview",
        "gpt-4-1106-preview",
        "gpt-3.5-turbo-1106",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4",
        "gpt-4-0314",
        "gpt-4-0613",
        "gpt-4-32k",
        "gpt-4-32k-0314",
        "gpt-4-32k-0613",
    ],
    "anthropic": [
        "claude-3-5-sonnet",
        "claude-3-haiku",
        "claude-3-opus",
        "claude-3-5-sonnet-20240620",
        "claude-3-sonnet",
        "claude-2.1",
        "claude-2",
        "claude-instant-1.2",
        "claude-instant-1",
    ],
    "deepseek": ["deepseek-chat", "deepseek-coder"],
    "ollama": [
        "mistral",
        "mistral-7B-Instruct-v0.1",
        "mistral-7B-Instruct-v0.2",
        "mixtral-8x7B-Instruct-v0.1",
        "mixtral-8x22B-Instruct-v0.1",
        "llama2",
        "llama2:13b",
        "llama2:70b",
        "llama2-uncensored",
        "codellama",
        "llama3",
        "llama3:70b",
        "orca-mini",
        "vicuna",
        "nous-hermes",
        "nous-hermes:13b",
        "wizard-vicuna",
    ],
}


class Character(BaseModel):
    quality: List[str] = Field(
        description="List of quality tags for the character description"
    )
    clothes: List[str] = Field(
        description="List of clothing items worn by the character"
    )
    hair: List[str] = Field(
        description="Hair characteristics including color, length, style"
    )
    expression: List[str] = Field(
        default_factory=list, description="Facial expressions and emotions"
    )
    body: List[str] = Field(default_factory=list, description="Body characteristics")
    pose: List[str] = Field(default_factory=list, description="Body pose and position")
    accessories: List[str] = Field(
        default_factory=list, description="Accessories worn by the character"
    )
    background: List[str] = Field(
        default_factory=list, description="Background description"
    )
    composition: List[str] = Field(
        default_factory=list, description="Composition of the scene"
    )


class CharacterPromptParser:
    CATEGORY: str
    FUNCTION: str
    RETURN_TYPES: tuple
    RETURN_NAMES: tuple

    def __init__(self):
        self.CATEGORY = "parsing"
        self.FUNCTION = "parse_prompt"
        # Dynamically get field names from Character class
        self.RETURN_TYPES = tuple("STRING" for _ in Character.model_fields)
        self.RETURN_NAMES = tuple(Character.model_fields.keys())

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "provider": (list(ProviderToModels.keys()), {"default": "openai"}),
                "model": ("STRING", {"default": "gpt-3.5-turbo"}),
                "api_key": ("STRING", {"default": ""}),
                "temperature": (
                    "FLOAT",
                    {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1},
                ),
            }
        }

    async def parse_prompt(
        self,
        prompt: str,
        provider: str,
        model: str,
        api_key: str,
        temperature: float = 1,
    ) -> tuple:
        model_str = (
            f"{provider}/{model}" if provider in ["deepseek", "ollama"] else model
        )
        client = from_litellm(acompletion)

        character: Character = await client.chat.completions.create(
            model=model_str,
            messages=[
                {
                    "role": "system",
                    "content": "Parse the character description into structured data.",
                },
                {"role": "user", "content": prompt},
            ],
            response_model=Character,
            temperature=temperature,
            api_key=api_key,
        )

        return tuple(
            json.dumps(getattr(character, field)) for field in self.RETURN_NAMES
        )

    # Add custom update method to handle dynamic model dropdown
    FUNCTION = "update"

    def update(self):
        return ProviderToModels[self.provider]


# Run async function
character = CharacterPromptParser()
if __name__ == "__main__":
    import asyncio

    character = asyncio.run(
        CharacterPromptParser().parse_prompt(
            """score_9, score_8_up, score_7_up, source_anime,
        1girl, breast_curtains, very_long_hair, (blue_hair:1.2), long_hair, red_eyes, looking_at_viewer, smile, simple_background, white_background, solo, upper_body, fur-trimmed_capelet, fur_trim, white_capelet, capelet, white_dress, bowtie, cute_face, eyeliner, curly_hair, light_blue_hair, mini_witch_hat, neutral""",
            provider="deepseek",
            model="deepseek-chat",
            api_key="sk-fc122a11b4fc46778021c08c50727f1d",
        )
    )
    print(character)
