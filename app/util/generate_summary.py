import openai
from openai import OpenAI
import logging
from . import config
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

# openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def generate_summary(text: str):
    generated_summary = ""
   # print(openai.api_key)
    try:
        generated_summary = client.chat.completions.create(
            model=config.ENGINE,
            messages=[
                {'role': 'user',
                 'content': f'{config.SUMMARIZATION_GENERATION_PROMPT}\nUSER:{text}\nYour Response:'}
            ],

        )

        logging.info(generated_summary.choices[0].message.content)
        return generated_summary.choices[0].message.content

    except Exception as e:
        logging.info("something went wrong with generating presentation json based on the provided content")

    return generated_summary
