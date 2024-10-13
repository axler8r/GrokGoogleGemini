import argparse
import os

from dotenv import load_dotenv

__version__ = "0.7.0"


# fmt: off
def parse_arguments() -> argparse.Namespace:
    class DependOnFileArgument(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if not getattr(namespace, "file"):
                parser.error("Missing one or more --file arguments")

    parser = argparse.ArgumentParser(description="Generate content using Google Gemini API")

    # information arguments
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    # bahvriour arguments
    parser.add_argument("--system-instruction", type=argparse.FileType("r"), help="File containing the system instructions",)
    parser.add_argument("--model", type=str, help="Model to use for generation", default="gemini-1.5-flash",)
    parser.add_argument("--output", type=str, help="Output file name")
    parser.add_argument("--stream", action="store_true", help="Stream the output")
    # parser.add_argument("--configuration", type=argparse.FileType("r"), help="Configuration file")
    parser.add_argument("--file", type=argparse.FileType("rb"), action="append", help="Binary file(s) to process")

    # task arguments
    group: argparse._MutuallyExclusiveGroup = parser.add_mutually_exclusive_group()
    group.add_argument("--list-models", action="store_true", help="List available models")
    group.add_argument("--generate", action="store_true", help="Generate text content")
    group.add_argument("--describe", action=DependOnFileArgument, help="Describe one or more images")
    
    # positional arguments
    parser.add_argument("instruction", nargs="*", help="Input for the generation")

    try:
        namesapce: argparse.Namespace = parser.parse_args()
    except argparse.ArgumentError as e:
        raise e

    return namesapce
# fmt: on


def get_key():
    load_dotenv()
    api_key: str | None = os.getenv("AX_GOOGLE_GEMNINI_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment variables")
    return api_key
