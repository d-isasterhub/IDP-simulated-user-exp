from enum import Enum
import pandas as pd
from typing import TypedDict
import pprint
import re

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

class UserBackground(TypedDict):
    """A class that represents the demographic/domain background of a user"""

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
    features_ca : str
    features_la : str
    features_pa : str
    features_ra : str


class UserProfile:
    """
    A class that represents a user profile (demographic data, AI experience, warm-up questions)

    """

    user_background : UserBackground
    warmup_answers : WarmupAnswers

    human_predictions : [Auklets]
    human_agreement : [str] # maybe int is better? idk

    profiling_prompt : str

    def __init__(self):
        """Profile filled with default values (average/most common values)"""

        self.user_background = {
            "age" : 30,
            "gender" : Gender.FEMALE,
            "employment_status" : Employment.FULL_TIME,
            "ai_user" : True,
            "ai_dev" : False
        }

        # TODO: default values for feature descriptions?

        self.warmup_answers = {
            "features_ca" : "",
            "features_la" : "",
            "features_pa" : "",
            "features_ra" : ""
        }

        # beware
        self.human_predictions = [Auklets.CRESTED] * 20 
        self.human_agreement = ["7"] * 6

    def __init__(self, age:int, gender:Gender, employment_status:Employment, ai_user:bool, ai_dev:bool, 
                 features_ca:str, features_la:str, features_pa:str, features_ra:str):
        """Profile info based on manually given parameters"""
        
        self.user_background = {
            "age" : age,
            "gender" : gender,
            "employment_status" : employment_status,
            "ai_user" : ai_user,
            "ai_dev" : ai_dev
        }

        self.warmup_answers = {
            "features_ca" : features_ca,
            "features_la" : features_la,
            "features_pa" : features_pa,
            "features_ra" : features_ra
        }

        self.human_predictions = []
        self.human_agreement = []

    def __init__(self, user_series : pd.Series):
        """Profile info based on a single pandas Series (dataset row)"""
        
        self.user_background = {
            "age" : user_series.at['Age'],
            "gender" : Gender[user_series.at['Gender'].upper()],
            "employment_status" : Employment[user_series.at['Employment'].upper()],
            "ai_user" : user_series.at['AI_User'],
            "ai_dev" : user_series.at['AI_Dev'],
        }

        self.warmup_answers = {
            "features_ca" : user_series.at['Warmup_2_CA'],
            "features_la" : user_series.at['Warmup_2_LA'],
            "features_pa" : user_series.at['Warmup_2_PA'],
            "features_ra" : user_series.at['Warmup_2_RA']
        }

        self.human_predictions = []
        for i in range(20):
            self.human_predictions.append(user_series.at['Q' + str(i+1)])

        self.human_agreement = []
        for i in range(6):
            self.human_agreement.append(user_series.at['Q_' + str(i+1)])


    def __str__(self) -> str:
        return "User background : " + pprint.pformat(self.user_background) + \
            "\nWarmup Questions : " + pprint.pformat(self.warmup_answers) + \
            "\nPredictions : " + pprint.pformat(self.human_predictions) + \
            "\nAgreements : " + pprint.pformat(self.human_agreement)

    def profiling_prompt(self, SYSTEM) -> str:
        """Replaces placeholders in profiling prompt with actual profiling info"""

        placeholders = {
            'bg_numbers' : ["AGE"],
            'bg_enums' : ["GENDER", "EMPLOYMENT_STATUS"],
            'bg_some_or_none' : ["AI_USER", "AI_DEV"],
            'wu_text' : ["FEATURES_CA", "FEATURES_LA", "FEATURES_PA", "FEATURES_RA"]
        }

        # using replace() would make a copy each time. to avoid this, we work on a list of tokens.
        tokenized_prompt = re.findall(r"[\w']+|[.,!?;]", SYSTEM)
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
        PROFILING = re.sub(r'\s+([?.!,])', r'\1', PROFILING)

        self.profiling_prompt = PROFILING
        return PROFILING