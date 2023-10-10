import openai
import logging
from . import config
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

openai.api_key = os.getenv('OPENAI_API_KEY')


def generate_summary(text: str):
    generated_summary = ""
    try:
        generated_summary = openai.ChatCompletion.create(
            model=config.ENGINE,
            messages=[
                {'role': 'user',
                 'content': f'{config.SUMMARIZATION_GENERATION_PROMPT}\nUSER:{text}\nYour Response:'}
            ],

        )

        logging.info(generated_summary)
        return generated_summary

    except Exception as e:
        logging.info("something went wrong with generating presentation json based on the provided content")

    return generated_summary
