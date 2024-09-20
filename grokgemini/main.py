import os

import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai import GenerateContentResponse


def get_request() -> str:
    return input("Please enter your query: ")


def main():
    load_dotenv()
    genai.configure(api_key=os.getenv("AX_GOOGLE_GEMNINI_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    request: str = get_request()
    response: GenerateContentResponse = model.generate_content(request)
    print(response)


if __name__ == "__main__":
    main()
