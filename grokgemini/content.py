"""
This module provides functionality to generate content using Google's generative
AI models.

Functions:
    generate(
        instruction: str,
        model: str,
        api_key: str, stream: bool = False,
        system_instruction: Optional[str] = None
    ) -> GenerateContentResponse:

    describe() -> None:
        Raises a NotImplementedError indicating that image generation is not yet implemented.
"""

from typing import Any, List, Optional

import google.generativeai as genai
import PIL.Image as Image
from google.generativeai.types.generation_types import GenerateContentResponse
from loguru import logger as __logger


def generate(
    instruction: str,
    model: str,
    api_key: str,
    stream: bool = False,
    system_instruction: Optional[str] = None,
) -> GenerateContentResponse:
    """
    Generates content based on the provided instruction using a specified generative model.

    Args:
        instruction (str): The instruction or prompt to generate content from.
        model (str): The name of the generative model to use.
        api_key (str): The API key for authentication with the generative model service.
        stream (bool, optional): Whether to stream the response. Defaults to False.
        system_instruction (Optional[str], optional): Additional system instructions for the model. Defaults to None.

    Returns:
        GenerateContentResponse: The generated content response from the model.

    Raises:
        genai.APIError: If an API error occurs during content generation.
        Exception: If an unexpected error occurs.
    """
    try:
        __logger.debug("Generate content...")

        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(
            model_name=model, system_instruction=system_instruction
        )
        content: GenerateContentResponse = model_instance.generate_content(
            ''.join(instruction), stream=stream
        )

        __logger.debug("Generated content...")

        return content

    except Exception:
        raise


def _load_image(image_path: str) -> Image.Image:
    """
    Loads an image from the specified path.

    Args:
        image_path (str): The path to the image file.

    Returns:
        Image.Image: The loaded image.
    """
    return Image.open(image_path)


def describe(
    instruction: str,
    parts: List[str],
    model: str,
    api_key: str,
    stream: bool = False,
    system_instruction: Optional[str] = None,
) -> None:
    """
    Generates content based on the provided instructions and parts using a specified generative model.

    Args:
        instruction (str): The main instruction to guide content generation.
        parts (List[str]): A list of parts (e.g., image paths) to be included in the content generation process.
        model (str): The name of the generative model to be used.
        api_key (str): The API key for authenticating with the generative model service.
        stream (bool, optional): Whether to stream the content generation process. Defaults to False.
        system_instruction (Optional[str], optional): An optional system instruction to configure the model. Defaults to None.

    Returns:
        GenerateContentResponse: The generated content response from the model.

    Raises:
        Exception: If any error occurs during the content generation process.
    """
    try:
        __logger.debug("Describe content...")

        genai.configure(api_key=api_key)
        model_instance = genai.GenerativeModel(
            model_name=model, system_instruction=system_instruction
        )
        instructions: List[Any] = [_load_image(part) for part in parts]
        instructions.append(''.join(instruction))
        content: GenerateContentResponse = model_instance.generate_content(
            instructions, stream=stream
        )

        __logger.debug("Described content...")

        return content

    except Exception:
        raise
