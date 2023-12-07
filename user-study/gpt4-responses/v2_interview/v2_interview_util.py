# Imports
import pandas as pd
import random


# -------------------------------------------- Interactions with the OpenAI API ----------------------------------------------------------

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


# ----------------------------------------------- During interview ---------------------------------------------------------------

def check_answer_exists():
    pass


def save_result_df(df:pd.DataFrame):
    df.sort_values(by=['id'], inplace=True)
    df.reset_index()
    df.to_csv('out/simulated_interview_results.csv', na_rep='NA')
    

# ------------------------------------------------ Interview Setup ----------------------------------------------------------------

def read_questions(path_to_csv:str, indices:[int]) -> [(int, str)]:
    """Reads file paths associated with questions from csv file
    
    Args:
        path_to_csv (str) : path to csv file with file paths for each question
        indices ([int]) : list of question indices (starting with 1)
        
    Returns:
        ([(int, str)]) : list of index-filepath pairs
    """
    questions_df = pd.read_csv(path_to_csv)
    return [(i, questions_df.at[i-1, "image_path"]) for i in indices]


def select_questions(n=1, method='balanced') -> [int]:
    """Selects n question indices in [1..20] using the specified selection method (default: 'balanced').
    balanced: 1, 6, 11, 16, 2, 7, 12, 17, ...
    random: as expected
    first: 1, 2, 3, 4...

    Args:
        n (int) : number of questions to select
        method (string) : how to select the questions. options: balanced, random, first
    
    Returns:
        ([int]) : a list of question indices
    """
    
    selection_methods = ['random', 'balanced', 'first']

    if method not in selection_methods:
        raise ValueError("Invalid selection method. Expected one of: %s" % selection_methods)
    
    n = max(n, 20)

    # select number_questions out of 20 using selected method
    if method == 'balanced':
        question_IDs = [(i%4)*5 + (i//4) + 1 for i in range(n)]
    elif method == 'random':
        question_IDs = random.sample(range(1, 21), n)
    else:
        question_IDs = range(1, n+1) 

    return question_IDs


def read_human_data(path_to_csv:str, n=5, selection='first') -> pd.DataFrame:
    """Reads data of max(n, length of csv file) users from given CSV file into DataFrame.
        
    Args:
        path_to_csv (str) : path to a csv file with user data
        n (int) : the number of users to create profiles for
        selection (str) : how to select the n users from the dataset
    
    Returns:
        ([UserProfile]) : a list of n UserProfile objects
    """
    selection_methods = ['random', 'first', 'last']

    if selection not in selection_methods:
        raise ValueError("Invalid selection method. Expected one of: %s" % selection_methods)
    
    if selection == 'first':
        # if we only want the first n rows, we don't need to read the whole file
        df = pd.read_csv(path_to_csv, nrows=n)
        
    elif selection == 'last':
        df = pd.read_csv(path_to_csv)
        df = df.tail(n)
    else: 
        df = pd.read_csv(path_to_csv)
        df = df.sample(n)
    
    df['id'] = df.index
    df = df.rename(columns={"Q_8" : "Q_4"})

    return df