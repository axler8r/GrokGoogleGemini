import argparse
import pprint

import google.generativeai as genai
from google.generativeai.types.generation_types import GenerateContentResponse
from loguru import logger as __logger



def _generate_content(
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


def _describe_image() -> None:
    raise NotImplementedError("Image generation is not yet implemented")

    else:




    if args.generate_text:
        __logger.info("Generate text content")
        system_instruction: str | None = (
            args.system_instruction.read() if args.system_instruction else None
        )
        content: GenerateContentResponse = _generate_content(
            instruction=args.instruction,
            model=args.model,
            api_key=api_key,
            stream=args.stream,
            system_instruction=system_instruction,
        )
        __logger.trace(f"Model: {args.model}")
        __logger.trace(f"System Instruction: {system_instruction}")
        __logger.trace(f"Content: {content}")
        if args.stream:
            for chunk in content:
                __logger.trace(f"Chunk: {chunk.text}")
                print(chunk.text)
        else:
            print(content.text)
        if args.output:
            with open(args.output, "w") as file:
                file.write(content.text)
        __logger.info("Generated text content")

    elif args.describe_image:
        _describe_image()
    elif args.list_models:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        for model in models:
            pprint.pprint(model.display_name)
