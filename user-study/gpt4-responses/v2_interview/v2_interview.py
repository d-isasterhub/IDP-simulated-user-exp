import openai
import pandas as pd
import random

from v2_profiling import (
    UserProfile,
    Auklets
)

from v2_interview_util import (
    get_msg,
    get_msg_with_image
)

from v2_interview_util_prompts import (
    SYSTEM,
    USER
)

def create_user_profiles(path_to_csv, n=5, selection='first') -> [UserProfile]:
    """Constructs n UserProfiles based on user data given in a .csv file
        
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
    
    safe_n = n

    if selection == 'first':
        # if we only want the first n rows, we don't need to read the whole file
        df = pd.read_csv(path_to_csv, nrows=n)
        
    elif selection == 'last':
        df = pd.read_csv(path_to_csv)
        df = df.tail(n)
        if df.size < n:
            safe_n = df.size
    else: 
        df = pd.read_csv(path_to_csv)
        df = df.sample(n)
        if df.size < n:
            safe_n = df.size
    
    df = df.rename(columns={"Q_8" : "Q_4"})

    userprofiles = []

    for i in range(safe_n):
        userprofiles.append(UserProfile(df.iloc[i].squeeze()))

    return userprofiles   


def single_interview(user : UserProfile, image_path : str, user_num : int, q_num : int) -> str:
    """
        Simulates an interview by profiling a user and asking a user study question. 
        Prompts and response are written to "interview_protocol.txt".

        Args:
            user (UserProfile) : object representing the user that is simulated
            image_path (str) : path to the image corresponding to the question
            user_num (int) : number of user in a series of interviews
            q_num (int) : number of question in a series of interviews
        
        Returns:
            (str) : simulated response
    """

    # https://platform.openai.com/docs/api-reference/chat/create?lang=python
    QUESTION = user.personalize_prompt(USER)
    
    f = open("out/interview_protocol.txt", mode="a+")
    f.write("Simulated user {u} answering question {i}:\n".format(u=user_num, i=q_num))
    f.write(user.profiling_prompt)
    f.write(QUESTION)

    #response = openai.ChatCompletion.create(
    #    model = "gpt-4-vision-preview",
    #    max_tokens = 300,
    #    messages = 
    #        get_msg(role="system", prompt=user.profiling_prompt) +\
    #        get_msg_with_image(role="user", prompt=QUESTION, image=image_path)
    #)
    #actual_response = response["choices"][0]["message"]["content"] # have a string
    actual_response = "dummy_response"
    f.write(actual_response)
    f.write("\n\n")
    f.close()
    return actual_response


def simulate_interviews(number_users=1, number_questions=1, user_select='first', question_select='balanced'):
    """
        Simulates multiple interviews by generating multiple user profiles from dataset,
        selecting multiple questions and conducting an interview for each user-question combination.
    """

    selection_methods = ['random', 'balanced']

    if question_select not in selection_methods:
        raise ValueError("Invalid selection method. Expected one of: %s" % selection_methods)

    # select number_questions out of 20 using selected method
    if question_select == 'balanced':
        question_IDs = [(i%4)*5 + (i//4) for i in range(number_questions)]
    elif question_select == 'random':
        question_IDs = random.sample(range(1, 21), number_questions)
    else:
        question_IDs = range(1, number_questions+1) 

    # read question data, find image paths
    questions_df = pd.read_csv("prediction_questions.csv")
    question_paths = [(i+1, questions_df.at[i, "image_path"]) for i in question_IDs]
    
    # create user profiles from dataset
    profiles: [UserProfile] = create_user_profiles("../../data-exploration-cleanup/cleaned_simulatedusers.csv", n=number_users, selection=user_select)
    
    # simulate interview for each user and question
    f_results = open("out/simulated_interview_results.csv", mode="a")
    
    for user_num, user in enumerate(profiles):
        
        for (index, q_path) in question_paths:
            user.personalize_prompt(SYSTEM, profiling=True)
            llm_response = single_interview(user, q_path, user_num, index)
            user.llm_predictions[index] = llm_response

        f_results.write("\n")
        f_results.write(user.to_csv_string())
    
    f_results.close()

simulate_interviews()

 