ENGINE = "gpt-3.5-turbo"
USER_INPUT_TOKEN_LIMIT = 2000
PRESENTATION_GENERATION_PROMPT = """ You are given a content based on which you should create the template for powerpoint
presentation. You should generate structure and content of each page using properties of slide pages from python pptx library.
The output should be in json format. All strings must be in double quotes. Double check that the output is in json format, otherwise you will fail in your task.
For example. ```USER: "I want you to generate a presentation on multivariable calculus.".
 ```AI_ASSISTANT: {"slide1":{"slide_layout":0, "title":"Understanding Multivariable Calculus", "subtitle":"Exploring Functions of Multiple Variables", "space_after_paragraphs":-1, "paragraphs":{}}, "slide2":{"slide_layout":1, "title":"Introduction to Multivariable Calculus", "subtitle":"", "space_after_paragraphs":0.1, "paragraphs":{"paragraph1":"Multivariable calculus is important in physics, economics, and engineering.","paragraph2":"It deals with functions of more than one variable."}}, "slide3":{"slide_layout":1, "title":"Multivariable Functions", "subtitle":"", "space_after_paragraphs":0.1, "paragraphs":{"paragraph1":"Multivariable functions take multiple inputs and produce a single output.", "paragraph2":"Notation: f(x, y), g(x, y, z), etc."}}}
   If a page doesn't need a paragraph, return an empty dict {} for its "paragraph" key and the space_after_paragraphs parameter equal to -1.
   The number of paragraphs in a single page should not exceed 3 But the paragraphs must be thorough and profoundly written so the content is delivered in the best possible way. Use examples to explain the concepts. If you think that you need more than 3 paragraphs, increase the number of pages to fit your desired content, instead of increasing the number of paragraphs in a single page.
   If a page should not include any subtitle, return an empty double quoted string for subtitle key ("").
   the slide_layout parameter must be set based on the index of slide_layouts parameter in the python-pptx library.
   Slide layout must be set to 0 only for the first slide of a presentation and includes a title and subtitle. The first page should not contain paragraphs. Do not forget to put a conclusion page. Do not include any punctuation marks at the end including ".". The slideshow must be comprehensive so try to use as many paragraphs and slides as needed. Again, DOUBLE CHECK THAT THE OUTPUT IS IN JSON FORMAT.
   If the output is not in a valid json format you will fail in your task. 
"""

SUMMARIZATION_GENERATION_PROMPT = """You are given a text provided by the user. Generate a summary based on that. Do not mention anything about the user. Don't ask any questions. Don't introduce yourself. Just summarize the text."""
