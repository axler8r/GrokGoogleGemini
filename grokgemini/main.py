import argparse
import os
import sys
from typing import Any, Optional

import google.generativeai as genai
from dotenv import load_dotenv
from loguru import logger

__version__ = "0.1.0"


def _read_image_file(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        return file.read()


# fmt: off
def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate content using Google Gemini API")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-s", "--system-instruction", type=argparse.FileType("r"), help="File containing the system instructions")
    parser.add_argument("-m", "--model", type=str, help="Model to use for generation", default="gemini-1.5-flash")
    parser.add_argument("-o", "--output", type=str, help="Output file name")
    parser.add_argument("-v", "--verbose", action="count", help="Enable verbose logging", default=0)

    group: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--list-models", action="store_true", help="List available models")
    group.add_argument("-t", "--generate-text", action="store_true", help="Generate text content")
    group.add_argument("-i", "--generate-image", action="store_true", help="Generate image")
    group.add_argument("-d", "--describe-image", type=argparse.FileType("rb"), help="Describe image (valid formats: jpeg, png)")

    parser.add_argument("instruction", nargs="*", help="Input for the generation")

    return parser.parse_args()
# fmt: on


def _generate_text(
    instruction: str, model: str, api_key: str, system_instruction: Optional[str] = None
) -> str:
    logger.info("Generating text content")
    logger.debug(f"Instruction: {instruction}")
    logger.debug(f"Model: {model}")
    logger.debug(f"System Instruction: {system_instruction}")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model, system_instruction=system_instruction)
        content: Any = model.generate_content(instruction)

        logger.trace(f"Response: {content}")
        return content.text

    except genai.APIError as e:
        logger.error(f"API error occurred: {e}")
        raise

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise


def _generate_image() -> None:
    raise NotImplementedError("Image generation is not yet implemented")


def _describe_image() -> None:
    raise NotImplementedError("Image generation is not yet implemented")


if __name__ == "__main__":
    # logger.info("Parsing command line arguments")
    args: argparse.Namespace = _parse_arguments()
    # logger.info("Parsed command line arguments")

    # logger.info("Configuring logging")
    if args.verbose == 0:
        logger.remove()
        logger.add(sink=sys.stderr, level="WARNING")
    elif args.verbose == 1:
        logger.remove()
        logger.add(sink=sys.stderr, level="INFO")
    elif args.verbose == 2:
        logger.remove()
        logger.add(sink=sys.stderr, level="DEBUG")
    else:
        logger.remove()
        logger.add(sink=sys.stderr, level="TRACE")

    logger.info("Parse command line arguments")
    logger.trace(args)
    logger.info("Parsed command line arguments")

    logger.info("Configure logging")
    logger.trace(f"Logger: {logger}")
    logger.info("Configured logging")

    logger.info("Fetch environment variables")

    load_dotenv()
    api_key: str | None = os.getenv("AX_GOOGLE_GEMNINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables")

    logger.info("Fetched environment variables")

    if args.generate_text:
        logger.info("Generate text content")

        system_instruction: str | None = (
            args.system_instruction.read() if args.system_instruction else None
        )
        content: str = _generate_text(
            instruction=args.instruction,
            model=args.model,
            api_key=api_key,
            system_instruction=system_instruction,
        )
        if args.output:
            with open(args.output, "w") as file:
                file.write(content)
        else:
            print(content)

        logger.trace(f"System Instruction: {system_instruction}")
        logger.trace(f"Content: {content}")
        logger.info("Generated text content")
    elif args.generate_image:
        _generate_image()
    elif args.describe_image:
        _describe_image()
    elif args.list_models:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        print(models)
