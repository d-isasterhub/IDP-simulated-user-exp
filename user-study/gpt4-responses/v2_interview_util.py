# Imports


# Utils
def get_msg(role:str, prompt:str):
    # allows you to simply concatenate messages (messages = msg1 + msg2)
    _role_check(role)
    msg = [
        {"role": role, "content": prompt}
    ]
    return msg

def get_msg_with_image(role:str, prompt:str, image:str):
    # image example: "9-Crested.png", maybe modify to take links instead
    _role_check(role)
    img_url = "https://github.com/d-isasterhub/IDP-simulated-user-exp/blob/main/images/" + image + "?raw=true"
    msg = [{"role": role, "content": [
        {
            "type": "text", 
            "text": prompt
        },
        {
            "type": "image_url",
            "image_url": img_url
        }
    ]}]
    return msg
    

def _role_check(role:str):
    # TODO: system, user, assistant
    pass