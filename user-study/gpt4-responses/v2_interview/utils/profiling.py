from enum import Enum
import pandas as pd
from typing import TypedDict
from collections import defaultdict
import pprint
import re
import itertools

# -------------------------------- enums for demographic data -----------------------

class Employment(Enum):
    """Enum for the employment options"""

    RETIRED = "retired"
    STUDENT = "being a student"
    FREELANCER = "being a freelancer"
    UNEMPLOYED = "being unemployed"
    PART_TIME = "working part-time"
    FULL_TIME = "working full-time"
    OTHER = "neither retired, studying, unemployed, or working"

class Gender(Enum):
    """Enum for the gender options"""

    FEMALE = "female"
    MALE = "male"
    PREFER_NOT_TO_SAY = "unknown"

class Auklets(Enum):
    """Enum for the 4 bird species"""

    CRESTED = "Crested Auklet"
    LEAST = "Least Auklet"
    PARAKEET = "Parakeet Auklet"
    RHINOCEROS = "Rhinoceros Auklet"

# -------------------------- default data for no-profiling option -------------------

DEFAULT_DATA = pd.Series({
    'id' : 0,
    'Age' : 0,
    'Gender' : 'female',
    'Employment' : 'other',
    'AI_User' : True,
    'AI_Dev' : True,
    'Warmup_2_CA' : "",
    'Warmup_2_LA' : "",
    'Warmup_2_PA' : "",
    'Warmup_2_RA' : "",
    'Q1' : "",
    'Q2' : "",
    'Q3' : "",
    'Q4' : "",
    'Q5' : "",
    'Q6' : "",
    'Q7' : "",
    'Q8' : "",
    'Q9' : "",
    'Q10' : "",
    'Q11' : "",
    'Q12' : "",
    'Q13' : "",
    'Q14' : "",
    'Q15' : "",
    'Q16' : "",
    'Q17' : "",
    'Q18' : "",
    'Q19' : "",
    'Q20' : "",
    'Q_1' : "",
    'Q_2' : "",
    'Q_3' : "",
    'Q_4' : "",
    'Q_5' : "",
    'Q_6' : "",
})

# ------------------------ data structures for user profiles ----------------------

class UserBackground(TypedDict):
    """A class that represents the demographic/domain background of a user"""

    # id
    id : int

    # general demographic info
    age : int
    gender : Gender
    employment_status : Employment

    # dataset also has option "no experience", but i think that's redundant
    ai_user : bool
    ai_dev : bool
    
    # TODO: add experience details (encoded)?

class WarmupAnswers(TypedDict):
    """A class that represents the answers given by user to warmup question"""

    # warm-up: features from XAI heatmap
    heatmap_features_ca : str
    heatmap_features_la : str
    heatmap_features_pa : str
    heatmap_features_ra : str


# --------------------------------- UserProfile class --------------------------------

class UserProfile:
    """
    A class that represents a user profile (demographic data, AI experience, warm-up questions)

    """

    user_background : UserBackground
    warmup_answers : WarmupAnswers

    # defaultdicts return a default value if accessed by a key that doesn't exist 
    # -> useful for csv output
    human_predictions : defaultdict[int, Auklets]
    human_agreements : defaultdict[int, str] # maybe (int, int) is better? idk
    llm_predictions : defaultdict[int, str]
    llm_agreements : defaultdict[int, str]

    profiling_prompt : str

    def __init__(self):
        """Profile filled with default values (average/most common values)"""

        self.user_background = {
            "id" : 0,
            "age" : 30,
            "gender" : Gender.FEMALE,
            "employment_status" : Employment.FULL_TIME,
            "ai_user" : True,
            "ai_dev" : False
        }

        # TODO: default values for feature descriptions?

        self.warmup_answers = {
            "heatmap_features_ca" : "",
            "heatmap_features_la" : "",
            "heatmap_features_pa" : "",
            "heatmap_features_ra" : ""
        }

        # beware, these are dummy values
        self.human_predictions = defaultdict(lambda: "NA")
        self.human_agreements = defaultdict(lambda: "NA")
        self.llm_predictions = defaultdict(lambda: "NA")
        self.llm_agreements = defaultdict(lambda: "NA")

        self.profiling_prompt = None

    # TODO: constructors don't work like this in python :c
    def __init__(self, id:int, age:int, gender:Gender, employment_status:Employment, ai_user:bool, ai_dev:bool, 
                 features_ca:str, features_la:str, features_pa:str, features_ra:str):
        """Profile info based on manually given parameters"""
        
        self.user_background = {
            "id" : id,
            "age" : age,
            "gender" : gender,
            "employment_status" : employment_status,
            "ai_user" : ai_user,
            "ai_dev" : ai_dev
        }

        self.warmup_answers = {
            "heatmap_features_ca" : features_ca,
            "heatmap_features_la" : features_la,
            "heatmap_features_pa" : features_pa,
            "heatmap_features_ra" : features_ra
        }

        self.human_predictions = defaultdict(lambda: "NA")
        self.human_agreements = defaultdict(lambda: "NA")
        self.llm_predictions = defaultdict(lambda: "NA")
        self.llm_agreements = defaultdict(lambda: "NA")

        self.profiling_prompt = None

    def __init__(self, user_series : pd.Series):
        """Profile info based on a single pandas Series (dataset row)"""
        
        self.user_background = {
            "id" : user_series.at['id'],
            "age" : user_series.at['Age'],
            "gender" : Gender[user_series.at['Gender'].upper()],
            "employment_status" : Employment[user_series.at['Employment'].upper()],
            "ai_user" : user_series.at['AI_User'],
            "ai_dev" : user_series.at['AI_Dev'],
        }

        self.warmup_answers = {
            "heatmap_features_ca" : user_series.at['Warmup_2_CA'],
            "heatmap_features_la" : user_series.at['Warmup_2_LA'],
            "heatmap_features_pa" : user_series.at['Warmup_2_PA'],
            "heatmap_features_ra" : user_series.at['Warmup_2_RA']
        }
        
        self.human_predictions = defaultdict(lambda: "NA")
        self.human_agreements = defaultdict(lambda: "NA")
        self.llm_predictions = defaultdict(lambda: "NA")
        self.llm_agreements = defaultdict(lambda: "NA")

        for i in range(20):
            self.human_predictions[i+1] = str(user_series.at['Q' + str(i+1)])

        for i in range(6):
            self.human_agreements[i+1]= str(user_series.at['Q_' + str(i+1)])
        
        self.profiling_prompt = None

        self.profiling_prompt = None


    def __str__(self) -> str:
        return "User background : " + pprint.pformat(self.user_background) + \
            "\nWarmup Questions : " + pprint.pformat(self.warmup_answers) + \
            "\nPredictions : " + pprint.pformat(self.human_predictions) + \
            "\nAgreements : " + pprint.pformat(self.human_agreements)

    def personalize_prompt(self, SYSTEM, profiling=False) -> str:
        """Replaces placeholders in profiling prompt with actual profiling info"""

        placeholders = {
            'bg_numbers' : ["AGE"],
            'bg_enums' : ["GENDER", "EMPLOYMENT_STATUS"],
            'bg_some_or_none' : ["AI_USER", "AI_DEV"],
            'wu_text' : ["HEATMAP_FEATURES_CA", "HEATMAP_FEATURES_LA", "HEATMAP_FEATURES_PA", "HEATMAP_FEATURES_RA"]
        }

        # using replace() would make a copy each time. to avoid this, we work on a list of tokens.
        tokenized_prompt = re.findall(r"[\w']+|[.,!:?;-]|[\n]", SYSTEM)
        # print(tokenized_prompt)

        def replace_placeholder(p):
            if p in placeholders['bg_numbers']:
                return str(self.user_background[p.lower()])
            elif p in placeholders['bg_enums']:
                return self.user_background[p.lower()].value
            elif p in placeholders['bg_some_or_none']:
                return "some" if self.user_background[p.lower()] else "no" 
            elif p in placeholders['wu_text']:
                return self.warmup_answers[p.lower()]
            else:
                return p

        tokenized_prompt = list(map(replace_placeholder, tokenized_prompt))
        PROFILING = " ".join(tokenized_prompt)
        PROFILING = re.sub(r'\s+([?.!,:])', r'\1', PROFILING) # remove whitespaces before ?.!,

        if profiling:
            self.profiling_prompt = PROFILING
        return PROFILING
    
    def to_csv_string(self):
        # columns 1 - 9
        infos = [str(self.user_background['age']), self.user_background['gender'].name,
            self.user_background['employment_status'].name,
            str(self.user_background['ai_user']), str(self.user_background['ai_dev']), 
            self.warmup_answers["heatmap_features_ca"], self.warmup_answers["heatmap_features_la"], 
            self.warmup_answers["heatmap_features_pa"], self.warmup_answers["heatmap_features_ra"]]
        
        human_preds = [self.human_predictions[i] for i in range(1, 21)] # columns 10-29
        human_agree = [str(self.human_agreements[i]) for i in range(1, 7)] # columns 30-35
        LLM_preds = [self.llm_predictions[i] for i in range(1, 21)] # columns 36-55
        LLM_agree = [str(self.llm_agreements[i]) for i in range(1, 7)] # columns 56-61

        csv_string = ",".join(itertools.chain(infos, human_preds, human_agree, LLM_preds, LLM_agree))
        return csv_string
    
    def get_LLM_predictions(self):
        LLM_preds = [self.llm_predictions[i] for i in range(1, 21)]
        return LLM_preds


def create_userprofiles(data : pd.DataFrame) -> [UserProfile]:
    """Constructs UserProfiles based on dataframe
    
    Args:
        data (pd.DataFrame) : dataframe with human data
        
    Returns:
        ([UserProfile]) : a list of UserProfile objects
    """
    return (data.apply(lambda x: UserProfile(x), axis = 1)).to_list()