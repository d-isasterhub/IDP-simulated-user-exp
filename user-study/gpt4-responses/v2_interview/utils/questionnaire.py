import random
import pandas as pd


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