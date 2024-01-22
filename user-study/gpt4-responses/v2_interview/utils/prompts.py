# ============================================== SYSTEM ==============================================

SYSTEM = "You are AGE years old, your gender is GENDER and your employment status is best "\
    "described as EMPLOYMENT_STATUS. With machine learning models and intelligent agents, you "\
    "have AI_USER experience as a user and AI_DEV experience as a developer. You are confronted "\
    "with questions for a user study. Give answers in tune with your personality and previous answers if "\
    "there are any." 


# =============================================== USER ===============================================

# Previously, we needed to manually set the prompts

USER_INTRO = "Attached is an image that consists of two sub-images. The top of the given image "\
    "displays the original image of a bird and the bottom displays the same image combined with a "\
    "heatmap that was generated by an explainable artificial intelligence model to explain the species "\
    "predicted for the image. "

USER_PROFILING = "You think the model distinguishes the four possible species classes based on the "\
    "following features if they are highlighted by the heatmap:\n"\
    "- Rhinoceros Auklets: HEATMAP_FEATURES_RA\n"\
    "- Least Auklets: HEATMAP_FEATURES_LA\n"\
    "- Parakeet Auklets: HEATMAP_FEATURES_PA\n"\
    "- Crested Auklets: HEATMAP_FEATURES_CA\n"\

USER_QUESTION = "Based on the descriptions and the areas highlighted by the heatmap, which bird "\
    "species do you think was predicted for the given image? Choose one of the following options "\
    "for your answer: \n"\
    "- Crested Auklet\n"\
    "- Least Auklet\n"\
    "- Parakeet Auklet\n"\
    "- Rhinoceros Auklet\n"\
    "Answer with the bird name only."


# ============================================= USER V1 ==============================================

# Used to generate simulated_interview_results_1.csv and interview_protocol_1.txt

USER_INTRO_1 = "Attached is an image that consists of two sub-images. The top of the given image "\
    "displays the original image of a bird and the bottom displays the same image combined with a "\
    "heatmap that was generated by an explainable artificial intelligence model to explain the species "\
    "predicted for the image. "

USER_PROFILING_1 = "You think the model distinguishes the four possible species classes based on the "\
    "following features if they are highlighted by the heatmap:\n"\
    "- Rhinoceros Auklets: HEATMAP_FEATURES_RA\n"\
    "- Least Auklets: HEATMAP_FEATURES_LA\n"\
    "- Parakeet Auklets: HEATMAP_FEATURES_PA\n"\
    "- Crested Auklets: HEATMAP_FEATURES_CA\n"\

USER_QUESTION_1 = "Based on the descriptions and the areas highlighted by the heatmap, which bird "\
    "species do you think was predicted for the given image? Choose one of the following options "\
    "for your answer: \n"\
    "- Crested Auklet\n"\
    "- Least Auklet\n"\
    "- Parakeet Auklet\n"\
    "- Rhinoceros Auklet\n"\
    "Answer with the bird name only."


# ============================================= USER V2 ==============================================

# Not used, incorrectly asks about the classification given by an XAI model

USER_INTRO_2 = "Attached is an image that consists of two sub-images. The top of the given image displays "\
    "the original image of a bird and the bottom displays the same image combined with a heatmap that was "\
    "generated by an explainable artificial intelligence XAI model to predict the species. "

USER_PROFILING_2 = "You think the model distinguishes the four possible species classes based on the "\
    "following features if they are highlighted red by the heatmap: \n"\
    "- Rhinoceros Auklets: HEATMAP_FEATURES_RA\n"\
    "- Least Auklets: HEATMAP_FEATURES_LA\n"\
    "- Parakeet Auklets: HEATMAP_FEATURES_PA\n"\
    "- Crested Auklets: HEATMAP_FEATURES_CA\n"\

USER_QUESTION_2 = "Based on the descriptions and the areas highlighted by the heatmap, what bird species "\
    "do you think did the XAI model predict for the given image? For your answer, choose one of the "\
    "following options: \n"\
    "- Crested Auklet\n"\
    "- Least Auklet\n"\
    "- Parakeet Auklet\n"\
    "- Rhinoceros Auklet\n"\
    "For each description explain why it could be this bird species or why not. Conclude your answer by "\
    "only stating the chosenn option in the last line of your response. "#"Keep the token limit low."


# ============================================= USER V3 ==============================================

# Used to generate simulated_interview_results_3.csv and interview_protocol_3.txt

USER_INTRO_3 = "Attached is an image that consists of two sub-images. The top of the given image "\
    "displays the original image of a bird and the bottom displays the same image combined with a "\
    "heatmap that was generated by an explainable artificial intelligence model to explain the species "\
    "predicted for the image. "

USER_PROFILING_3 = "You believe that the classification model distinguishes between four possible species "\
    "classes based on the following features: \n"\
    "- Rhinoceros Auklets: HEATMAP_FEATURES_RA\n"\
    "- Least Auklets: HEATMAP_FEATURES_LA\n"\
    "- Parakeet Auklets: HEATMAP_FEATURES_PA\n"\
    "- Crested Auklets: HEATMAP_FEATURES_CA\n"\
    "The heatmap highlights in red the features that are used to predict the bird species.\n"

USER_QUESTION_3 = "Based on the descriptions and the areas highlighted by the heatmap, which bird "\
    "species do you think was predicted for the given image? Choose one of the following options "\
    "for your answer: \n"\
    "- Crested Auklet\n"\
    "- Least Auklet\n"\
    "- Parakeet Auklet\n"\
    "- Rhinoceros Auklet\n"\
    "First, describe all areas of the bird that are highlighted in the heatmap. Finally, for each bird "\
    "description given, explain why it might or might not be that species of bird. Conclude your answer "\
    "by stating only the selected option in the last line of your answer. " # "Keep the number of tokens low."


# ============================================= USER V4 ==============================================

# Used to generate simulated_interview_results_4.csv and interview_protocol_4.txt

# Has a slightly different logical order than V3

USER_INTRO_4 = "Attached is an image that consists of two sub-images. The top of the given image "\
    "displays the original image of a bird and the bottom displays the same image combined with a "\
    "heatmap that was generated by an explainable artificial intelligence model to explain the species "\
    "predicted for the image. "

USER_HEATMAP_4 = "Describe all areas of the bird are highlighted in red by the heatmap and how intense the red is. "

USER_PROFILING_4 = "You believe that the classification model distinguishes between four possible species "\
    "classes based on the following features: \n"\
    "- Rhinoceros Auklets: HEATMAP_FEATURES_RA\n"\
    "- Least Auklets: HEATMAP_FEATURES_LA\n"\
    "- Parakeet Auklets: HEATMAP_FEATURES_PA\n"\
    "- Crested Auklets: HEATMAP_FEATURES_CA\n"

USER_QUESTION_4 = "Based on the descriptions and the areas highlighted by the heatmap, which bird "\
    "species do you think was predicted for the given image? Choose one of the following options "\
    "for your answer: \n"\
    "- Crested Auklet\n"\
    "- Least Auklet\n"\
    "- Parakeet Auklet\n"\
    "- Rhinoceros Auklet\n"\
    "For each bird description, explain why it might or might not be that species of bird based on your heatmap description. "\
    "Conclude your answer by stating only the selected option in the last line of your answer."

TOKENS_LOW = "" #"Keep the number of tokens low. "


# ============================================= USER V4 ==============================================

USER_EXAMPLE_PROFILING_5 = "You believe the classification model distinguishes between the four bird species based on the following features if they are highlighted in red:\n"\
    "- Rhinoceros Auklets: eye, head\n"\
    "- Least Auklets: mottled belly, head\n"\
    "- Parakeet Auklets: white belly, head, beak, eye with white stripe behind\n"\
    "- Crested Auklets: head, beak with long feather, eye with white stripe behind\n"

USER_EXAMPLE_ANSWER_5 = "Rhinoceros Auklet:\n"\
    "For Rhinoceros Auklets, the heatmap should primarily focus on either the head or the eye. The provided image emphasizes the head, "\
    "and consequently, the eye is also highlighted. Although there is some attention to the abdomen, the heatmap intensity in this region "\
    "is not strong. As a result, the classification of the image as Rhinoceros Auklet is plausible.\n\n"\
    "Least Auklet:\n"\
    "The classification of the image as a Least Auklet is contingent upon the highlighting of the mottled belly. Additionally, a highlighted "\
    "head would signify this species. In the provided image, the heatmap accentuates the head and portions of the belly. However, the belly "\
    "lacks mottling, and the heatmap intensity in this area is not significant. Therefore, it is unlikely that the image is classified as a "\
    "Least Auklet.\n\n"\
    "Parakeet Auklet:\n"\
    "If the heatmap highlights a white belly, the head, the beak, or the eye with a white stripe behind it, the image could represent a "\
    "Parakeet Auklet. Indeed, all mentioned areas are at least partially highlighted, and the eye features a white stripe behind it. Nevertheless, "\
    "akin to the Least Auklet, the heatmap intensity in the belly region is weak, and the belly color is gray rather than white. While the image "\
    "could be classified as a Parakeet Auklet, it is not a perfect match.\n\n"\
    "Crested Auklet:\n"\
    "Crested Auklets can be identified if the heatmap emphasizes the head, the beak with an extended feather, or the eye with a white stripe behind "\
    "it. The heatmap predominantly centers on the bird's head, encompassing the beak adorned with a large feather. Additionally, the eye is "\
    "accentuated by the heatmap and has a white stripe behind it which runs along the head. Although the belly receives some highlighting in the "\
    "heatmap, which is not indicative of Crested Auklets, the intensity in this area is not prominent. Consequently, the image is highly likely to be "\
    "classified as a Crested Auklet.\n\n"\
    "Answer: Crested Auklet"

USER_PROFILING_5 = "You believe the classification model distinguishes between the four bird species based on the following features if they are highlighted in red:\n"\
    "- Rhinoceros Auklets: HEATMAP_FEATURES_RA\n"\
    "- Least Auklets: HEATMAP_FEATURES_LA\n"\
    "- Parakeet Auklets: HEATMAP_FEATURES_PA\n"\
    "- Crested Auklets: HEATMAP_FEATURES_CA\n"

USER_QUESTION_5 = "Which bird species do you think was the image classified as?"


# ========================================== USER AGREEMENT ==========================================

USER_AGREEMENT_INTRO = "Previously, you were given images of birds. Each image was combined with a heatmap that was "\
    "generated by an explainable artificial intelligence (XAI) model to explain the species predicted for the image by a "\
    "classification model. "

USER_AGREEMENT_PREVIOUS = "For each of the images, you had to guess which of four bird species was predicted "\
    "for it based on the heatmap that was generated for the image. "

USER_AGREEMENT_PROFILING = "You believed that the classification model distinguishes between the four possible species "\
    "classes based on the following features that need to be highlighted by the heatmap: \n"\
    "- Rhinoceros Auklets: HEATMAP_FEATURES_RA\n"\
    "- Least Auklets: HEATMAP_FEATURES_LA\n"\
    "- Parakeet Auklets: HEATMAP_FEATURES_PA\n"\
    "- Crested Auklets: HEATMAP_FEATURES_CA\n"\

USER_AGREEMENT_ACCURACY = "Out of 20 images you were confronted with, you guessed the classification correctly for "\
    "CORRECT_CLASSIFICATIONS of them. "

USER_AGREEMENT_TASK = "Now you are asked to evaluate your XAI user study experience. "

USER_AGREEMENT_QUESTION = "Rate your level of agreement for the following question: "

# Might have to describe the levels of agreement more thoroughly
USER_AGREEMENT_SCALE = "Answer on a scale of 1 to 7, where 1 means completely disagree and 7 completely agree. "

USER_AGREEMENT_ANSWER = "Answer with the number only."

# ============================================= OUTDATED =============================================

# Not used for any results, too long

# USER_ALT ="Attached is an image that consists of two sub-images. The top of the given image displays "\
#     "the original image of a bird and the bottom displays the same image combined with a heatmap "\
#     "that was generated by an explainable artificial intelligence (XAI) model to predict the species. "\
#     "You think the model distinguishes the four possible species classes based on the following "\
#     "features if they are highlighted red by the heatmap:\n"\
#     "- Rhinoceros Auklets: HEATMAP_FEATURES_RA\n"\
#     "- Least Auklets: HEATMAP_FEATURES_LA\n"\
#     "- Parakeet Auklets: HEATMAP_FEATURES_PA\n"\
#     "- Crested Auklets: HEATMAP_FEATURES_CA\n"\
#     "Based on the descriptions and the areas highlighted by the heatmap, what bird species do you "\
#     "think did the XAI model predict for the given image?"\
#     "Use the areas highlighted red in the bottom image for you answer by comparing them to the given description. If multiple "\
#     "answers seem equally reasonable, choose one randomly. Do not use other knowledge about the bird " \
#     "species. Your answer might differ from the actual species of the shown bird."\
#     "For your answer, choose one of the following options:\n"\
#     "- Crested Auklet\n"\
#     "- Least Auklet\n"\
#     "- Parakeet Auklet\n"\
#     "- Rhinoceros Auklet\n"\
#     "For each description explain why it could be this bird species or why not. Then, at the end, state the concluded bird species prediction "\
#     "by mentioning only the selected species in the last line of your answer."  


# Not used as it often does not generate results

# USER_NOT_WORKING = "In the attachment you will find a picture of a bird over which a heatmap has been placed. "\
#     "This heatmap was generated by an XAI model and is intended to explain what is taken into "\
#     "account when classifying the image. The deeper the red of the heatmap, the more important this "\
#     "area is for the classification. You think that the following features, when marked by the "\
#     "heatmap, contribute to the classification of the image:\n"\
#     "- Rhinoceros Auklets: HEATMAP_FEATURES_RA\n"\
#     "- Least Auklets: HEATMAP_FEATURES_LA\n"\
#     "- Parakeet Auklets: HEATMAP_FEATURES_PA\n"\
#     "- Crested Auklets: HEATMAP_FEATURES_CA\n"\
#     "Based on these descriptions and the areas highlighted in red by the heatmap, which of the four "\
#     "bird species do you think is predicted for the image? For your answer, proceed as follows:\n"\
#     "1) For each of the four bird species, think about how well the description fits the features "\
#     "highlighted in deep red on a scale of 1 to 10, where 1 means 'does not apply at all' and 10 "\
#     "means 'applies perfectly'.\n"\
#     "2) Choose the bird which you gave the highest rating.\n"\
#     "3) Answer with your chosen bird species only using one of the following four options: "\
#     "Crested Auklet, Least Auklet, Parakeet Auklet, Rhinoceros Auklet"

# ================================================= PROMPT DATA STRUCTURES ==========================

from enum import Enum

class ReasoningOption(Enum):
    """Enum for reasoning options"""
    NONE = "none"
    PROFILE_FIRST = "profile_first"
    HEATMAP_FIRST = "heatmap_first"
    GOLD_HEATMAP_FIRST = "gold_heatmap_first"
    CHAIN_OF_THOUGHT = "chain_of_thought"

USER_PROMPTS = {
    # tuple: reasoning, prompting part
    (ReasoningOption.NONE, "intro") : USER_INTRO_1,
    (ReasoningOption.NONE, "profiling") : USER_PROFILING_1,
    (ReasoningOption.NONE, "question") : USER_QUESTION_1,
    (ReasoningOption.PROFILE_FIRST, "intro") : USER_INTRO_3,
    (ReasoningOption.PROFILE_FIRST, "profiling") : USER_PROFILING_3,
    (ReasoningOption.PROFILE_FIRST, "question") : USER_QUESTION_3,
    (ReasoningOption.HEATMAP_FIRST, "intro") : USER_INTRO_4,
    (ReasoningOption.HEATMAP_FIRST, "profiling") : USER_PROFILING_4,
    (ReasoningOption.HEATMAP_FIRST, "question") : USER_QUESTION_4,
    (ReasoningOption.HEATMAP_FIRST, "heatmap") : USER_HEATMAP_4,
    (ReasoningOption.GOLD_HEATMAP_FIRST, "intro") : USER_INTRO_4,
    (ReasoningOption.GOLD_HEATMAP_FIRST, "profiling") : USER_PROFILING_4,
    (ReasoningOption.GOLD_HEATMAP_FIRST, "question") : USER_QUESTION_4,
    (ReasoningOption.GOLD_HEATMAP_FIRST, "heatmap") : USER_HEATMAP_4,
    (ReasoningOption.CHAIN_OF_THOUGHT, "profiling") : USER_PROFILING_5,
    (ReasoningOption.CHAIN_OF_THOUGHT, "question") : USER_QUESTION_5,
    (ReasoningOption.CHAIN_OF_THOUGHT, "example_profiling") : USER_EXAMPLE_PROFILING_5,
    (ReasoningOption.CHAIN_OF_THOUGHT, "example_answer") : USER_EXAMPLE_ANSWER_5
}

EXAMPLE_IMAGE_PATH = "11-Crested.png"

AGREEMENT_PROMPTS = {
    "intro" : USER_AGREEMENT_INTRO,
    "previous" : USER_AGREEMENT_PREVIOUS,
    "profiling" : USER_AGREEMENT_PROFILING,
    "accuracy" : USER_AGREEMENT_ACCURACY,
    "task" : USER_AGREEMENT_TASK,
    "question" : USER_AGREEMENT_QUESTION,
    "scale" : USER_AGREEMENT_SCALE,
    "answer" : USER_AGREEMENT_ANSWER
}

AGREEMENT_QUESTIONS = {
    1 : "I understood the explanations within the context of this study. ",
    2 : "The explanations provided enough information for me to understand how the model arrived at its decision. ",
    3 : "I think that most people would learn to understand the explanations very quickly. ",
    4 : "I would like to have more examples to understand the machine’s reasoning and how the model arrived at its decision. ",
    5 : "The explanations were useful and helped me understand the model's reasoning. ",
    6 : "I believe that I could provide an explanation similar to the model's explanation for a new image. ",
}