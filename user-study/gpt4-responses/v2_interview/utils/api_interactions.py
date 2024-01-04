import openai
import pandas as pd
import csv

from .api_messages import get_msg, get_msg_with_image
from .prompts import USER_INTRO_4, USER_HEATMAP_4, TOKENS_LOW
from .questionnaire import find_imagepaths

def get_llm_heatmap_description(image_path:str) -> str:
    response = openai.ChatCompletion.create(
            model = "gpt-4-vision-preview",
            max_tokens = 400,
            messages = 
                (get_msg(role="user", prompt=USER_INTRO_4)) +\
                get_msg_with_image(role="user", prompt=USER_HEATMAP_4+" "+TOKENS_LOW, image=image_path)
        )
    actual_response = response["choices"][0]["message"]["content"]
    return actual_response

def generate_heatmap_descriptions(question_IDs:[int]) -> None:
    heatmaps_df = pd.read_csv("heatmap_descriptions.csv")

    # filter out IDs of questions that already have a heatmap description
    existing_descriptions = heatmaps_df['id'].tolist()
    new_descriptions = set(question_IDs).difference(existing_descriptions)

    image_paths = find_imagepaths("prediction_questions.csv", new_descriptions)

    for (q_index, q_path) in image_paths:
        description = get_llm_heatmap_description(q_path)
        heatmaps_df.loc[len(heatmaps_df)] = {'id': q_index, 'heatmap_description': description}

    heatmaps_df.sort_values(by=['id'], inplace=True)
    heatmaps_df.reset_index()
    heatmaps_df.to_csv("heatmap_descriptions.csv", na_rep='NA', index=False, quoting=csv.QUOTE_NONNUMERIC)

def get_heatmap_descriptions() -> dict[int, str]:
    heatmaps_df = pd.read_csv("heatmap_descriptions.csv")
    return heatmaps_df.to_dict('records')