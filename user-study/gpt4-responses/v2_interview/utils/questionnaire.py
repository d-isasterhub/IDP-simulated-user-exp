import random
import pandas as pd

from .profiling import (
    UserProfile
)

from .file_interactions import (
    RESULT_FILES
)

def find_imagepaths(path_to_csv:str, indices:[int]) -> [(int, str)]:
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
    
    n = min(n, 20)

    # select number_questions out of 20 using selected method
    if method == 'balanced':
        question_IDs = [(i%4)*5 + (i//4) + 1 for i in range(n)]
    elif method == 'random':
        question_IDs = random.sample(range(1, 21), n)
    else:
        question_IDs = range(1, n+1) 

    return question_IDs

def get_true_answers(path_to_csv:str) -> dict[int, str]:
    """Reads the correct answers to the specified questions from given file.

    Args:
        path_to_csv (str) : path to csv file with correct answers for each question

    Returns:
        dict[int, str] : dict mapping question indices to correct answer
    """
    questions_df = pd.read_csv(path_to_csv)
    return dict(zip(questions_df['ID'], questions_df['correct_answer']))


def count_correct_LLM_answers(user_id : int, variation=int) -> int:
    """For a specific user, returns the number of questions correctly answered by the LLM.
    Missing answers (NAs) will be counted as wrong answers.
    
    Args:
        user_id (int) : ID of user
    
    Returns:
        (int) : number of correct answers
    
    """
    results_df = pd.read_csv(RESULT_FILES[variation], index_col = "id", keep_default_na=False)
    user_results = results_df.filter(like='LLM_Q', axis=1).iloc[user_id]

    true_answers = get_true_answers("prediction_questions.csv")

    correct_answers = [user_results['LLM_Q' + str(i)] == true_answers[i] for i in range(1, 21)].count(True)

    return correct_answers


def count_correct_human_answers(user: UserProfile) -> int:
    """For a specific user, returns the number of correctly answered questions.
    Missing answers (NAs) will be counted as wrong answers.
    
    Args:
        user (UserProfile) : the user
    
    Returns:
        (int) : number of correct answers

    """
    true_answers = get_true_answers("prediction_questions.csv")

    correct_answers = [user.human_predictions[i] == true_answers[i] for i in range(1, 21)].count(True)

    return correct_answers