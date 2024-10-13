from typing import Optional

import google.generativeai as genai
from google.generativeai.types.generation_types import GenerateContentResponse


def generate(
    instruction: str,
    model: str,
    api_key: str,
    stream: bool = False,
    system_instruction: Optional[str] = None,
) -> GenerateContentResponse:
    try:
        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(
            model_name=model, system_instruction=system_instruction
        )
        content: GenerateContentResponse = model_instance.generate_content(
            instruction, stream=stream
        )
        return content

    except genai.APIError as e:
        raise

    except Exception as e:
        raise


def describe() -> None:
    raise NotImplementedError("Image generation is not yet implemented")
