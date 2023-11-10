import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

response = openai.ChatCompletion.create(
    model = "gpt-4-vision-preview",
    messages = [
        {"role": "system", "content": ""},
        # (Optionally)
        # {"role": "assistant", "content": ""},
        # {"role": "user", "content": ""}m
        {
            "role": "user", 
            "content": [
                {
                    "type": "text", "text": "What can you see in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": "https://github.com/d-isasterhub/IDP-simulated-user-exp/blob/main/images/015_X_cam.jpg?raw=true"
                }
            ]
        }
    ]
)

print(response["choices"][0]["message"]["content"])