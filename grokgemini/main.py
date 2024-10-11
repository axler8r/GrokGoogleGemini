import argparse
import os

import google.generativeai as genai
from dotenv import load_dotenv

__version__ = "0.1.0"


def _read_image_file(file_path: str) -> bytes:
    with open(file_path, "rb") as file:
        return file.read()


# fmt: off
def _parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate contect using Google Gemini API")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-s", "--system-prompt", type=argparse.FileType("r"), help="File containing the system prompt",)
    parser.add_argument("-m", "--model", type=str, help="Model to use for generation", default="gemini-1.5-flash")

    group: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--list-models", action="store_true", help="List available models")
    group.add_argument("-t", "--generate-text", action="store_true", help="Generate text content")
    group.add_argument("-i", "--generate-image", action="store_true", help="Generate image")
    group.add_argument("-d", "--describe-image", type=argparse.FileType("rb"), help="Describe image (valid formats: jpeg, png)",)

    parser.add_argument("input", nargs="*", help="Input for the generation")

    return parser.parse_args()
# fmt: on


def _generate_text(model: str, input: str) -> None:
    genai.configure(api_key=os.getenv("AX_GOOGLE_GEMNINI_API_KEY"))
    model = genai.GenerativeModel(model)
    request: str = " ".join(input)
    response: genai.GenerateContentResponse = model.generate_content(request)
    print(response)


def _generate_image() -> None:
    raise NotImplementedError("Image generation is not yet implemented")
    load_dotenv()
    genai.configure(api_key=os.getenv("AX_GOOGLE_GEMNINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    request: str = _read_input()
    response = model.generate_image(request)
    print(response)


def _describe_image() -> None:
    raise NotImplementedError("Image generation is not yet implemented")
    load_dotenv()
    genai.configure(api_key=os.getenv("AX_GOOGLE_GEMNINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    request: str = _read_image_file(_ARGS.describe_image.name)
    response = model.describe_image(request)
    print(response)


if __name__ == "__main__":
    _ARGS: argparse.Namespace = _parse_arguments()

    load_dotenv()
    if _ARGS.generate_text:
        _generate_text(_ARGS.model, _ARGS.input)
    if _ARGS.generate_image:
        _generate_image()
    if _ARGS.describe_image:
        _describe_image()
