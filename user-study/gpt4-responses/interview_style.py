import interview_util_prompts
import interview_util
import openai
import os
import pandas as pd

# df['output_2'] = (df['input_1'] + df['input_2'])

openai.api_key = os.environ["OPENAI_API_KEY"]

def get_response(row):
    messages = interview_util.MESSAGE_BASE

# def get_response(row, colnames:list, question:str):
#     messages = interview_util.MESSAGE_BASE

#     response = openai.ChatCompletion.create(
#         model = "gpt-4-vision-preview",
#         max_tokens = 300,
#         messages = messages
#     )
#     pass

# print(response)
# print(response["choices"][0]["message"]["content"])