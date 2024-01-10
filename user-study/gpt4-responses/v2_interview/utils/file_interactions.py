# Imports
import pandas as pd
import random

# ------------------------------------------------ FILE NAMES AND PATHS ----------------------------------------

BIRD_PREFIXES = {
    1 : "out/v1_profile_no_reason/",
    2 : "out/v2_no_profile_no_reason/",
    3 : "out/v3_profile_reason/",
    4 : "out/v4_no_profile_reason/",
    5 : "out/v5_profile_heatmap/",
    6 : "out/v6_no_profile_heatmap/"
}

AGREEMENT_PREFIXES = {
    # boolean: with accuracy
    True : "out/agreement/with_accuracy_",
    False : "out/agreement/without_accuracy_"
}

FILE_SUFFIXES = {
    "protocol" : "protocol.txt",
    "results" : "results.csv"
}

def bird_output_path(variation: int, out_type:str="protocol") -> str:
    """Returns path to output file.
    
    Args:
        variation (int) : prompt variation
        type (str) : protocol file vs result file
    
    Returns:
        (str) : file path
    """
    output_types = ["protocol", "results"] 
    if type not in output_types: 
        raise ValueError("Invalid output file type. Expected one of: %s" % output_types)

    return BIRD_PREFIXES[variation] + FILE_SUFFIXES[out_type]


def agree_output_path(with_accuracy: bool, out_type:str="protocol") -> str:
    """Returns path to output file.
    
    Args:
        with_accuracy (bool) : whether accuracy was used in prompt
        type (str) : protocol file vs result file
    
    Returns:
        (str) : file path
    """
    output_types = ["protocol", "results"] 
    if type not in output_types: 
        raise ValueError("Invalid output file type. Expected one of: %s" % output_types)

    return AGREEMENT_PREFIXES[with_accuracy] + FILE_SUFFIXES[out_type]


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