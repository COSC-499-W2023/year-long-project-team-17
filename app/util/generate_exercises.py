import openai
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import logging
from . import config
import os

logging.basicConfig(level=logging.DEBUG)

load_dotenv(find_dotenv())
# openai.api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def generate_exercises_from_prompt(prompt:str):
    response = ""
    try:
        response = client.chat.completions.create(
            model=config.ENGINE,
            messages=[
                {'role': 'user',
                 'content': f'{config.EXERCISE_GENERATION_PROMPT}\nUSER:{prompt}\nYour Response:'}
            ],

        )
        # print("after A")
        response_json = response.choices[0].message.content

        logging.info(response_json)
        return response_json

    except Exception as e:
        logging.info(response.choices[0].message.content)
        logging.info("something went wrong with generating exercises based on the provided prompt.")
        logging.info(e)
        logging.error(e)


def generate_similar_exercises(text:str):
    response = ""
    try:
        response = client.chat.completions.create(
            model=config.ENGINE,
            messages=[
                {'role': 'user',
                 'content': f'{config.SIMILAR_EXERCISE_GENERATION_PROMPT}\nUSER:{text}\nYour Response:'}
            ],

        )
        # print("after A")
        response_json = response.choices[0].message.content

        logging.info(response_json)
        return response_json

    except Exception as e:
        logging.info(response["choices"][0]["message"]["content"])
        logging.info("something went wrong with generating exercises based on the provided prompt.")
        logging.info(e)
        logging.error(e)
