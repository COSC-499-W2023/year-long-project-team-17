from pptx import Presentation
from pptx.util import Pt, Inches
import tiktoken
import os
from typing import Dict
import openai
from openai import OpenAI
import json
import requests
from dotenv import load_dotenv, find_dotenv
import logging
from . import config
from util.generate_presentation import process_and_store_presentation_json
from io import BytesIO
from PIL import Image

logging.basicConfig(level=logging.DEBUG)

load_dotenv(find_dotenv())

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def generate_modified_presentation_json(original_presentation_json, user_comment):
    response = ""
    try:

        response = client.chat.completions.create(
            model=config.ENGINE,
            messages=[
                {'role': 'user',
                 'content': f'{config.PRESENTATION_MODIFICATION_PROMPT}\nORIGINAL PRESENTATION JSON: {original_presentation_json}\nUSER COMMENT:{user_comment}\nYour Response:'}
            ],
            response_format={"type": "json_object"},

        )
        response_json = json.loads(response.choices[0].message.content)

        logging.info(response_json)
        return response_json
    except Exception as e:
        logging.error(f"Something went wrong with modifying presentation json based on the provided comment and the original json: {e}")


def generate_modified_presentation(original_presentation_json: dict, user_comment: str):
    try:
        presentation_json = generate_modified_presentation_json(original_presentation_json, user_comment)
        # pres_info = get_presentation_info(presentation_json)
        presentation_object = process_and_store_presentation_json(presentation_json, True)
        # pres_info['presentation_json'] = presentation_json
        # values = {}
        # values['presentation'] = presentation_object
        # values['pres_info'] = pres_info
        return presentation_json, presentation_object
    except Exception as e:
        logging.error(f"Something went wrong with modifying the presentation: {e}")


def check_user_message(user_message):
    response = ""
    try:

        response = client.chat.completions.create(
            model=config.ENGINE,
            messages=[
                {'role': 'user',
                 'content': f'{config.MODIFICATION_CHECKER_PROMPT}\nUSER MESSAGE: {user_message}\nYour Response:'}
            ],
            # response_format={"type": "json_object"},

        )
        # response_json = json.loads(response.choices[0].message.content)
        logging.info(f"MODIFICATION CHECKER RESPONSE: {response}")

        modification_response = ""

        logging.info(str(response.choices[0].message.content).upper())
        logging.info(response.choices[0].message.content.upper())
        logging.info(response.choices[0].message.content.strip('"').upper())
        if '"' in response.choices[0].message.content:
            modification_response = response.choices[0].message.content.strip('"').upper()
        if modification_response == "TRUE":
            logging.info("IN THE TRUE")
            modification_needed = True
        else:
            logging.info("IN THE FALSE")
            modification_needed = False

        return modification_needed
    except Exception as e:
        logging.error(f"Something went wrong with checking modification user message: {e}")


def generate_modification_assistant_response(user_message):
    response = ""
    try:

        response = client.chat.completions.create(
            model=config.ENGINE,
            messages=[
                {'role': 'user',
                 'content': f'{config.MODIFICATION_ASSISTANT_PROMPT}\nUSER MESSAGE: {user_message}\nYour Response:'}
            ],
            # response_format={"type": "json_object"},

        )
        modification_assistant_response = response.choices[0].message.content
        logging.info(f"MODIFICATION ASSISTANT RESPONSE: {modification_assistant_response}")

        return modification_assistant_response
    except Exception as e:
        logging.error(f"Something went wrong with generating modification assistant response: {e}")
