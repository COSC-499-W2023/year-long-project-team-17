import openai
from openai import OpenAI
import logging
from . import config
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def generate_summary(text: str):
    """
    A function to generate a summary of the provided text
    :param text: Text, summary of which has to be generated
    :return: The generated summary
    """
    generated_summary = ""
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
