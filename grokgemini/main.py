import argparse
import pprint

import google.generativeai as genai
from google.generativeai.types.generation_types import GenerateContentResponse
from loguru import logger as __logger

from grokgemini.content import describe, generate
from grokgemini.util import configure_logger, get_key, make_believe, parse_arguments


def _generate(args, api_key):
    __logger.info("Generate text content")
    system_instruction: str | None = (
        args.system_instruction.read() if args.system_instruction else None
    )
    content: GenerateContentResponse = generate(
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


if __name__ == "__main__":
    args: argparse.Namespace = parse_arguments()
    configure_logger(args)
    make_believe(args)

    api_key = get_key()

    if args.generate_text:
        _generate(args, api_key)
    elif args.describe_image:
        describe()
    elif args.list_models:
        genai.configure(api_key=api_key)
        models = genai.list_models()
        for model in models:
            pprint.pprint(model.display_name)
