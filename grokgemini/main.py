import argparse
import os
from typing import Optional

import google.generativeai as genai
from dotenv import load_dotenv

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
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model, system_instruction=system_instruction)
    request: str = " ".join(instruction)
    response = model.generate_content(request)
    return response.text


def _generate_image() -> None:
    raise NotImplementedError("Image generation is not yet implemented")


def _describe_image() -> None:
    raise NotImplementedError("Image generation is not yet implemented")


if __name__ == "__main__":
    load_dotenv()
    api_key: str | None = os.getenv("AX_GOOGLE_GEMNINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables")

    args: argparse.Namespace = _parse_arguments()
    if args.generate_text:
        system_instruction: str | None = (
            args.system_instruction.read() if args.system_instruction else None
        )
        result: str = _generate_text(
            instruction=args.instruction,
            model=args.model,
            api_key=api_key,
            system_instruction=system_instruction,
        )
        if args.output:
            with open(args.output, "w") as file:
                file.write(result)
        else:
            print(result)
    elif args.generate_image:
        _generate_image()
    elif args.describe_image:
        _describe_image()
    elif args.list_models:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        print(models)
