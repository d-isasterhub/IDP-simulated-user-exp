import openai
import os
import pandas as pd
import random
import os

from v2_profiling import (
    UserProfile,
    Auklets
)

from v2_interview_util import (
    get_msg,
    get_msg_with_image,
    save_result_df
)

from v2_interview_util_prompts import (
    SYSTEM,
    USER
)

# openai.api_key = os.environ["OPENAI_API_KEY"]

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
    
def create_userprofiles(data : pd.DataFrame) -> [UserProfile]:
    """Constructs UserProfiles based on dataframe
    
    Args:
        data (pd.DataFrame) : dataframe with human data
        
    Returns:
        ([UserProfile]) : a list of UserProfile objects
    """
    return (data.apply(lambda x: UserProfile(x), axis = 1)).to_list()


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

    # Get gpt-4 response and add the question + answer in the protocol
    with open("out/interview_protocol.txt", mode="a+") as f:
        f.write("Simulated user {u} answering question {i}:\n".format(u=user_num, i=q_num))
        f.write(user.profiling_prompt)
        f.write("\n")
        f.write(QUESTION)
        f.write("\n")

        response = openai.ChatCompletion.create(
            model = "gpt-4-vision-preview",
            max_tokens = 300,
            messages = 
                get_msg(role="system", prompt=user.profiling_prompt) +\
                get_msg_with_image(role="user", prompt=QUESTION, image=image_path)
        )
        actual_response = response["choices"][0]["message"]["content"] # have a string
        
        f.write(actual_response)
        f.write("\n\n")

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
    results_df = pd.read_csv("out/simulated_interview_results.csv", index_col = "id", keep_default_na=False)

    birds = [bird.value.lower() for bird in Auklets]

    for user_num, user in enumerate(profiles):

        user_id = user.user_background['id']

        # if the user does not already have a row in the results data frame, create a new one
        if user_id not in list(results_df.index):
            print(user_id)
            results_df.loc[user_id] = 'NA'

        # request gpt-4 responses for not yet (properly) answered questions
        for (index, q_path) in question_paths:
            question = "LLM_Q" + str(index) # TODO: will have to change this probably
            print(results_df.at[user_id, question])
            if results_df.at[user_id, question].lower() not in birds:
                user.personalize_prompt(SYSTEM, profiling=True)
                try:
                    results_df.at[user_id, question] = single_interview(user, q_path, user_num, index)
                except:
                    print("Response generation failed")

    # saving the result dataframe again
    save_result_df(results_df)

    # with open("out/simulated_interview_results.csv", mode="a") as f_results:

    #     for user_num, user in enumerate(profiles): 
        
    #         for (index, q_path) in question_paths:
    #             user.personalize_prompt(SYSTEM, profiling=True) 
    #             llm_response = single_interview(user, q_path, user_num, index)
    #             user.llm_predictions[index] = llm_response

    #         f_results.write("\n")
    #         f_results.write(user.to_csv_string())

    
    

# openai.api_key = os.environ["OPENAI_API_KEY"]
simulate_interviews(number_users=50, number_questions=20, user_select='random')