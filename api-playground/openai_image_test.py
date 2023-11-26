import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

system = "You are a human who has no knowledge of bird species. "\
    "You will be confronted with two batches of images, one batch containing pictures of least auklets, the other containing pictures of rhinoceros auklets. "\
        "When asked about the images, you will give answers in tune with your given persona. Do not use knowledge that you can't deduct from the images."

user1 = "In the following picture you see least auklets."
user2 = "In the following picture you see rhinoceros auklets."
user3 = "Based on the pictures I have given you, write down what features you can use to distinguish these two species. For example, 'Least Auklet: dark gray wings'."

response = openai.ChatCompletion.create(
    model = "gpt-4-vision-preview",
    max_tokens = 300,
    messages = [
        {"role": "system", "content": system},
        # (Optionally)
        # {"role": "assistant", "content": ""},
        # {"role": "user", "content": ""}
        {
            "role": "user", 
            "content": [
                {
                    "type": "text", "text": user1
                },
                {
                    "type": "image_url",
                    "image_url": "https://github.com/d-isasterhub/IDP-simulated-user-exp/blob/main/images/leastauklet_01.png?raw=true"
                },
                {
                    "type": "image_url",
                    "image_url": "https://github.com/d-isasterhub/IDP-simulated-user-exp/blob/main/images/leastauklet_02.png?raw=true"
                },
                {
                    "type": "image_url",
                    "image_url": "https://github.com/d-isasterhub/IDP-simulated-user-exp/blob/main/images/leastauklet_03.png?raw=true"
                },
                {
                    "type": "image_url",
                    "image_url": "https://github.com/d-isasterhub/IDP-simulated-user-exp/blob/main/images/leastauklet_04.png?raw=true"
                }
            ]
        },

        {
            "role": "user", 
            "content": [
                {
                    "type": "text", "text": user2
                },
                {
                    "type": "image_url",
                    "image_url": "https://github.com/d-isasterhub/IDP-simulated-user-exp/blob/main/images/rhinocerosauklet_01.png?raw=true"
                },
                {
                    "type": "image_url",
                    "image_url": "https://github.com/d-isasterhub/IDP-simulated-user-exp/blob/main/images/rhinocerosauklet_02.png?raw=true"
                },
                {
                    "type": "image_url",
                    "image_url": "https://github.com/d-isasterhub/IDP-simulated-user-exp/blob/main/images/rhinocerosauklet_03.png?raw=true"
                },
                {
                    "type": "image_url",
                    "image_url": "https://github.com/d-isasterhub/IDP-simulated-user-exp/blob/main/images/rhinocerosauklet_04.png?raw=true"
                }
            ]
        },

        {
            "role": "user", 
            "content": [
                {
                    "type": "text", "text": user3
                }
            ]
        }
    ]
)

print(response)
print(response["choices"][0]["message"]["content"])