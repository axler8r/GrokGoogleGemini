import argparse
import pprint

import google.generativeai as genai
from google.generativeai.types.generation_types import GenerateContentResponse
from loguru import logger as __logger

from grokgemini.content import describe, generate
from grokgemini.util import get_key, parse_arguments


def _generate(args, api_key):
    system_instruction: str | None = (
        args.system_instruction.read() if args.system_instruction else None
    )
    __logger.debug("Generate content...")

    content: GenerateContentResponse = generate(
        instruction=args.instruction,
        model=args.model,
        api_key=api_key,
        stream=args.stream,
        system_instruction=system_instruction,
    )
    if args.stream:
        for chunk in content:
            print(chunk.text)
    else:
        print(content.text)
    if args.output:
        with open(args.output, "w") as file:
            file.write(content.text)

    __logger.debug("Generated content...")


def _describe(args, api_key):
    system_instruction: str | None = (
        args.system_instruction.read() if args.system_instruction else None
    )
    __logger.debug("Describe content...")

    content: GenerateContentResponse = describe(
        instruction=args.instruction,
        parts=args.parts,
        model=args.model,
        api_key=api_key,
        stream=args.stream,
        system_instruction=system_instruction,
    )
    if args.stream:
        for chunk in content:
            print(chunk.text)
    else:
        print(content.text)
    if args.output:
        with open(args.output, "w") as file:
            file.write(content.text)

    __logger.debug("Described content...")


if __name__ == "__main__":
    __logger.info("Start grokgemini...")

    args: argparse.Namespace = parse_arguments()
    __logger.debug(f"Arguments: {args}")
    api_key = get_key()

    if args.generate:
        __logger.info("Generate content...")
        _generate(args, api_key)

    if args.describe and not args.parts:
        args.error("The --describe argument requires at least one --file argument")
        __logger.error("The --describe argument requires at least one --file argument")
    else:
        __logger.info("Describe content...")
        _describe(args, api_key)

    if args.list_models:
        __logger.info("List models...")
        genai.configure(api_key=api_key)
        models = genai.list_models()
        for model in models:
            pprint.pprint(model.display_name)
