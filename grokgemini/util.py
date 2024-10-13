import argparse
import os
import sys

from dotenv import load_dotenv

__version__ = "0.7.0"


# fmt: off
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate content using Google Gemini API")

    # information arguments
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    # bahvriour arguments
    parser.add_argument("--system-instruction", type=argparse.FileType("r"), help="File containing the system instructions",)
    parser.add_argument("--model", type=str, help="Model to use for generation", default="gemini-1.5-flash",)
    parser.add_argument("--output", type=str, help="Output file name")
    parser.add_argument("--stream", action="store_true", help="Stream the output")
    # parser.add_argument("--multi-modal", action="store_true", help="Enable multi-modal generation")
    # parser.add_argument("--configuration", type=argparse.FileType("r"), help="Configuration file")

    # task arguments
    group: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group()
    group.add_argument("--list-models", action="store_true", help="List available models")
    group.add_argument("-t", "--generate-text", action="store_true", help="Generate text content")
    group.add_argument("-d", "--describe-image", type=argparse.FileType("rb"), help="Describe image (valid formats: jpeg, png)",)

    # positional arguments
    parser.add_argument("instruction", nargs="*", help="Input for the generation")

    return parser.parse_args()
# fmt: on





def get_key():
    load_dotenv()
    api_key: str | None = os.getenv("AX_GOOGLE_GEMNINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables")
    return api_key
