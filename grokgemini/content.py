from typing import Optional

import google.generativeai as genai
from google.generativeai.types.generation_types import GenerateContentResponse
from loguru import logger as __logger


def generate(
    instruction: str,
    model: str,
    api_key: str,
    stream: bool = False,
    system_instruction: Optional[str] = None,
) -> GenerateContentResponse:
    __logger.info("Generating content")
    __logger.debug(f"Instruction: {instruction}")
    __logger.debug(f"Model: {model}")
    __logger.debug(f"System Instruction: {system_instruction}")
    __logger.debug(f"Stream: {stream}")
    try:
        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(
            model_name=model, system_instruction=system_instruction
        )
        content: GenerateContentResponse = model_instance.generate_content(
            instruction, stream=stream
        )
        __logger.trace(f"Response: {content}")
        return content

    except genai.APIError as e:
        __logger.error(f"API error occurred: {e}")
        raise

    except Exception as e:
        __logger.error(f"An unexpected error occurred: {e}")
        raise


def describe() -> None:
    raise NotImplementedError("Image generation is not yet implemented")
