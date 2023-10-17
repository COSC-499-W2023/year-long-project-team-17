from pptx import Presentation
from pptx.util import Pt, Inches
import tiktoken
import os
from typing import Dict
import openai
import json

from dotenv import load_dotenv, find_dotenv
import logging
from . import config

logging.basicConfig(level=logging.DEBUG)

load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_presentation_json(description: str) -> Dict[str, str]:
    """
        Generates Presentation json based on content.
        Args:
            description (str): A description of the user's presentation.
        Returns:
             presentation in json format
        """
    response=""
    try:
        # print("Inside of the function")
        response = openai.ChatCompletion.create(
                model=config.ENGINE,
                messages=[
                    {'role': 'user', 'content': f'{config.PRESENTATION_GENERATION_PROMPT}\nUSER:{description}\nYour Response:'}
                ],

            )
        # print("after A")
        response_json = json.loads(response["choices"][0]["message"]["content"])

        logging.info(response_json)
        return response_json
    except Exception as e:
        logging.info(response["choices"][0]["message"]["content"])

        logging.info("something went wrong with generating presentation json based on the provided content.")
        logging.info(e)
        logging.error(e)
def process_and_store_presentation_json(result: dict):
    """
           Process presentation json and create a Presentation object
           Args:
               result (dict): The json of presentation
           Returns:
                The presentation as a Presentation object
           """
    # print("*"*70)
    # print(type(result))
    #result = json.loads(result)
    try:
        presentation = Presentation()

        for key, value in result.items():
            # print(key, ":", value)
            current_slide = presentation.slides.add_slide(presentation.slide_layouts[value["slide_layout"]])
            current_slide_title = current_slide.shapes.title
            current_slide_title.text = value["title"]
            if value["subtitle"]:
                current_slide_subtitle = current_slide.shapes.placeholders[1]
                current_slide_subtitle.text = value["subtitle"]
            if value["paragraphs"]:
                for paragraph, paragraph_text in value["paragraphs"].items():
                    current_content = current_slide.shapes.placeholders[1]
                    current_paragraph = current_content.text_frame.add_paragraph()
                    current_paragraph.text = paragraph_text

                    for run in current_paragraph.runs:
                        run.font.size = Pt(18)

                    if value["space_after_paragraphs"] > 0:
                        current_paragraph.space_after = Inches(value["space_after_paragraphs"])
        return presentation
    except Exception as e:

        logging.info("something went wrong with generating Presentation object based on the presentation json.")
        logging.info(e)
        logging.error(e)
    #presentation.save(path)

def generate_presentation(description: str):
    try:
        presentation_json = get_presentation_json(description)
        presentation_object = process_and_store_presentation_json(presentation_json)
        return presentation_object
    except Exception as e:
        logging.info("Something went wrong with generating presentation.")
        logging.info(e)
        logging.error(e)


#tiktoken
