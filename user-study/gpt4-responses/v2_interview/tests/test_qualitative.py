import openai

# Does GPT-4 understand negative agreement answers?

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
    msg = [
        {"role": role, "content": prompt}
    ]
    return msg

def test_negative_agreement():
    USER_AGREEMENT_QUESTION = "You rate your level of agreement for the following statement: I would like to have more examples "\
        "to understand the machine's reasoning and how the model arrived at its decision. On a scale of 1 to 7, where 1 means "\
        "completely disagree and 7 completely agree, your answer was 6. "\
        "Is this positive or negative feedback for the model, meaning does it need improvement?."
    
    response = openai.ChatCompletion.create(
            model = "gpt-4-vision-preview",
            max_tokens = 400,
            messages = get_msg(role="user", prompt=USER_AGREEMENT_QUESTION)
        )
    actual_response = response["choices"][0]["message"]["content"]
    print(actual_response)

    with open("user-study/gpt4-responses/v2_interview/tests/test_negative_agreement.txt", "a+") as f:
        f.write(USER_AGREEMENT_QUESTION)
        f.write("\n")
        f.write(actual_response)
        f.write("\n\n")

def test_negative_agreement_2():
    USER_AGREEMENT_QUESTION = "Rate your level of agreement for the following statement: I would like to have more examples "\
        "to understand the machine's reasoning and how the model arrived at its decision. On a scale of 1 to 7, where 1 means "\
        "completely disagree and 7 completely agree, what would your answer be if you did not understand the model's reasoning well?"
    
    response = openai.ChatCompletion.create(
            model = "gpt-4-vision-preview",
            max_tokens = 400,
            messages = get_msg(role="user", prompt=USER_AGREEMENT_QUESTION)
        )
    actual_response = response["choices"][0]["message"]["content"]
    print(actual_response)

    with open("user-study/gpt4-responses/v2_interview/tests/test_negative_agreement.txt", "a+") as f:
        f.write(USER_AGREEMENT_QUESTION)
        f.write("\n")
        f.write(actual_response)
        f.write("\n\n")


# test_negative_agreement()
test_negative_agreement_2()