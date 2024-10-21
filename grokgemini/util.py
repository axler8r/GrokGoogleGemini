import argparse
import os

from dotenv import load_dotenv
from loguru import logger as __logger

from grokgemini import __app_name__, __version__


# fmt: off
def parse_arguments() -> argparse.Namespace:
    __logger.debug("Parse arguments...")

    parser = argparse.ArgumentParser(prog=__app_name__, description="Generate content using Google Gemini API")

    # information arguments
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    # bahvriour arguments
    parser.add_argument("--system-instruction", type=argparse.FileType("r"), help="File containing the system instructions",)
    parser.add_argument("--model", type=str, help="Model to use for generation", default="gemini-1.5-flash",)
    parser.add_argument("--output", type=str, help="Output file name")
    parser.add_argument("--stream", action="store_true", help="Stream the output")
    # parser.add_argument("--configuration", type=argparse.FileType("r"), help="Configuration file")
    parser.add_argument("--file", dest="parts", type=str, action="append", help="Name(s) of binary file(s)")

    # task arguments
    group: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group()
    group.add_argument("--list-models", action="store_true", help="List available models")
    group.add_argument("--generate", action="store_true", help="Generate text content")
    group.add_argument("--describe", action="store_true", help="Describe one or more images")
    
    # positional arguments
    parser.add_argument("instruction", nargs="*", help="Input for the generation")

    try:
        namesapce: argparse.Namespace = parser.parse_args()
    except argparse.ArgumentError as e:
        raise e

    __logger.debug("Parsed arguments...")

    return namesapce
# fmt: on


def get_key():
    __logger.debug("Get API key...")

    load_dotenv()
    api_key: str | None = os.getenv("AX_GOOGLE_GEMNINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables")

    __logger.debug("Got API key...")

    return api_key
