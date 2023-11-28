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
    """A class that represents the answers given by user to warmup questions"""

    # warm-up: features from raw pictures
    features_la : str
    features_ra : str

    # warm-up: features from XAI heatmap
    heatmap_features_ca : str
    heatmap_features_la : str
    heatmap_features_pa : str
    heatmap_features_ra : str


class UserProfile:
    """
    A class that represents a user profile (demographic data, AI experience, warm-up questions)

    """

    user_background : UserBackground
    warmup_answers : WarmupAnswers

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
            "features_la" : "",
            "features_ra" : "",
            "heatmap_features_ca" : "",
            "heatmap_features_la" : "",
            "heatmap_features_pa" : "",
            "heatmap_features_ra" : ""
        }

    def __init__(self, age:int, gender:Gender, employment_status:Employment, ai_user:bool, ai_dev:bool, 
                 features_la:str, features_ra:str, heatmap_features_ca:str, heatmap_features_la:str, 
                 heatmap_features_pa:str, heatmap_features_ra:str):
        """Profile info based on manually given parameters"""
        
        self.user_background = {
            "age" : age,
            "gender" : gender,
            "employment_status" : employment_status,
            "ai_user" : ai_user,
            "ai_dev" : ai_dev
        }

        self.warmup_answers = {
            "features_la" : features_la,
            "features_RA" : features_ra,
            "heatmap_features_ca" : heatmap_features_ca,
            "heatmap_features_la" : heatmap_features_la,
            "heatmap_features_pa" : heatmap_features_pa,
            "heatmap_features_ra" : heatmap_features_ra
        }

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
            "features_la" : user_series.at['Warmup_1_LA'],
            "features_ra" : user_series.at['Warmup_1_RA'],
            "heatmap_features_ca" : user_series.at['Warmup_2_CA'],
            "heatmap_features_la" : user_series.at['Warmup_2_LA'],
            "heatmap_features_pa" : user_series.at['Warmup_2_PA'],
            "heatmap_features_ra" : user_series.at['Warmup_2_RA']
        }

    def __str__(self) -> str:
        return "User background : " + pprint.pformat(self.user_background) + "\nWarmup Questions : " + pprint.pformat(self.warmup_answers)

    def profiling_prompt(self, SYSTEM) -> str:
        """Replaces placeholders in profiling prompt with actual profiling info"""

        age_placeholders = ["AGE"]
        enum_placeholders = ["GENDER", "EMPLOYMENT_STATUS"]
        bool_placeholders = ["AI_USER", "AI_DEV"]
        warmup_placeholders = ["FEATURES_LA", "FEATURES_RA", "HEATMAP_FEATURES_CA", "HEATMAP_FEATURES_LA", 
                        "HEATMAP_FEATURES_PA", "HEATMAP_FEATURES_RA"]

        # using replace() would make a copy each time. to avoid this, we work on a list of tokens.
        tokenized_prompt = re.findall(r"[\w']+|[.,!?;]", SYSTEM)
        # print(tokenized_prompt)

        def replace_placeholder(p):
            if p == "AGE":
                return str(self.user_background[p.lower()])
            elif p in enum_placeholders:
                return self.user_background[p.lower()].value
            elif p in bool_placeholders:
                return "" if self.user_background[p.lower()] else "no" 
            elif p in warmup_placeholders:
                return self.warmup_answers[p.lower()]
            else:
                return p

        tokenized_prompt = list(map(replace_placeholder, tokenized_prompt))
        PROFILING = " ".join(tokenized_prompt)
        PROFILING = re.sub(r'\s+([?.!])', r'\1', PROFILING)

        self.profiling_prompt = PROFILING
        return PROFILING