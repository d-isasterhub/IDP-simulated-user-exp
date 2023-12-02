# Imports


# Utils
def get_msg(role:str, prompt:str):
    ''' Creates a message that can directly be used for an OpenAI api call: 
    messages = get_msg(role, prompt)

    To concatenate messages, write the following (example):
    messages = get_msg(role1, prompt1) + get_msg(role2, prompt2)
    
    Args:
        role (str) : a valid role (system, user, assistant)
        prompt (str) : the content of the message

    Returns:
        msg (list) : the message in a format directly usable for OpenAI api calls
    '''
    _role_check(role)
    msg = [
        {"role": role, "content": prompt}
    ]
    return msg

def get_msg_with_image(role:str, prompt:str, image:str):
    ''' Creates a message that can directly be used for an OpenAI api call and contains one
    image: 
    messages = get_msg_with_image(role, prompt, image)

    To concatenate the generated message with other messages, write the following (example):
    messages = get_msg(role1, prompt1) + get_msg(role2, prompt2, image2)
    
    Args:
        role (str) : a valid role (system, user, assistant)
        prompt (str) : the content of the message
        image (str) : the name of the image (e.g. "0-Crested.png"), the image must be in the 
                      images folder and uploaded to github

    Returns:
        msg (list) : the message in a format directly usable for OpenAI api calls
    '''
    _role_check(role)
    img_url = "https://github.com/d-isasterhub/IDP-simulated-user-exp/blob/main/images/" + image + "?raw=true"
    print(img_url)
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
    ''' Checks whether the given role is valid. Throws an error if the role is not valid.
    Accepted roles:
    - system
    - user
    - assistant
    
    Args:
        role (str) : the role to be tested
    '''
    roles = ['system', 'user', 'assistant']
    if role not in roles:
        raise ValueError("Invalid role type. Expected one of: %s" % roles)