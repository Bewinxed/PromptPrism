import json
from typing import Dict, List, Literal

from instructor import from_litellm
from litellm import completion
from pydantic import BaseModel, Field

from .model_config import PROVIDER_MODELS

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

field_emojis = {
    "eyes": "👀",
    "quality": "🌟",
    "clothes": "👗",
    "hair": "💇",
    "expression": "😊",
    "body": "👤",
    "pose": "🕺",
    "accessories": "🕶️",
    "background": "🏞️",
    "composition": "🖼️",
    "character": "👤",
    "gender": "🚻",
    "species": "🐾",
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
    eyes: List[str] = Field(description="Eye characteristics including color, shape")
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
    gender: List[str] = Field(
        default_factory=list, description="Gender of the character, if specified"
    )
    species: List[str] = Field(
        default_factory=list, description="Species of the character, if specified"
    )
    age: List[str] = Field(
        default_factory=list, description="Age of the character, if specified"
    )
    name: List[str] = Field(
        default_factory=list, description="Name of the character, if specified"
    )


class CharacterPromptParser:
    CATEGORY = "splitters"
    FUNCTION = "parse_prompt"
    RETURN_TYPES: tuple[Literal["STRING"], ...] = tuple(
        ["STRING" for _ in Character.model_fields] + ["CHARACTER"]
    )
    RETURN_NAMES: tuple[str, ...] = tuple(
        list(
            [
                f"{field} {field_emojis.get(field, '')}"
                for field in Character.model_fields.keys()
            ]
        )
        + ["character"]
    )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                # "provider": (list(PROVIDER_MODELS.keys()), {"default": "openai"}),
                "model": (
                    (
                        [
                            f"{provider}/{model}"
                            for provider, models in PROVIDER_MODELS.items()
                            for model in models
                        ]
                    ),
                    {"default": "gpt-4-turbo"},
                ),
                "api_key": ("STRING", {"default": ""}),
                "temperature": (
                    "FLOAT",
                    {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1},
                ),
            }
        }

    @classmethod
    def VALIDATE_INPUTS(cls, provider=None, model=None):
        # if model not in ProviderToModels[provider]:
        #     return f"Model {model} is not valid for provider {provider}"
        return True

    def parse_prompt(
        self,
        prompt: str,
        # provider: str,
        model: str,
        api_key: str,
        temperature: float = 1,
    ) -> tuple:
        # model_str = (
        #     f"{provider}/{model}" if provider in ["deepseek", "ollama"] else model
        # )
        client = from_litellm(completion)

        character = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Input is a image genai prompt, parse the character description into structured data, don't change the format of the tags or the associated weights if they are specified",
                },
                {"role": "user", "content": prompt},
            ],
            response_model=Character,
            temperature=temperature,
            api_key=api_key,
        )

        fields: List[str, List[str]] = [
            getattr(character, field) for field in Character.model_fields
        ]
        return tuple(fields + [character])

        return tuple(
            json.dumps(getattr(character, field)) for field in self.RETURN_NAMES
        )

    # Add custom update method to handle dynamic model dropdown
    # FUNCTION = "update"

    def update(self, **kwargs):
        """
        Update method for handling UI updates.
        This method should only be called without arguments.
        """
        if not hasattr(self, "provider"):
            return []
        return ProviderToModels.get(self.provider, [])


class CharacterPromptMerger:
    """
    ComfyUI node for merging character tags with weights and field toggles.
    Allows selective field inclusion and custom weights per field.
    """

    CATEGORY = "mergers"
    FUNCTION = "merge_character"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("tags",)

    @classmethod
    def INPUT_TYPES(cls):
        # Get all fields from Character model
        fields = list(Character.model_fields.keys())

        required_inputs = {
            "character": ("CHARACTER", {"forceInput": True}),  # Input character object
            "delimiter": ("STRING", {"default": ","}),  # Delimiter for joining tags
        }

        # Add toggle and weight inputs for each field
        for field in fields:
            # Boolean toggle for the field
            required_inputs[f"enable_{field}"] = ("BOOLEAN", {"default": True})
            # Weight input (only visible when toggle is True)
            required_inputs[f"weight_{field}"] = (
                "FLOAT",
                {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.1,
                    "visible": False,  # Initially hidden
                },
            )

        return {"required": required_inputs}

    def merge_character(
        self, character: Character, delimiter: str = ",", **kwargs
    ) -> tuple:
        """
        Merge character fields based on toggles and weights.

        Args:
            character: Character object containing field data
            delimiter: String delimiter for joining tags
            **kwargs: Dynamic inputs for field toggles and weights

        Returns:
            Tuple containing the merged tags string
        """
        result = []
        fields = Character.model_fields.keys()

        for field in fields:
            # Check if field is enabled
            if kwargs.get(f"enable_{field}", True):
                weight = kwargs.get(f"weight_{field}", 1.0)
                field_tags = getattr(character, field, [])

                # Apply weights if not 1.0
                if weight != 1.0:
                    field_tags = [f"{tag}:{weight:.1f}" for tag in field_tags]

                result.extend(field_tags)

        # Join all tags with the specified delimiter and return as a single-element tuple
        return (delimiter.join(result),)


# Run async function
character = CharacterPromptParser()
if __name__ == "__main__":
    import asyncio

    # character = asyncio.run(
    #     CharacterPromptParser().parse_prompt(
    #         """score_9, score_8_up, score_7_up, source_anime,
    #     1girl, breast_curtains, very_long_hair, (blue_hair:1.2), long_hair, red_eyes, looking_at_viewer, smile, simple_background, white_background, solo, upper_body, fur-trimmed_capelet, fur_trim, white_capelet, capelet, white_dress, bowtie, cute_face, eyeliner, curly_hair, light_blue_hair, mini_witch_hat, neutral""",
    #         provider="deepseek",
    #         model="deepseek-chat",
    #         api_key="sk-fc122a11b4fc46778021c08c50727f1d",
    #     )
    # )
    # print(character)
