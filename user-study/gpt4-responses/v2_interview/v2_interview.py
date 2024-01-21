import argparse
import openai
import os
import pandas as pd
import sys
import warnings

from utils.profiling import (
    UserProfile,
    Auklets,
    create_userprofiles,
    DEFAULT_DATA
)

from utils.api_messages import (
    get_msg,
    get_msg_with_image
)

from utils.file_interactions import (
    save_result_df,
    read_human_data,
    get_heatmap_descriptions,
    bird_output_path,
    agree_output_path
)

from utils.questionnaire import (
    select_questions,
    find_imagepaths,
    count_correct_LLM_answers,
    count_correct_human_answers,
    average_agreement_score
)

from utils.prompts import (
    SYSTEM,
    USER_PROMPTS,
    TOKENS_LOW,
    AGREEMENT_PROMPTS,
    AGREEMENT_QUESTIONS,
    EXAMPLE_IMAGE_PATH,
    ReasoningOption
)

from utils.answer_processing import (
    process_llm_output
)

from utils.api_interactions import (
    generate_heatmap_descriptions
)

# openai.api_key = os.environ["OPENAI_API_KEY"]

def initialize_parser():
    """Sets up an argparse.ArgumentParser object with desired command line options."""

    parser = argparse.ArgumentParser(description="Simulate a user study using LLMs.", formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--number_users', default=50, type=int, 
                                help="number of users to simulate (default: %(default)s)")
    parser.add_argument('--select_users', default='random', type=str, choices=['random', 'first', 'last'], 
                                help="how to select users (default: %(default)s, choices: %(choices)s)")
    #parser.add_argument('--profiling', default='full', type=str, choices=['full', 'minimal', 'none'],
    #                            help="how much profiling info to use (default: %(default)s, choices: %(choices)s)")
    parser.add_argument('--profiling', default=True, type=bool, 
                                help="whether to include profiling infor or not (default: True)")
    parser.add_argument('--reasoning', default='none', type=str, choices=['none', 'heatmap_first', 'profile_first', 'chain_of_thought'],
                                help="whether and how to ask LLM for reasoning (default: %(default)s, choices: %(choices)s)")
    
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

    agreement_parser = subparsers.add_parser('agreement', help='simulate agreement questions instead of XAI predictions.')
    agreement_parser.add_argument('--questions', default=[1,2,3,4,5,6], type=int, nargs='+',# choices=range(1, 7), 
                                help="questions to simulate")
    agreement_parser.add_argument('--example', default=1, type=int, choices=range(1, 7), 
                                help="which question to show the LLM as example, default: %(default)")
    
    example_parser = agreement_parser.add_mutually_exclusive_group(required=False)
    example_parser.add_argument('--with_example', dest='with_example', action='store_true')
    example_parser.add_argument('--without_example', dest='with_example', action='store_false')
    agreement_parser.set_defaults(with_example=True)
    
    accuracy_parser = agreement_parser.add_mutually_exclusive_group(required=False)
    accuracy_parser.add_argument('--with_accuracy', dest='with_accuracy', action='store_true')
    accuracy_parser.add_argument('--without_accuracy', dest='with_accuracy', action='store_false')
    agreement_parser.set_defaults(with_accuracy=True)

    average_parser = agreement_parser.add_mutually_exclusive_group(required=False)
    average_parser.add_argument('--with_average', dest='with_average', action='store_true')
    average_parser.add_argument('--without_average', dest='with_average', action='store_false')
    agreement_parser.set_defaults(with_average=False)

    average_parser = agreement_parser.add_mutually_exclusive_group(required=False)
    average_parser.add_argument('--fixed_average', dest='fixed_average', action='store_true')
    average_parser.add_argument('--user_average', dest='fixed_average', action='store_false')
    agreement_parser.set_defaults(fixed_average=False)
    
    return parser


def LLM_prediction_chain_of_thought(user:UserProfile, image_path_example: str, image_path_question: str, profiling: bool, question_example: str, question: str, answer_example: str) -> str:
    """Main part of the interview simulation, chain of thought: profiles a user, give example question and answer, and then asks a user study question.
    
        Args:
            user (UserProfile) : object representing the user that is simulated
            image_path_example (str) : path to the image used for the example question
            image_path_question (str) : path to the image used for the actual user study question 
            profiling (bool) : whether to use profiling
            example (str) : example question prompt with with predefined profiling info (bird descriptions)
            question (str) : adapted question prompt with necessary profiling info
        
        Returns:
            (str) : simulated question answer
    """
    print(user.profiling_prompt if profiling else "no profiling")
    print(question_example)
    print(image_path_example)
    print(answer_example)
    print(question)
    print(image_path_question)
    response = openai.ChatCompletion.create(
            model = "gpt-4-vision-preview",
            max_tokens = 400,
            messages = 
                (get_msg(role="system", prompt=user.profiling_prompt) if profiling else []) +\
                get_msg_with_image(role="user", prompt=question_example, image=image_path_example) +\
                get_msg(role="assistant", prompt=answer_example) +\
                get_msg_with_image(role="user", prompt=question, image=image_path_question)
        )
    actual_response = response["choices"][0]["message"]["content"] # have a string
    return actual_response


def LLM_prediction_heatmap_first(user:UserProfile, image_path: str, profiling: bool, heatmap_description: str, question: str) -> str:
    """Main part of the interview simulation, heatmap first: gives LLM a pre-generated heatmap description, then profiles a user and finally asks a user study question.
    
        Args:
            user (UserProfile) : object representing the user that is simulated
            image_path (str) : path to the image corresponding to the question
            profiling (bool) : whether to use profiling
            heatmap_description (str) : heatmap description associated with the question
            question (str) : adapted question prompt with necessary profiling info
        
        Returns:
            (str) : simulated question answer
    """
    response = openai.ChatCompletion.create(
            model = "gpt-4-vision-preview",
            max_tokens = 400,
            messages = 
                (get_msg(role="system", prompt=user.profiling_prompt) if profiling else []) +\
                get_msg_with_image(role="user", prompt=USER_PROMPTS[(ReasoningOption.HEATMAP_FIRST, "intro")]+USER_PROMPTS[(ReasoningOption.HEATMAP_FIRST, "heatmap")], image=image_path) +\
                get_msg(role="assistant", prompt=heatmap_description) +\
                get_msg(role="user", prompt=question) 
        )

    actual_response = response["choices"][0]["message"]["content"] # have a string
    return actual_response


def LLM_prediction_profile_first(user: UserProfile, image_path: str, profiling: bool, question: str) -> str:
    """Main part of the interview simulation, variants 1/2/3: profiles a user and then asks a user study question.
    
        Args:
            user (UserProfile) : object representing the user that is simulated
            image_path (str) : path to the image corresponding to the question
            profiling (bool) : whether to use profiling
            question (str) : adapted question prompt with necessary profiling info
        
        Returns:
            (str) : simulated question answer
    """
    response = openai.ChatCompletion.create(
            model = "gpt-4-vision-preview",
            max_tokens = 400,
            messages = 
                (get_msg(role="system", prompt=user.profiling_prompt) if profiling else []) +\
                get_msg_with_image(role="user", prompt=question, image=image_path)
        )
    actual_response = response["choices"][0]["message"]["content"] # have a string
    return actual_response


def LLM_agreement(user: UserProfile, profiling: bool, introprofile_prompt: str, question_prompt: str, with_example: bool, example_prompt: str, example_a: int) -> str:
    """Main part of the interview simulation: profiles a user, gives an agreement question as an example and finally asks an agreement question.
    
        Args:
            user (UserProfile) : object representing the user that is simulated
            profiling (bool) : whether to include profiling info
            introprofile_prompt (str) : prompt introducing context and task
            question_prompt (str) : prompt with actual question
            with_example (bool) : whether to include example question
            example_prompt (str) : prompt with example question
            example_a (int) : answer to example question
        
        Returns:
            (str) : simulated question answer
    """
    response = openai.ChatCompletion.create(
            model = "gpt-4-vision-preview",
            max_tokens = 400,
            messages = 
                (get_msg(role="system", prompt=user.profiling_prompt) if profiling else []) +\
                get_msg(role="user", prompt=introprofile_prompt) +\
                (get_msg(role="user", prompt=example_prompt) if with_example else []) +\
                (get_msg(role="assistant", prompt=str(example_a)) if with_example else []) +\
                get_msg(role="user", prompt=question_prompt) 
        )

    actual_response = response["choices"][0]["message"]["content"] # have a string
    return actual_response


def single_agreement(user : UserProfile, actual_q: int, with_example: bool, example_q: int, example_a: int, profiling : bool, with_accuracy: bool, number_correct: int, with_average: bool, fixed_average:bool, average_score: int) -> str:
    """Simulates an interview by profiling a user and asking an agreement study question. 
        Prompts and full response including reasoning are written to "interview_protocol.txt".

        Args:
            user (UserProfile) : object representing the user that is simulated
            actual_q (int) : number of agreement question to ask
            with_example (bool) : whether to show a question as example
            example_q (int) : number of agreement question to show as example
            example_a (int) : human answer to example question
            profiling (bool) : whether to use profiling
            with_accuracy (bool) : whether to include the number of correctly answered questions by human
            number_correct (int) : number of correctly answered questions by human
            with_average (bool) : whether to include the average agreement score of human
            average_score (int) : average agreement score of human
        
        Returns:
            (str) : simulated and cleaned question answer
    """
    INTRO_PROFILE = AGREEMENT_PROMPTS["intro"] + \
        AGREEMENT_PROMPTS["previous"] +\
        ("" if not profiling else user.personalize_prompt(AGREEMENT_PROMPTS["profiling"])) +\
        ("" if not with_accuracy else ("Out of 20 images you were confronted with, you guessed the classification correctly for "+str(number_correct)+" of them. ")) +\
        ("" if not with_average else ("You would rate your overall understanding of the model explanations and the study questions in general a " + \
                                      str(average_score) + " on a scale from 1 to 7, where 1 represents the lowest and 7 represents the highest level of understanding."))+\
        AGREEMENT_PROMPTS["task"]
    
    EXAMPLE = AGREEMENT_PROMPTS["question"] +\
        AGREEMENT_QUESTIONS[example_q] +\
        AGREEMENT_PROMPTS["scale"] + AGREEMENT_PROMPTS["answer"]

    QUESTION = AGREEMENT_PROMPTS["question"] +\
        AGREEMENT_QUESTIONS[actual_q] +\
        AGREEMENT_PROMPTS["scale"] + AGREEMENT_PROMPTS["answer"]

    with open(agree_output_path(with_accuracy, with_average, fixed_average, with_example, "protocol"), mode="a+") as f:
        f.write("Simulated user {u} answering agreement question {i}:\n".format(u=user.user_background['id'], i=actual_q))
        if profiling:
            f.write(user.profiling_prompt)
        f.write(INTRO_PROFILE)
        f.write("\n")
        if with_example:
            f.write(EXAMPLE)
            f.write("\n")
            f.write(str(example_a))
        f.write("\n")
        f.write(QUESTION)
        f.write("\n")

        llm_response = LLM_agreement(user, profiling, INTRO_PROFILE, QUESTION, with_example, EXAMPLE, example_a)
        
        answer = llm_response # no processing here (yet)
        
        f.write("Answer:\n")
        f.write(answer)
        f.write("\n\n")

    return answer


def single_prediction(user : UserProfile, image_path : str, q_num : int, profiling : bool, reasoning : ReasoningOption, heatmap_description:str=None, image_path_example:str="") -> str:
    """Simulates an interview by first profiling a user and then asking a user study question. 
        Prompts and full response including reasoning are written to "interview_protocol.txt".

        Args:
            user (UserProfile) : object representing the user that is simulated
            image_path (str) : path to the image corresponding to the question
            user_num (int) : number of user in a series of interviews
            q_num (int) : number of question in a series of interviews
            profiling (bool) : whether to use profiling
            reasoning (ReasoningOption) : variation of prompts to use
            heatmap_description (str) : optional heatmap description for question
        
        Returns:
            (str) : simulated and cleaned question answer
    """

    # https://platform.openai.com/docs/api-reference/chat/create?lang=python

    if reasoning == ReasoningOption.HEATMAP_FIRST:
        QUESTION = ("" if not profiling else user.personalize_prompt(USER_PROMPTS[(reasoning, "profiling")])) + USER_PROMPTS[(reasoning, "question")] + " " + TOKENS_LOW
    elif reasoning == ReasoningOption.CHAIN_OF_THOUGHT:
        EXAMPLE_QUESTION = USER_PROMPTS[(reasoning, "example_profiling")] + USER_PROMPTS[(reasoning, "question")]
        QUESTION = ("" if not profiling else user.personalize_prompt(USER_PROMPTS[(reasoning, "profiling")])) + USER_PROMPTS[(reasoning, "question")]
        EXAMPLE_ANSWER = USER_PROMPTS[(reasoning, "example_answer")]
    else:
        QUESTION = USER_PROMPTS[(reasoning, "intro")] + ("" if not profiling else user.personalize_prompt(USER_PROMPTS[(reasoning, "profiling")])) + USER_PROMPTS[(reasoning, "question")]
    print(QUESTION)

    # Get gpt-4 response and add the question + answer in the protocol
    with open(bird_output_path(reasoning, profiling, "protocol"), mode="a+") as f:
        f.write("Simulated user {u} answering question {i}:\n".format(u=user.user_background['id'], i=q_num))
        if profiling == True:
            f.write(user.profiling_prompt)
        if reasoning == ReasoningOption.HEATMAP_FIRST:
            f.write(USER_PROMPTS[(reasoning, "intro")])
            f.write(USER_PROMPTS[(reasoning, "heatmap")])
            f.write("\n")
            print(str(heatmap_description))
            f.write(heatmap_description)
            f.write("\n")
        if reasoning == ReasoningOption.CHAIN_OF_THOUGHT:
            f.write("Example profiling:\n")
            f.write(EXAMPLE_QUESTION)
            f.write("\n")
            f.write("Example answer:\n")
            f.write(EXAMPLE_ANSWER)
            f.write("\n")
        f.write("\n")
        f.write(QUESTION)
        f.write("\n")

        if reasoning == ReasoningOption.HEATMAP_FIRST:
            llm_response = LLM_prediction_heatmap_first(user, image_path, profiling, heatmap_description, QUESTION)
        elif reasoning == ReasoningOption.CHAIN_OF_THOUGHT:
            llm_response = LLM_prediction_chain_of_thought(user, image_path_example, image_path, profiling, EXAMPLE_QUESTION, QUESTION, EXAMPLE_ANSWER) 
        else:
            llm_response = LLM_prediction_profile_first(user, image_path, profiling, QUESTION)
            
        
        reasoning, answer = process_llm_output(llm_response)
        
        f.write("Reasoning:\n")
        f.write(reasoning)
        f.write("Answer:\n")
        f.write(answer)
        f.write("\n\n")

    return answer


def profile_users(profiles:[UserProfile], profiling:bool):
    """Personalizes system prompts for users at given profiling level. If profiling level is 'none', system prompt will be None.
    
        Args:
            profiles ([UserProfile]) : the users to profile
            profiling (str) : level of profiling to give
    """
    if profiling:
        for p in profiles:
            p.personalize_prompt(SYSTEM, profiling=True)


def simulate_agreements(questions:[int], profiles:[UserProfile], profiling:bool, with_accuracy: bool, with_example: bool, example_q: int, with_average: bool, fixed_average: bool):
    """Simulates interview for each user-question combination and saves results to output file.

        Args:
            question_paths ([(int, str)]) : IDs of questions with associated filepaths for images
            profiles ([UserProfile]) : objects representing the users to simulate
            profiling (bool) : whether to use profiling
            with_accuracy (bool) : whether to include the number of correctly answered questions by human
            with_example (bool) : whether to show a question as example
            example_q (int) : number of agreement question to show as example
            with_average (bool) : whether to include the average agreement score of human
    """
    # find (previous) results    
    out_path = agree_output_path(with_accuracy, with_average, fixed_average, with_example, "results")
    results_df = pd.read_csv(out_path, index_col = "id", keep_default_na=False)
    
    options = range(1, 8)

    # simulate interview for each user and question
    for user in profiles:

        user_id = user.user_background['id']
        number_correct = count_correct_human_answers(user)
        average_score = average_agreement_score(user)
        if fixed_average:
            average_score = 4

        # if the user does not already have a row in the results data frame, create a new one
        if user_id not in list(results_df.index):
            print(user_id)
            results_df.loc[user_id] = 'NA'

        # request gpt-4 responses for not yet (properly) answered questions
        for q in questions:
            example_a = user.human_agreements[q]
            question = "LLM_A" + str(q) # TODO: will have to change this probably
            print(results_df.at[user_id, question])
            if results_df.at[user_id, question] not in options:
                try:
                    results_df.at[user_id, question] = single_agreement(user, q, with_example, example_q, example_a, profiling, with_accuracy, number_correct, with_average, fixed_average, average_score)
                except Exception as e:
                    # TODO: this does not work
                    print("Response generation failed:\n")
                    print(e)

        save_result_df(results_df, out_path)

    # saving the result dataframe again
    save_result_df(results_df, agree_output_path(with_accuracy, with_average, fixed_average, with_example, "results"))


def simulate_interviews(question_paths:[(int, str)], profiles:[UserProfile], profiling:bool, reasoning:ReasoningOption, heatmap_descriptions:dict[int, str]=None):
    """Simulates interview for each user-question combination and saves results to output file.

        Args:
            question_paths ([(int, str)]) : IDs of questions with associated filepaths for images
            profiles ([UserProfile]) : objects representing the users to simulate
            profiling (bool) : whether to use profiling
            reasoning (ReasoningOption) : prompting variant, i.e. whether to ask for reasoning and if so, whether to ask for heatmap descriptions first
            heatmap_descriptions (dict[int, str]) : pre-generated descriptions of the heatmaps
    """
    # find (previous) results
    out_path = bird_output_path(reasoning, profiling, "results")    
    results_df = pd.read_csv(out_path, index_col = "id", keep_default_na=False)
    #results_df['LLM_Q2'] = 'NA'

    birds = [bird.value.lower() for bird in Auklets]

    # simulate interview for each user and question
    for user in profiles:

        user_id = user.user_background['id']

        # if the user does not already have a row in the results data frame, create a new one
        if user_id not in list(results_df.index):
            print(user_id)
            results_df.loc[user_id] = 'NA'

        # request gpt-4 responses for not yet (properly) answered questions
        for (q_index, q_path) in question_paths:
            question = "LLM_Q" + str(q_index) # TODO: will have to change this probably
            print(results_df.at[user_id, question])
            if results_df.at[user_id, question].lower() not in birds:
                try:
                    if reasoning==ReasoningOption.HEATMAP_FIRST:
                        results_df.at[user_id, question] = single_prediction(user, q_path, q_index, profiling, reasoning, heatmap_descriptions[q_index-1]['heatmap_description'])
                    elif reasoning==ReasoningOption.CHAIN_OF_THOUGHT:
                        results_df.at[user_id, question] = single_prediction(user, q_path, q_index, profiling, reasoning, image_path_example=EXAMPLE_IMAGE_PATH)
                    else:
                        results_df.at[user_id, question] = single_prediction(user, q_path, q_index, profiling, reasoning)
                except Exception as e:
                    # TODO: this does not work
                    print("Response generation failed:\n")
                    print(e)

        save_result_df(results_df, out_path)

    # saving the result dataframe again
    save_result_df(results_df, out_path)

# openai.api_key = os.environ["OPENAI_API_KEY"]

def main():
    """Sets up and conducts interviews."""

    # ------------------------------------- parse arguments --------------------------------------------

    parser = initialize_parser()
    args = parser.parse_args()
    
    # ----------------------------------------- profiling -----------------------------------------------

    if not args.profiling:
        profiles:[UserProfile] = [UserProfile(DEFAULT_DATA)]
    else:
        # find users
        profiles:[UserProfile] = create_userprofiles(read_human_data("../../data-exploration-cleanup/cleaned_simulatedusers.csv", 
                                                                  n=args.number_users, selection=args.select_users))
        profile_users(profiles, args.profiling)

    # --------------------------------- predictions or agreements ---------------------------------------
        
    prediction = (args.subparser_name is None) or (args.subparser_name in ['auto', 'manual']) 

    if prediction:

        # find questions
        if args.subparser_name is None:
            # if neither manual nor automatic selection of question was chosen, default to all questions
            question_IDs = range(1, 21)
        elif args.subparser_name == 'auto':
            question_IDs = select_questions(args.number_questions, args.select_questions)
        elif args.subparser_name == 'manual':
            # question IDs should be unique and between 1 and 20
            question_IDs = set(args.questions)
            valid_IDs = set(range(1, 21))
            if not question_IDs.issubset(valid_IDs):
                warnings.warn("Question IDs outside of valid range [1, 20] will be ignored.")
            question_IDs = list(question_IDs.intersection(valid_IDs))
        print(os.getcwd())
        question_paths = find_imagepaths("prediction_questions.csv", question_IDs)

        reasoning = ReasoningOption[args.reasoning.upper()]

        if reasoning != ReasoningOption.HEATMAP_FIRST:
            simulate_interviews(question_paths, profiles, args.profiling, reasoning)
        else:
            generate_heatmap_descriptions(question_IDs)
            heatmap_descriptions = get_heatmap_descriptions()
            simulate_interviews(question_paths, profiles, args.profiling, reasoning, heatmap_descriptions)

    else:
        agreement_questions = set(args.questions).difference(set([args.example])) if args.with_example else args.questions
        simulate_agreements(agreement_questions, profiles, args.profiling, args.with_accuracy, args.with_example, args.example, args.with_average, args.fixed_average)


if __name__ == '__main__':
    sys.exit(main())