ENGINE = "gpt-3.5-turbo-16k"
USER_INPUT_TOKEN_LIMIT = 2000
# PRESENTATION_GENERATION_PROMPT = """ You are given a content based on which you should create the template for powerpoint
# presentation. You should generate structure and content of each page using properties of slide pages from python pptx library.
# The output should be in json format. All strings must be in double quotes. Double check that the output is in json format, otherwise you will fail in your task.
# For example. ```USER: "I want you to generate a presentation on multivariable calculus.".
#  ```AI_ASSISTANT: {"slide1":{"slide_layout":0, "title":"Understanding Multivariable Calculus", "subtitle":"Exploring Functions of Multiple Variables", "space_after_paragraphs":-1, "paragraphs":{}}, "slide2":{"slide_layout":1, "title":"Introduction to Multivariable Calculus", "subtitle":"", "space_after_paragraphs":0.1, "paragraphs":{"paragraph1":"Multivariable calculus is important in physics, economics, and engineering.","paragraph2":"It deals with functions of more than one variable."}}, "slide3":{"slide_layout":1, "title":"Multivariable Functions", "subtitle":"", "space_after_paragraphs":0.1, "paragraphs":{"paragraph1":"Multivariable functions take multiple inputs and produce a single output.", "paragraph2":"Notation: f(x, y), g(x, y, z), etc."}}}
#    If a page doesn't need a paragraph, return an empty dict {} for its "paragraph" key and the space_after_paragraphs parameter equal to -1.
#    The number of paragraphs in a single page should not exceed 3 But the paragraphs must be thorough and profoundly written so the content is delivered in the best possible way. Use examples to explain the concepts. If you think that you need more than 3 paragraphs, increase the number of pages to fit your desired content, instead of increasing the number of paragraphs in a single page.
#    If a page should not include any subtitle, return an empty double quoted string for subtitle key ("").
#    the slide_layout parameter must be set based on the index of slide_layouts parameter in the python-pptx library.
#    Slide layout must be set to 0 only for the first slide of a presentation and includes a title and subtitle. The first page should not contain paragraphs. Do not forget to put a conclusion page. Do not include any punctuation marks at the end including ".". The slideshow must be comprehensive so try to use as many paragraphs and slides as needed. Again, DOUBLE CHECK THAT THE OUTPUT IS IN JSON FORMAT.
#    If the output is not in a valid json format you will fail in your task.
# """

PRESENTATION_GENERATION_PROMPT = """ You are given a content based on which you should create the template for powerpoint
presentation. You should generate structure and content of each page using properties of slide pages from python pptx library.
The output should be in json format. All strings must be in double quotes. Double check that the output is in json format, otherwise you will fail in your task.
For example. ```USER: "I want a presentation on the topic of NLP and Deep Learning. I want my presentation ot have 15 pages.".
 ```AI_ASSISTANT: {'slide1': {'slide_layout': 0, 'title': 'Introduction to NLP with Deep Learning', 'subtitle': 'Understanding the Intersection of Natural Language Processing and Deep Learning', 'space_after_paragraphs': -1, 'paragraphs': {}}, 'slide2': {'slide_layout': 1, 'title': 'What is NLP?', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'Natural Language Processing (NLP) is a subfield of artificial intelligence that focuses on the interaction between computers and human language.', 'paragraph2': 'Its goal is to enable computers to understand, interpret, and generate human language in a valuable and meaningful way.'}}, 'slide3': {'slide_layout': 1, 'title': 'Why Deep Learning in NLP?', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'Deep learning is a subfield of machine learning that leverages artificial neural networks to model and understand complex patterns and relationships in data.', 'paragraph2': 'In NLP, deep learning algorithms have achieved remarkable success in various tasks such as sentiment analysis, machine translation, and question answering.'}}, 'slide4': {'slide_layout': 1, 'title': 'Neural Networks in NLP', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'Neural networks are a fundamental component of deep learning.', 'paragraph2': 'In NLP, neural networks can be used for tasks such as text classification, named entity recognition, and language generation.', 'paragraph3': 'They are capable of automatically learning and extracting meaningful representations of textual data.'}}, 'slide5': {'slide_layout': 1, 'title': 'Recurrent Neural Networks (RNNs)', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'RNNs are a type of neural network that can capture sequential information in data.', 'paragraph2': 'In NLP, RNNs are commonly used for tasks such as text generation, language modeling, and sentiment analysis.', 'paragraph3': 'They can handle variable-length inputs and have a built-in memory to retain previous information.'}}, 'slide6': {'slide_layout': 1, 'title': 'Long Short-Term Memory (LSTM)', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'LSTM is a variant of RNNs that addresses the vanishing gradient problem.', 'paragraph2': 'In NLP, LSTMs are widely used for tasks such as machine translation, speech recognition, and text summarization.', 'paragraph3': 'They can effectively capture long-range dependencies in sequential data.'}}, 'slide7': {'slide_layout': 1, 'title': 'Convolutional Neural Networks (CNNs)', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'CNNs are primarily used for image recognition, but they can also be applied to NLP tasks.', 'paragraph2': 'In NLP, CNNs can be used for tasks such as text classification, sentiment analysis, and document classification.', 'paragraph3': 'They can learn local features from text and effectively capture patterns in different scales.'}}, 'slide8': {'slide_layout': 1, 'title': 'Transformers', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'Transformers are a type of deep learning model that has revolutionized NLP.', 'paragraph2': 'They utilize self-attention mechanisms to capture relationships between different words in a sentence.', 'paragraph3': 'Transformers have achieved state-of-the-art performance in various NLP tasks such as language translation, question answering, and text summarization.'}}, 'slide9': {'slide_layout': 1, 'title': 'Applications of NLP with Deep Learning', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'The combination of NLP and deep learning has enabled advancements in many real-world applications.', 'paragraph2': 'Some examples include chatbots, sentiment analysis in social media, machine translation, and voice assistants like Siri and Alexa.', 'paragraph3': 'These applications have greatly impacted industries such as healthcare, customer service, and e-commerce.'}}, 'slide10': {'slide_layout': 1, 'title': 'Challenges and Limitations', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'While NLP with deep learning has achieved remarkable progress, there are still challenges and limitations to overcome.', 'paragraph2': 'Some challenges include the lack of interpretability in deep learning models, the need for large amounts of labeled data, and biases in language representations.', 'paragraph3': 'Researchers are actively working on addressing these challenges to further advance the field.'}}, 'slide11': {'slide_layout': 1, 'title': 'Future Directions', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'The future of NLP with deep learning holds exciting possibilities.', 'paragraph2': 'Areas of future research include multimodal NLP, better language generation models, and addressing ethical concerns related to bias and misinformation.', 'paragraph3': 'Advancements in NLP will continue to shape how we interact with computers and enable new forms of human-computer communication.'}}, 'slide12': {'slide_layout': 1, 'title': 'Conclusion', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'In conclusion, NLP with deep learning is a powerful combination that enables computers to understand and process human language.', 'paragraph2': 'By leveraging neural networks and deep learning architectures, significant progress has been made in various NLP tasks.', 'paragraph3': 'As research and development in this field continue, we can expect even more exciting advancements and applications in the future.'}}, 'slide13': {'slide_layout': 1, 'title': 'References', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': '1. Goldberg, Y. (2017). Neural network methods for natural language processing. Synthesis Lectures on Human Language Technologies, 10(1), 1-309.', 'paragraph2': '2. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. Advances in Neural Information Processing Systems, 30, 5998-6008.', 'paragraph3': '3. Jurafsky, D., & Martin, J. H. (2019). Speech and Language Processing (3rd ed.). Pearson.'}}, 'slide14': {'slide_layout': 1, 'title': 'Thank You', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'Thank you for your attention!', 'paragraph2': 'Any questions?'}}}
   If a page doesn't need a paragraph, return an empty dict {} for its "paragraph" key and the space_after_paragraphs parameter equal to -1.
   The number of paragraphs in a single page should not exceed 3 But the paragraphs must be thorough and profoundly written so the content is delivered in the best possible way. Use examples to explain the concepts. If you think that you need more than 3 paragraphs, increase the number of pages to fit your desired content, instead of increasing the number of paragraphs in a single page.
   If a page should not include any subtitle, return an empty double quoted string for subtitle key ("").
   the slide_layout parameter must be set based on the index of slide_layouts parameter in the python-pptx library.
   Slide layout must be set to 0 only for the first slide of a presentation and includes a title and subtitle. The first page should not contain paragraphs. Do not forget to put a conclusion page. Do not include any punctuation marks at the end including ".". The slideshow must be comprehensive so try to use as many paragraphs and slides as needed. Again, DOUBLE CHECK THAT THE OUTPUT IS IN JSON FORMAT.
   If the output is not in a valid json format you will fail in your task.
"""

SUMMARIZATION_GENERATION_PROMPT = """You are given a text provided by the user. Generate a summary based on that. Do not mention anything about the user. Don't ask any questions. Don't introduce yourself. Just summarize the text."""