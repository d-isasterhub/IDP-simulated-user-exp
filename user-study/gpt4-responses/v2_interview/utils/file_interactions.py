# Imports
import pandas as pd
import random

from .prompts import (
    ReasoningOption
)

# ------------------------------------------------ FILE NAMES AND PATHS ----------------------------------------

REASON_OPTIONS = {
    ReasoningOption.NONE : "out/no_reason/",
    ReasoningOption.HEATMAP_FIRST : "out/reason_heatmap_first/",
    ReasoningOption.PROFILE_FIRST : "out/reason_profile_first/",
    ReasoningOption.CHAIN_OF_THOUGHT : "out/reason_chain_of_thought/",
}

ACCURACY_PREFIXES = {
    # boolean: with accuracy
    True : "with_accuracy/",
    False : "without_accuracy/"
}

AVERAGE_PREFIXES = {
    True : "with_average/",
    False: "without_average/"
}

EXAMPLE_PREFIXES = {
    True: "with_example/",
    False: "without_example/"
}


FILE_SUFFIXES = {
    "protocol" : "protocol.txt",
    "results" : "results.csv"
}

def bird_output_path(reasoning:ReasoningOption, profiling:bool, out_type:str="protocol") -> str:
    """Returns path to output file.
    
    Args:
        reasoning (ReasoningOption) : prompt variation
        type (str) : protocol file vs result file
    
    Returns:
        (str) : file path
    """
    output_types = ["protocol", "results"] 
    if out_type not in output_types: 
        raise ValueError("Invalid output file type. Expected one of: %s" % output_types)
    
    return REASON_OPTIONS[reasoning] + ("profile/" if profiling else "no_profile/") + FILE_SUFFIXES[out_type] 


def agree_output_path(with_accuracy: bool, with_average: bool, with_example: bool, out_type:str="protocol") -> str:
    """Returns path to output file.
    
    Args:
        with_accuracy (bool) : whether accuracy was used in prompt
        type (str) : protocol file vs result file
    
    Returns:
        (str) : file path
    """
    output_types = ["protocol", "results"] 
    if out_type not in output_types: 
        raise ValueError("Invalid output file type. Expected one of: %s" % output_types)

    return "out/agreement/" + ACCURACY_PREFIXES[with_accuracy] + EXAMPLE_PREFIXES[with_example] + AVERAGE_PREFIXES[with_average] + FILE_SUFFIXES[out_type]


# ----------------------------------------------- During interview ---------------------------------------------------------------

def check_answer_exists():
    pass


def save_result_df(df:pd.DataFrame, result_path: str):
    df.sort_values(by=['id'], inplace=True)
    df.reset_index()
    df.to_csv(result_path, na_rep='NA')
    

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
    
    #df = pd.read_csv(path_to_csv)
    #df = df.iloc[[44]]
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