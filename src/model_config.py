# model_config.py
import json
import os
from typing import Dict, List

PROVIDER_MODELS: Dict[str, List[str]] = {
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


# Write config to JS file
def write_js_config():
    js_content = (
        f"export const ProviderToModels = {json.dumps(PROVIDER_MODELS, indent=2)};"
    )
    js_path = os.path.join(os.path.dirname(__file__), "..", "js", "modelConfig.js")
    os.makedirs(os.path.dirname(js_path), exist_ok=True)
    with open(js_path, "w") as f:
        f.write(js_content)


write_js_config()
