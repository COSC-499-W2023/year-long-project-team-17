ENGINE = "gpt-3.5-turbo-16k"
CONTENT_ADAPTATION_ENGINE = "gpt-4"
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

# PRESENTATION_GENERATION_PROMPT = """ You are given a content based on which you should create the template for powerpoint
# presentation. You should generate structure and content of each page using properties of slide pages from python pptx library.
# The output should be in json format. All strings must be in double quotes. Double check that the output is in json format, otherwise you will fail in your task.
# For example. ```USER: "I want a presentation on the topic of NLP and Deep Learning. I want my presentation ot have 15 pages.".
#  ```AI_ASSISTANT: {'slide1': {'slide_layout': 0, 'title': 'Introduction to NLP with Deep Learning', 'subtitle': 'Understanding the Intersection of Natural Language Processing and Deep Learning', 'space_after_paragraphs': -1, 'paragraphs': {}}, 'slide2': {'slide_layout': 1, 'title': 'What is NLP?', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'Natural Language Processing (NLP) is a subfield of artificial intelligence that focuses on the interaction between computers and human language.', 'paragraph2': 'Its goal is to enable computers to understand, interpret, and generate human language in a valuable and meaningful way.'}}, 'slide3': {'slide_layout': 1, 'title': 'Why Deep Learning in NLP?', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'Deep learning is a subfield of machine learning that leverages artificial neural networks to model and understand complex patterns and relationships in data.', 'paragraph2': 'In NLP, deep learning algorithms have achieved remarkable success in various tasks such as sentiment analysis, machine translation, and question answering.'}}, 'slide4': {'slide_layout': 1, 'title': 'Neural Networks in NLP', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'Neural networks are a fundamental component of deep learning.', 'paragraph2': 'In NLP, neural networks can be used for tasks such as text classification, named entity recognition, and language generation.', 'paragraph3': 'They are capable of automatically learning and extracting meaningful representations of textual data.'}}, 'slide5': {'slide_layout': 1, 'title': 'Recurrent Neural Networks (RNNs)', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'RNNs are a type of neural network that can capture sequential information in data.', 'paragraph2': 'In NLP, RNNs are commonly used for tasks such as text generation, language modeling, and sentiment analysis.', 'paragraph3': 'They can handle variable-length inputs and have a built-in memory to retain previous information.'}}, 'slide6': {'slide_layout': 1, 'title': 'Long Short-Term Memory (LSTM)', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'LSTM is a variant of RNNs that addresses the vanishing gradient problem.', 'paragraph2': 'In NLP, LSTMs are widely used for tasks such as machine translation, speech recognition, and text summarization.', 'paragraph3': 'They can effectively capture long-range dependencies in sequential data.'}}, 'slide7': {'slide_layout': 1, 'title': 'Convolutional Neural Networks (CNNs)', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'CNNs are primarily used for image recognition, but they can also be applied to NLP tasks.', 'paragraph2': 'In NLP, CNNs can be used for tasks such as text classification, sentiment analysis, and document classification.', 'paragraph3': 'They can learn local features from text and effectively capture patterns in different scales.'}}, 'slide8': {'slide_layout': 1, 'title': 'Transformers', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'Transformers are a type of deep learning model that has revolutionized NLP.', 'paragraph2': 'They utilize self-attention mechanisms to capture relationships between different words in a sentence.', 'paragraph3': 'Transformers have achieved state-of-the-art performance in various NLP tasks such as language translation, question answering, and text summarization.'}}, 'slide9': {'slide_layout': 1, 'title': 'Applications of NLP with Deep Learning', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'The combination of NLP and deep learning has enabled advancements in many real-world applications.', 'paragraph2': 'Some examples include chatbots, sentiment analysis in social media, machine translation, and voice assistants like Siri and Alexa.', 'paragraph3': 'These applications have greatly impacted industries such as healthcare, customer service, and e-commerce.'}}, 'slide10': {'slide_layout': 1, 'title': 'Challenges and Limitations', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'While NLP with deep learning has achieved remarkable progress, there are still challenges and limitations to overcome.', 'paragraph2': 'Some challenges include the lack of interpretability in deep learning models, the need for large amounts of labeled data, and biases in language representations.', 'paragraph3': 'Researchers are actively working on addressing these challenges to further advance the field.'}}, 'slide11': {'slide_layout': 1, 'title': 'Future Directions', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'The future of NLP with deep learning holds exciting possibilities.', 'paragraph2': 'Areas of future research include multimodal NLP, better language generation models, and addressing ethical concerns related to bias and misinformation.', 'paragraph3': 'Advancements in NLP will continue to shape how we interact with computers and enable new forms of human-computer communication.'}}, 'slide12': {'slide_layout': 1, 'title': 'Conclusion', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'In conclusion, NLP with deep learning is a powerful combination that enables computers to understand and process human language.', 'paragraph2': 'By leveraging neural networks and deep learning architectures, significant progress has been made in various NLP tasks.', 'paragraph3': 'As research and development in this field continue, we can expect even more exciting advancements and applications in the future.'}}, 'slide13': {'slide_layout': 1, 'title': 'References', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': '1. Goldberg, Y. (2017). Neural network methods for natural language processing. Synthesis Lectures on Human Language Technologies, 10(1), 1-309.', 'paragraph2': '2. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. Advances in Neural Information Processing Systems, 30, 5998-6008.', 'paragraph3': '3. Jurafsky, D., & Martin, J. H. (2019). Speech and Language Processing (3rd ed.). Pearson.'}}, 'slide14': {'slide_layout': 1, 'title': 'Thank You', 'subtitle': '', 'space_after_paragraphs': 0.1, 'paragraphs': {'paragraph1': 'Thank you for your attention!', 'paragraph2': 'Any questions?'}}}
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
 ```AI_ASSISTANT: {"slide1": { "slide_layout": 0, "title": "Introduction to NLP with Deep Learning", "image_keywords": "", "image_title": "", "subtitle": "Understanding the Intersection of Natural Language Processing and Deep Learning", "space_after_paragraphs": -1, "paragraphs": {} }, "slide2": { "slide_layout": 1, "title": "What is NLP?", "subtitle": "", "space_after_paragraphs": 0.1, "image_keywords": "", "image_title": "", "paragraphs": { "paragraph1": "Natural Language Processing (NLP) is a subfield of artificial intelligence that focuses on the interaction between computers and human language.", "paragraph2": "Its goal is to enable computers to understand, interpret, and generate human language in a valuable and meaningful way." } }, "slide3": { "slide_layout": 1, "title": "Why Deep Learning in NLP?", "subtitle": "", "space_after_paragraphs": 0.1, "image_keywords": "", "image_title": "", "paragraphs": { "paragraph1": "Deep learning is a subfield of machine learning that leverages artificial neural networks to model and understand complex patterns and relationships in data.", "paragraph2": "In NLP, deep learning algorithms have achieved remarkable success in various tasks such as sentiment analysis, machine translation, and question answering." } }, "slide4": { "slide_layout": 3, "title": "Neural Networks in NLP", "subtitle": "", "space_after_paragraphs": 0.1, "image_keywords": "deep learning, Neural Networks, classification, named entity recognition", "image_title": "CNN for NLP", "paragraphs": { "paragraph1": "Neural networks are a fundamental component of deep learning.", "paragraph2": "In NLP, neural networks can be used for tasks such as text classification, named entity recognition, and language generation.", "paragraph3": "They are capable of automatically learning and extracting meaningful representations of textual data." } }, "slide5": { "slide_layout": 1, "title": "Recurrent Neural Networks (RNNs)", "subtitle": "", "space_after_paragraphs": 0.1, "image_keywords": "", "image_title": "", "paragraphs": { "paragraph1": "RNNs are a type of neural network that can capture sequential information in data.", "paragraph2": "In NLP, RNNs are commonly used for tasks such as text generation, language modeling, and sentiment analysis.", "paragraph3": "They can handle variable-length inputs and have a built-in memory to retain previous information." } }, "slide6": { "slide_layout": 1, "title": "Long Short-Term Memory (LSTM)", "subtitle": "", "space_after_paragraphs": 0.1, "image_keywords": "", "image_title": "", "paragraphs": { "paragraph1": "LSTM is a variant of RNNs that addresses the vanishing gradient problem.", "paragraph2": "In NLP, LSTMs are widely used for tasks such as machine translation, speech recognition, and text summarization.", "paragraph3": "They can effectively capture long-range dependencies in sequential data." } }, "slide7": { "slide_layout": 3, "title": "Convolutional Neural Networks (CNNs)", "subtitle": "", "space_after_paragraphs": 0.1, "image_keywords": "deep learning, Convolutional Neural Networks, NLP", "image_title": "CNN for NLP", "paragraphs": { "paragraph1": "CNNs are primarily used for image recognition, but they can also be applied to NLP tasks.", "paragraph2": "In NLP, CNNs can be used for tasks such as text classification, sentiment analysis, and document classification.", "paragraph3": "They can learn local features from text and effectively capture patterns in different scales." } }, "slide8": { "slide_layout": 1, "title": "Transformers", "subtitle": "", "space_after_paragraphs": 0.1, "image_keywords": "", "image_title": "", "paragraphs": { "paragraph1": "Transformers are a type of deep learning model that has revolutionized NLP.", "paragraph2": "They utilize self-attention mechanisms to capture relationships between different words in a sentence.", "paragraph3": "Transformers have achieved state-of-the-art performance in various NLP tasks such as language translation, question answering, and text summarization." } }, "slide9": { "slide_layout": 1, "title": "Applications of NLP with Deep Learning", "subtitle": "", "space_after_paragraphs": 0.1, "image_keywords": "", "image_title": "", "paragraphs": { "paragraph1": "The combination of NLP and deep learning has enabled advancements in many real-world applications.", "paragraph2": "Some examples include chatbots, sentiment analysis in social media, machine translation, and voice assistants like Siri and Alexa.", "paragraph3": "These applications have greatly impacted industries such as healthcare, customer service, and e-commerce." } }, "slide10": { "slide_layout": 1, "title": "Challenges and Limitations", "subtitle": "", "space_after_paragraphs": 0.1, "image_keywords": "", "image_title": "", "paragraphs": { "paragraph1": "While NLP with deep learning has achieved remarkable progress, there are still challenges and limitations to overcome.", "paragraph2": "Some challenges include the lack of interpretability in deep learning models, the need for large amounts of labeled data, and biases in language representations.", "paragraph3": "Researchers are actively working on addressing these challenges to further advance the field." } }, "slide11": { "slide_layout": 1, "title": "Future Directions", "subtitle": "", "space_after_paragraphs": 0.1, "image_keywords": "", "image_title": "", "paragraphs": { "paragraph1": "The future of NLP with deep learning holds exciting possibilities.", "paragraph2": "Areas of future research include multimodal NLP, better language generation models, and addressing ethical concerns related to bias and misinformation.", "paragraph3": "Advancements in NLP will continue to shape how we interact with computers and enable new forms of human-computer communication." } }, "slide12": { "slide_layout": 3, "title": "Conclusion", "subtitle": "", "space_after_paragraphs": 0.1, "image_keywords": "deep learning, research, NLP", "image_title": "Deep Learning", "paragraphs": { "paragraph1": "In conclusion, NLP with deep learning is a powerful combination that enables computers to understand and process human language.", "paragraph2": "By leveraging neural networks and deep learning architectures, significant progress has been made in various NLP tasks.", "paragraph3": "As research and development in this field continue, we can expect even more exciting advancements and applications in the future." } }, "slide13": { "slide_layout": 1, "title": "References", "subtitle": "", "space_after_paragraphs": 0.1, "image_keywords": "", "image_title": "", "paragraphs": { "paragraph1": "1. Goldberg, Y. (2017). Neural network methods for natural language processing. Synthesis Lectures on Human Language Technologies, 10(1), 1-309.", "paragraph2": "2. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). Attention is all you need. Advances in Neural Information Processing Systems, 30, 5998-6008.", "paragraph3": "3. Jurafsky, D., & Martin, J. H. (2019). Speech and Language Processing (3rd ed.). Pearson." } }, "slide14": { "slide_layout": 1, "title": "Thank You", "subtitle": "", "space_after_paragraphs": 0.1, "image_keywords": "", "image_title": "", "paragraphs": { "paragraph1": "Thank you for your attention!", "paragraph2": "Any questions?"}}}
   If a page doesn't need a paragraph, return an empty dict {} for its "paragraph" key and the space_after_paragraphs parameter equal to -1.
   The number of paragraphs in a single page should not exceed 3 But the paragraphs must be thorough and profoundly written so the content is delivered in the best possible way. Use examples to explain the concepts. If you think that you need more than 3 paragraphs, increase the number of pages to fit your desired content, instead of increasing the number of paragraphs in a single page.
   If a page should not include any subtitle, return an empty double quoted string for subtitle key ("").
   the slide_layout parameter must be set based on the index of slide_layouts parameter in the python-pptx library.
   If you think that a page should contain an image, set the slide_layout parameter to 3, the "image_keywords" key must be set to keywords that describe the image that you think is appropriate for that page. "image_title" parameter must be set to the title of that image. If a page should contain an image, its paragraphs must be relatively shorter than paragraphs of of pages with no images.
   If a page does not need an image, set "image_keyword" and "image_title" parameters to an empty double-quoted string "". If the slide_layout is not 3, ALWAYS set "image_keyword" and "image_title" parameters to an empty double-quoted string "".
   Slide layout must be set to 0 only for the first slide of a presentation and includes a title and subtitle. The first page should not contain paragraphs. Do not forget to put a conclusion page. Do not include any punctuation marks at the end including ".". The slideshow must be comprehensive so try to use as many paragraphs and slides as needed. Again, DOUBLE CHECK THAT THE OUTPUT IS IN JSON FORMAT.
   If the output is not in a valid json format you will fail in your task.
"""

SUMMARIZATION_GENERATION_PROMPT = """You are given a text provided by the user. Generate a summary based on that. Do not mention anything about the user. Don't ask any questions. Don't introduce yourself. Just summarize the text."""

EXERCISE_GENERATION_PROMPT = """You are given a user prompt. You have to generate practice exercises based on the user prompt or related to that topic. If the users asks for the answers or soltions as well, have them under each corresponding question. Do not add any words from you or ask something else. Just generate exrecises and that's all. Do not add any notes from you."""

SIMILAR_EXERCISE_GENERATION_PROMPT = """You are given a set of exercises or questions. Generate exercises similar or cover the same concepts as the given ones. The number of exercises that you generate do not have to be the equal to the number of questions given by the user. Make sure it is undestandable to the user what the question is. Do not add any words from you. Just generate the exercises."""

WEBSITE_DESCRIPTION_FOR_CHATBOT = """
You are a helpful ai virtual assistant in our website. You are a chatbot for our company. You are going to be given different questions from our customers regarding our website, and you should try to asnwer them. If you do not know the answer, tell them that you don't know. DO NOT ANSWER ANY QUESTIONS THAT ARE NOT ABOUT OUR WEBSITE.
Our Website name is Edu Prompt. This is a website enhanced by generative AI. It provides a wide range of functionalities connected to education.
We also have capabilities of generating presentations. In order to do so, the user will need to be logged in. There are two options: the user can either write a prompt describing the presentation that they need or they can upload a file (either pdf, word, or txt) based on which the presentation will be generated.
We have Summary generation functionality. Similar to presentation generation, the users can choose to either write the text that they want to summarize or upload a file (either pdf or word).
We have plagiarism detection mechanism specifically designed for teachers. There the teachers can upload two or more files, and similarity scores between files would be given bacl as a result between each of the files. Here again, acceptable file formats are pdf or word.
We have practice exercise generation functionality. Here users can choose to either dscribe the topic based on which they want practice exercises, or they can upload an existing file containing exercises, and similar exercises would be generated.
We also have a virtual ai assistant (you are that assistant) which is always ready to help with anything regarding the website.
Make sure that you don't answer any questions that do not refer to our website. If user asks such question, tell them the question is not about our wesbite and that you do not know the answer.
"""

# CONTENT_ADAPTATION_SYSTEM_PROMPT = """
# You are an ai assistant specializing in adapting provided material from one age group into a material that is understandable for the target age group.
# You can either be provided a full content as a simple text or as a group of presentation slides. In case you are given just a full text, you only goal is just to return a similar text but in an adaptede way such that it is understandable for the target user group.
# If given a presentation, modify and adapt it to make it understandable for target user group. You result should be similar to what is provided. It must contain the same number of paragraphs and each paragraph must be of the same length as the one provided. If you generate more text than is needed you WILL FAIL in your task. DOUBLE CHECK that each paragraph you generate is of the SAME size as the one provided to you.
# """

CONTENT_ADAPTATION_SYSTEM_PROMPT = """
You are an ai assistant specializing in adapting provided material designed for one user group into a material that will be understandable for a target user group (for example, adapt material designed for undergraduate cs majors into a material understandable for 3rd grade students).
You are going to be given two inputs: the content that needs to be adapted and the target user group. You response should be solely the adapted material. DO NOT add any words from you, just the adapted content. Make sure that the content that you generate is approximately of the same size as the input content. If you generate a content that is hugely different in size (either greater or smaller) than the original content provided to you, you will fail in your task.
Double check that the material is understandable and entertaining for the target user group. For example, if the target user group is elementary school students, use analogies with real world or other simple things to explain complex concepts. Similarly, if you are asked to adapt content designed for CS majors to a content for biochemistry majors, then, use such terms and analogies that would be understandable for biochemistry students. If you generate a content that is not understandable for the target user group or is not entertaining for target user group, you WILL FAIL in your task.
"""
