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
from io import BytesIO
from PIL import Image

logging.basicConfig(level=logging.DEBUG)

load_dotenv(find_dotenv())

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def get_presentation_json(description: str) -> Dict[str, str]:
    """
        Generates Presentation json based on content.
        Args:
            description (str): A description of the user's presentation.
        Returns:
             presentation in json format
        """
    response = ""
    try:

        response = client.chat.completions.create(
            model=config.ENGINE,
            messages=[
                {'role': 'user',
                 'content': f'{config.PRESENTATION_GENERATION_PROMPT}\nUSER:{description}\nYour Response:'}
            ],
        )
        response_json = json.loads(response.choices[0].message.content)

        logging.info(response_json)
        return response_json
    except Exception as e:
        logging.info(response.choices[0].message.content)

        logging.info("something went wrong with generating presentation json based on the provided content.")
        logging.info(e)
        logging.error(e)


def download_image(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        original_image = Image.open(BytesIO(response.content))

        original_image.save(destination)

        logging.info(f"Image downloaded successfully and saved to {destination}")
    else:
        logging.info(f"Failed to download image. Status code: {response.status_code}")


def process_and_store_presentation_json(result: dict):
    """
           Process presentation json and create a Presentation object
           Args:
               result (dict): The json of presentation
           Returns:
                The presentation as a Presentation object
           """

    try:
        presentation = Presentation()
        i = 0
        all_image_paths = []
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
                    current_content = None
                    if value["slide_layout"] == 3:
                        print("true")
                        current_content = current_slide.shapes.placeholders[1]
                    else:
                        current_content = current_slide.shapes.placeholders[1]
                    current_paragraph = current_content.text_frame.add_paragraph()
                    current_paragraph.text = paragraph_text

                    for run in current_paragraph.runs:
                        run.font.size = Pt(18)

                    if value["space_after_paragraphs"] > 0:
                        current_paragraph.space_after = Inches(value["space_after_paragraphs"])
            if value.get("image_title") and value.get("slide_layout") == 3:
                content = current_slide.shapes.placeholders[2]
                image_title = content.text_frame.add_paragraph()
                image_title.text = value.get("image_title")
                for run in image_title.runs:
                    run.font.size = Pt(18)
                image_path = generate_presentation_images(value.get("image_keywords"), i)
                all_image_paths.append(image_path)
                left_inch = Inches(5.5)
                top_inch = Inches(3)
                width_inch = height_inch = Inches(4)
                current_slide.shapes.add_picture(image_path, left_inch, top_inch, width_inch, height_inch)
                i += 1

        presentation.save("my_presentation.pptx")
        for image_path in all_image_paths:
            if os.path.exists(image_path):
                os.remove(image_path)
        return presentation
    except Exception as e:

        logging.info("something went wrong with generating Presentation object based on the presentation json.")
        logging.info(e)
        logging.error(e)


def generate_presentation(description: str):
    try:
        presentation_json = get_presentation_json(description)
        presentation_object = process_and_store_presentation_json(presentation_json)
        return presentation_object
    except Exception as e:
        logging.info("Something went wrong with generating presentation.")
        logging.info(e)
        logging.error(e)


def generate_presentation_images(image_keywords, image_number):
    result = client.images.generate(
        model="dall-e-3",
        prompt=image_keywords,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = result.data[0].url
    image_path = f"downloaded_image_{image_number}.png"
    download_image(image_url, image_path)
    return image_path
