SYSTEM = "You are a human answering a questionnaire for a study, where the topic is the "\
    "understanding of Explainable Artificial Intelligence (XAI) images. The questionnaire "\
    "is carried out in form of an interview, where I am the interviewer and you are the "\
    "interviewee. So far, you have answered questions about your persona and were given an "\
    "introduction and an objective description. Further, you have answered a couple of "\
    "questions about XAI images, where you had to guess how the XAI model has classified "\
    "an images based on the explanations it produced. When answering further, similar "\
    "questions, give answers in tune with your persona and based on your previous answers. "\
    "Answer in a consistent style."

USER_AGE = "What is your age in years?"

USER_SEX = "What is your sex? Choose from the following options:\n"\
    "- Female\n"\
    "- Male\n"\
    "- Prefer not to say"

USER_EMPLOYMENT_STATUS = "What desccribes your employment statusover the last three month best? "\
    "Choose from the following options:\n"\
    "- Working full-time\n"\
    "- Working part-time\n"\
    "- Unemployed and looking for work\n"\
    "- Freelancer\n"\
    "- Student\n"\
    "- Retired\n"\
    "- Other"

USER_ML_EXPERIENCE_1 = "What is your prior experience with machine learning models and intelligent "\
    "agents (e.g. Alexa, Siri)? Choose from the following options:\n"\
    "- No experience\n"\
    "- User\n"\
    "- Programmer / developer"

USER_ML_EXPERIENCE_2 = "If you have had prior experience with machine learning models or "\
    "intelligent agents, please explain your experience."

OBJECTIVE_DESCRIPTION_1 = "The objective of this study is to explore approaches to explain the "\
    "decision-making process of machine-learning models to human end-users like you. During the "\
    "study, you will be presented with an image classification task and asked to learn and "\
    "respond to related questions.\nYour task will involve comprehending how the machine-learning "\
    "model identifies the class label for each image, using the provided examples."

OBJECTIVE_DESCRIPTION_2 = "We will start with a warm-up task: I will give you images of two "\
    "species of birds, namely the Least Auklet and the Rhinoceros Auklet. You will be confronted "\
    "with two batches of images, one batch containing pictures of Least Auklets, the other "\
    "containing pictures of Rhinoceros Auklets."

WARM_UP_TASK_1_LEAST = "In the following images you see Least Auklets."

WARM_UP_TASK_1_RHINOCEROS = "In the following images you see Rhinoceros Auklets."

WARM_UP_TASK_1 = "Based on the images I have given you, write down what features you can use to "\
    "distinguish these two species. For example, 'Least Auklet: dark gray wings'."

WARM_UP_TASK_1_LEAST_ANSWER = "Least Auklet:\nANSWER"

WARM_UP_TASK_1_RHINOCEROS_ANSWER = "Rhinoceros Auklet:\nANSWER"

OBJECTIVE_DESCRIPTION_3 = "Great, you just found a way to distinguish between Least Auklet and "\
    "Rhinoceros Auklet! Now, I have a bigger challenge for you: two of the Least Auklet images "\
    "are actually Parakeet Auklets and two of the Rhinoceros are actually Crested Auklets. To "\
    "understand how the model distinguishes these four species (Least, Parakeet, Rhinoceros, and "\
    "Crested), the machine-learning model generated 'heatmaps' which highlight the important "\
    "feature (the red area) that the machine-learning model uses to determine the species.\n"\
    "I will show you four 4 groups of images, one for each of the bird species. Each image I'll "\
    "show you consists of two sub-images. The top of the given images displays the original image "\
    "and the bottom displays the image combined with the heatmap generated by the machine-"\
    "learning model. The goal of your task is to understand the model's reasoning based on the "\
    "highlighted features (areas)."

WARM_UP_TASK_2_RHINOCEROS = "In the following images you see Rhinoceros Auklets."

WARM_UP_TASK_2_LEAST = "In the following images you see Least Auklets."

WARM_UP_TASK_2_PARAKEET = "In the following images you see Parakeet Auklets."

WARM_UP_TASK_2_CRESTED = "In the following images you see Crested Auklets."

WARM_UP_TASK_2 = "Please write down important features for each class that you learn from the "\
    "heatmaps, which are used by the model to distinguish this class from other classes."

WARM_UP_TASK_2_RHINOCEROS_ANSWER = "Rhinoceros Auklet:\nANSWER"

WARM_UP_TASK_2_LEAST_ANSWER = "Least Auklet:\nANSWER"

WARM_UP_TASK_2_PARAKEET_ANSWER = "Parakeet Auklet:\nANSWER"

WARM_UP_TASK_2_CRESTED_ANSWER = "Crested Auklet:\nANSWER"

OBJECTIVE_DESCRIPTION_4 = "Next, you will answer 20 questions. In each question, you will see an "\
    "image and its heatmap generated by the model. Along with the question, you are given "\
    "examples from each class you just saw above.\n Your task is to predict what label the model "\
    "will give according to its heatmap (reasoning)."

UNDERSTANDING_CHECK = "Before getting started, let's make sure that you understand the task. "\
    "Please choose the task that you will do:\n"\
    "- I will choose the label that I think is correct for the image\n"\
    "- I will choose the label that I think the model would predict"

CLASS_PREDICTION_Q1 = "I will again show you an image that consists of two sub-images. "\
    "The top of the given images displays the original image and the bottom displays the "\
    "image combined with the heatmap generated by the machine-learning model."\
    "Please choose the bird species for this image that the xai model might "\
    "choose based on its reasoning (highlighted area) that you see in the bottom part. "\
    "Choose one of the following options:\n"\
    "- Crested Auklet\n"\
    "- Least Auklet\n"\
    "- Parakeet Auklet\n"\
    "- Rhinoceros Auklet"
    
    