# Imports
import pandas as pd
import random

# ------------------------------------------------ FILE NAMES ----------------------------------------

RESULT_FILES = {
    1 : "out/simulated_interview_results_1.csv",
    2 : "out/simulated_interview_results_2.csv",
    3 : "out/simulated_interview_results_3.csv",
    4 : "out/simulated_interview_results_4.csv"
}

PROTOCOL_FILES = {
    1 : "out/interview_protocol_1.txt",
    2 : "out/interview_protocol_2.txt",
    3 : "out/interview_protocol_3.txt",
    4 : "out/interview_protocol_4.txt"
}

# ----------------------------------------------- During interview ---------------------------------------------------------------

def check_answer_exists():
    pass


def save_result_df(df:pd.DataFrame, variation:int):
    df.sort_values(by=['id'], inplace=True)
    df.reset_index()
    df.to_csv(RESULT_FILES[variation], na_rep='NA')
    

# ------------------------------------------------ Before Interview ---------------------------------------------------------------


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

def get_heatmap_descriptions() -> dict[int, str]:
    """Reads all available heatmap descriptions from csv files.
    
    Returns:
        ([dict[int, str]]) : a dict containing all heatmap descriptions, keys are question numbers
    """
    heatmaps_df = pd.read_csv("heatmap_descriptions.csv")
    return heatmaps_df.to_dict('records')