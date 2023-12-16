import argparse
import openai
import os
import pandas as pd
import sys
import warnings

from utils.profiling import (
    UserProfile,
    Auklets,
    create_userprofiles
)

from utils.api_messages import (
    get_msg,
    get_msg_with_image
)

from utils.file_interactions import (
    save_result_df,
    read_human_data
)

from utils.questionnaire import (
    select_questions,
    find_imagepaths
)

from utils.prompts import (
    SYSTEM,
    USER_INTRO,
    USER_PROFILING,
    USER_QUESTION
)

# openai.api_key = os.environ["OPENAI_API_KEY"]

def initialize_parser():
    """Sets up an argparse.ArgumentParser object with desired command line options."""

    parser = argparse.ArgumentParser(description="Simulate a user study using LLMs.", formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--number_users', default=50, type=int, 
                                help="number of users to simulate (default: %(default)s)")
    parser.add_argument('--select_users', default='random', type=str, choices=['random', 'first', 'last'], 
                                help="how to select users (default: %(default)s, choices: %(choices)s)")
    parser.add_argument('--profiling', default='full', type=str, choices=['full', 'minimal', 'none'],
                                help="how much profiling info to use (default: %(default)s, choices: %(choices)s)")
    
    subparsers = parser.add_subparsers(dest='subparser_name', help='optionally: specify how to select questionnaire questions. by default, all 20 are used')

    auto_parser = subparsers.add_parser('auto', help='automatic selection of questions. can be given the following args:\n'\
                                        '\t--number_questions\tnumber of questions to select (default: 20)\n'\
                                        '\t--select_questions\thow to select questions (default: \'balanced\', choices: \'random\', \'balanced\', \'first\')')
    auto_parser.add_argument('--number_questions', default=20, type=int,
                                help="number of main questionnaire questions to simulate (default: %(default)s)")
    auto_parser.add_argument('--select_questions', default='balanced', type=str, choices=['random', 'balanced', 'first'],
                                help="how to select the users (default: %(default)s, choices: %(choices)s)")
    
    manual_parser = subparsers.add_parser('manual', help='manual selection of questions. needs following arg:\n'\
                                          '\t--questions\tid(s) of questions to simulate. expects unique values in [1, 20]')
    manual_parser.add_argument('--questions', type=int, nargs='+',
                                help="id(s) of questions to simulate")

    return parser


def single_interview(user : UserProfile, image_path : str, user_num : int, q_num : int, profiling_level : str) -> str:
    """Simulates an interview by profiling a user and asking a user study question. 
        Prompts and response are written to "interview_protocol.txt".

        Args:
            user (UserProfile) : object representing the user that is simulated
            image_path (str) : path to the image corresponding to the question
            user_num (int) : number of user in a series of interviews
            q_num (int) : number of question in a series of interviews
            profiling (str) : level of profiling to give
        
        Returns:
            (str) : simulated response
    """

    # https://platform.openai.com/docs/api-reference/chat/create?lang=python
    QUESTION = USER_INTRO + ("" if profiling_level == 'none' else user.personalize_prompt(USER_PROFILING)) + USER_QUESTION

    # Get gpt-4 response and add the question + answer in the protocol
    with open("out/interview_protocol.txt", mode="a+") as f:
        f.write("Simulated user {u} answering question {i}:\n".format(u=user_num, i=q_num))
        if profiling_level == 'full':
            f.write(user.profiling_prompt)
        f.write("\n")
        f.write(QUESTION)
        f.write("\n")

        response = openai.ChatCompletion.create(
            model = "gpt-4-vision-preview",
            max_tokens = 300,
            messages = 
                (get_msg(role="system", prompt=user.profiling_prompt) if profiling_level == 'full' else []) +\
                get_msg_with_image(role="user", prompt=QUESTION, image=image_path)
        )
        actual_response = response["choices"][0]["message"]["content"] # have a string
        
        f.write(actual_response)
        f.write("\n\n")

    return actual_response


def profile_users(profiles:[UserProfile], profiling_level:str):
    """Personalizes system prompts for users at given profiling level. If profiling level is 'none', system prompt will be None.
    
        Args:
            profiles ([UserProfile]) : the users to profile
            profiling (str) : level of profiling to give
    """
    if profiling_level == 'full':
        for p in profiles:
            p.personalize_prompt(SYSTEM, profiling=True)


def simulate_interviews(question_paths:[(int, str)], profiles:[UserProfile], profiling_level:str):
    """Simulates interview for each user-question combination and saves results to output file.

        Args:
            question_paths ([(int, str)]) : IDs of questions with associated filepaths for images
            profiles ([UserProfile]) : objects representing the users to simulate
            profiling (str) : level of profiling to give
    """
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

        # request gpt-4 responses for not yet (properly) answered questions
        for (index, q_path) in question_paths:
            question = "LLM_Q" + str(index) # TODO: will have to change this probably
            print(results_df.at[user_id, question])
            if results_df.at[user_id, question].lower() not in birds:
                try:
                    results_df.at[user_id, question] = single_interview(user, q_path, user_num, index, profiling_level)
                except:
                    print("Response generation failed")

    # saving the result dataframe again
    save_result_df(results_df)

# openai.api_key = os.environ["OPENAI_API_KEY"]

def main():
    """Sets up and conducts interviews."""

    # parse arguments
    parser = initialize_parser()
    args = parser.parse_args()

    # find questions
    if args.subparser_name is None:
        # if neither manual nor automatic selection of question was chosen, default to all questions
        question_IDs = range(1, 21)
    elif args.subparser_name == 'auto':
        question_IDs = select_questions(args.number_questions, args.select_questions)
    else:
        # question IDs should be unique and between 1 and 20
        question_IDs = set(args.questions)
        valid_IDs = set(range(1, 21))
        if not question_IDs.issubset(valid_IDs):
            warnings.warn("Question IDs outside of valid range [1, 20] will be ignored.")
        question_IDs = list(question_IDs.intersection(valid_IDs))

    question_paths = find_imagepaths("prediction_questions.csv", question_IDs)
    
    # find users
    profiles:[UserProfile] = create_userprofiles(read_human_data("../../data-exploration-cleanup/cleaned_simulatedusers.csv", 
                                                                  n=args.number_users, selection=args.select_users))
    profile_users(profiles, args.profiling)

    simulate_interviews(question_paths, profiles, args.profiling)


if __name__ == '__main__':
    sys.exit(main())