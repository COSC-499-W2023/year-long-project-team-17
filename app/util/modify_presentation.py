import os
from openai import OpenAI
import json
from dotenv import load_dotenv, find_dotenv
import logging
from . import config
from util.generate_presentation import process_and_store_presentation_json


logging.basicConfig(level=logging.DEBUG)

load_dotenv(find_dotenv())

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def generate_modified_presentation_json(original_presentation_json, user_comment):
    """
    A function that generates the json of the modified presentation based on the previous presentation as well as the user comments
    :param original_presentation_json: Previously generated presentation json
    :param user_comment: User comment, based on which new presentation json has to be generated
    :return: The newly generated presentation json
    """
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
    """
    A wrapper function that generateds a modified presentation end-to-end using previous presentation json as well as the user comment
    :param original_presentation_json: Previous presentation json
    :param user_comment: User comment based on which the presentation has to be modified
    :return: The modified presentation
    """

    try:
        presentation_json = generate_modified_presentation_json(original_presentation_json, user_comment)
        presentation_object = process_and_store_presentation_json(presentation_json, True)
        return presentation_json, presentation_object
    except Exception as e:
        logging.error(f"Something went wrong with modifying the presentation: {e}")


def check_user_message(user_message):
    """
    A function to check whether the user message requires to modify the previously generated presentation or not
    :param user_message: The user message
    :return: A boolean indicating if the presentation needs to be modified or not
    """

    response = ""
    try:

        response = client.chat.completions.create(
            model=config.ENGINE,
            messages=[
                {'role': 'user',
                 'content': f'{config.MODIFICATION_CHECKER_PROMPT}\nUSER MESSAGE: {user_message}\nYour Response:'}
            ],

        )
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
    """
    A function that responds to the user given question, indicating that either presentation is being modified or that the question is not in its scopes of expertice
    :param user_message: The user message
    :return: Response to the user message
    """

    response = ""
    try:

        response = client.chat.completions.create(
            model=config.ENGINE,
            messages=[
                {'role': 'user',
                 'content': f'{config.MODIFICATION_ASSISTANT_PROMPT}\nUSER MESSAGE: {user_message}\nYour Response:'}
            ],

        )
        modification_assistant_response = response.choices[0].message.content
        logging.info(f"MODIFICATION ASSISTANT RESPONSE: {modification_assistant_response}")

        return modification_assistant_response
    except Exception as e:
        logging.error(f"Something went wrong with generating modification assistant response: {e}")
