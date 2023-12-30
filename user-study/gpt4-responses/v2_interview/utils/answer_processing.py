import re
import warnings
from .profiling import Auklets

QUESTIONNAIRES = ['birds']

QUESTIONNAIRES_TO_ENUMS = {
    'birds' : Auklets
}

def validate_answer(answer:str, questionnaire:str='birds') -> str:
    """Checks if answer is one of the valid options expected in a questionnaire.
    
        Args:
            answer (str) : clean (alphanumeric) answer string
            questionnaire (str) : specifies questionnaire/answer options to validate against
            
        Returns:
            (str) : answer string with right capitalization (if answer is valid) or empty string"""
    
    if questionnaire not in QUESTIONNAIRES:
        raise ValueError("Invalid questionnaire option. Expected one of: %s" % QUESTIONNAIRES)
    
    answer_enum = QUESTIONNAIRES_TO_ENUMS.get(questionnaire)
    valid_answer = next((option.value for option in answer_enum if option.value.lower() == answer.lower()), "")
    
    return valid_answer


def clean_answer(raw:str) -> str:
    """Removes non-alphanumeric characters from answer string

        Args:
            raw (str) : answer string with potentially additional non-alphanumeric chars

        Returns:
            (str) : the cleaned answer
    
    """
    clean = re.sub('[\W_]+', ' ', raw)
    clean = clean.strip()
    return clean
    

def extract_answer(answer:str, questionnaire:str='birds') -> str:
    """Extracts answer option from a full sentence. Returns empty string if not exactly one valid answer is found.

        Args:
            raw (str) : full answer string

        Returns:
            (str) : valid answer
    
    """
    if questionnaire not in QUESTIONNAIRES:
        raise ValueError("Invalid questionnaire option. Expected one of: %s" % QUESTIONNAIRES)
    
    answer_enum = QUESTIONNAIRES_TO_ENUMS.get(questionnaire)
    matches = {option.value for option in answer_enum if option.value.lower() in answer.lower()}

    if len(matches) == 0:
        warnings.warn("No valid answer option found in last line of LLM response. Proceeding with empty answer.")
        return ""
    elif len(matches) > 1:
        warnings.warn("More than one valid answer option found in last line of LLM reponse. Proceeding with empty answer.")
        return ""
    else:
        return list(matches)[0]


def split_llm_output(output:str) -> (str, str):
    """Splits LLM output into reasoning and question answer.

        Expects last line of output to contain the question answer.
        Returns empty string for reasoning if output is only one line.
        
        Args:
            output (str) : the LLM output
        
        Returns:
            ((str, str)) : the reasoning and the raw answer
    """
    reasoning, delim, raw_answer = output.rpartition('\n')
    return reasoning, raw_answer


def process_llm_output(output:str, questionnaire:str='birds') -> (str, str):
    """Processes raw LLM output into reasoning and cleaned + validated answer.
    
        Args:
            output (str) : the LLM output
            questionnaire (str) : specifies questionnaire/answer options to validate against

        Returns:
            ((str, str)) : the reasoning and the cleaned + validated answer
    """
    reasoning, raw_answer = split_llm_output(output)
    return reasoning, extract_answer(raw_answer, questionnaire)