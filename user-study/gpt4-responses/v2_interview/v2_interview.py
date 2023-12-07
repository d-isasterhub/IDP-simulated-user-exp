import openai
import os
import pandas as pd

from v2_profiling import (
    UserProfile,
    Auklets,
    create_userprofiles
)

from v2_interview_util import (
    get_msg,
    get_msg_with_image,
    save_result_df,
    select_questions,
    read_questions,
    read_human_data
)

from v2_interview_util_prompts import (
    SYSTEM,
    USER
)

# openai.api_key = os.environ["OPENAI_API_KEY"]


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

    # find questions
    question_IDs = select_questions(number_questions, question_select)
    question_paths = read_questions("prediction_questions.csv", question_IDs)
    
    # find users
    profiles: [UserProfile] = create_userprofiles(read_human_data("../../data-exploration-cleanup/cleaned_simulatedusers.csv", n=number_users, selection=user_select))
    
    # find (previous) results    
    results_df = pd.read_csv("out/simulated_interview_results.csv", index_col = "id", keep_default_na=False)

    birds = [bird.value.lower() for bird in Auklets]

    # simulate interview for each user and question
    for user_num, user in enumerate(profiles):

        user_id = user.user_background['id']

        # if the user does not already have a row in the results data frame, create a new one
        if user_id not in list(results_df.index):
            print(user_id)
            results_df.loc[user_id] = 'NA'

        # profiling prompt only needs to be created once per UserProfile object
        if user.profiling_prompt is None:
            user.personalize_prompt(SYSTEM, profiling=True)

        # request gpt-4 responses for not yet (properly) answered questions
        for (index, q_path) in question_paths:
            question = "LLM_Q" + str(index) # TODO: will have to change this probably
            print(results_df.at[user_id, question])
            if results_df.at[user_id, question].lower() not in birds:
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