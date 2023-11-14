import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

system = "You are a human who has a lot of experience with Machine Learning and Artificial Intelligence. "\
    "You will be confronted with an image that has been created with an Explainable Artificial Intelligence (XAI) method "\
        "and explains the classification of a picture. When I ask questions about the XAI image, you will give me answers in tune with your given persona."

user = "Consider a Artificial Intelligence model that was trained to classify images. "\
    "The provided image has been created with the help of an XAI method. Which category do you think the model assigned to the image? "\
        "Give a brief explanation for your answer."

response = openai.ChatCompletion.create(
    model = "gpt-4-vision-preview",
    max_tokens = 300,
    messages = [
        {"role": "system", "content": system},
        # (Optionally)
        # {"role": "assistant", "content": ""},
        # {"role": "user", "content": ""}m
        {
            "role": "user", 
            "content": [
                {
                    "type": "text", "text": user
                },
                {
                    "type": "image_url",
                    "image_url": "https://github.com/d-isasterhub/IDP-simulated-user-exp/blob/main/images/010_X_cam.jpg?raw=true"
                }
            ]
        }
    ]
)

print(response)
print(response["choices"][0]["message"]["content"])