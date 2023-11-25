# Imports
import copy
import interview_util
import interview_util_images
import openai
import pandas as pd


# Class
class Interview:
    """
    A class for simulating a last answer of the user study.

    ...

    Attributes
    ----------
    csv_file_path : str
        a string for reading the csv
    df : pd.DataFrame
        a dataframe that stores the answers of the user study

    Methods
    -------
    create_template()
        Creates the template that is to be sent to gpt-4 as messages
    """
    
    def __init__(self, csv_file_path:str) -> None:
        self.csv_file_path = csv_file_path
        self.df = pd.read_csv(csv_file_path)
        self.df = self.df.tail(-2)
        self.df.drop(self.df.columns[[0, 1]], axis=1, inplace=True)
        self.df = self.df.fillna('NA')
        pd.set_option('display.max_columns', None)
        
        
    def conduct(self):
        answered_questions =  ["Q" + str(i) for i in range(1, 20+1)]
        unanswered_question = answered_questions.pop(19)
        self.df['Q20_gpt4'] = self.df.apply(self.get_answer, args = (answered_questions, unanswered_question),axis=1)
        self.df.to_csv("out.csv")
        
        
    def get_answer(self, row, given_columns:list, open_question:str):
        query = self.create_template(row, given_columns, open_question)
        print(query)
        response = openai.ChatCompletion.create(
            model = "gpt-4-vision-preview",
            max_tokens = 300,
            messages = query
        )
        return response["choices"][0]["message"]["content"]
        
        
    def create_template(self, row, given_columns:list, open_question:str):
        self.messages = interview_util.MESSAGE_BASE_SYS +\
            interview_util.MESSAGE_BASE_AGE + [{"role": "assistant", "content": str(row['D1'])}] +\
            interview_util.MESSAGE_BASE_SEX +\
                [{"role": "assistant", "content": self._replace(str(row['D2']), interview_util.SEX_MAPPING)},] +\
            interview_util.MESSAGE_BASE_EMPLOY +\
                [{"role": "assistant", "content": self._replace(str(row['D3']), interview_util.EMPLOYMENT_MAPPING)},] + \
            interview_util.MESSAGE_BASE_MLXP1 +\
                [{"role": "assistant", "content": self._replace(str(row['D4']), interview_util.EXPERIENCE_MAPPING)},] +\
            interview_util.MESSAGE_BASE_MLXP2 + [{"role": "assistant", "content": row['D5']},] +\
            interview_util.MESSAGE_BASE_WARMUP1 +\
                [{"role": "assistant", "content": 'Least Auklet:\n' + row['Intro-1'] + '\n\nRhinoceros Auklet:\n' + row['Q158']},]+\
            interview_util.MESSAGE_BASE_WARMUP2 +\
                [{"role": "assistant", "content": 'Rhinoceros Auklet:\n' + row['Intro-1.1'] +\
                    '\n\nLeast Auklet:\n' + row['Q159'] + \
                    '\n\nParakeet Auklet:\n' + row['Q160'] + \
                    '\n\nCrested Auklet:\n' + row['Q161']},] +\
            interview_util.MESSAGE_BASE_UNDERSTANDING +\
                [{"role": "assistant", "content": self._replace(str(row['D4']), interview_util.UNDERSTANDING_MAPPING)},] 
                
        for column in given_columns:
            self._create_question_and_answer(row, column)
            
        self._create_question(open_question)
        
        return self.messages
        
    
    def _replace(self, string:str, dictionary:dict):
        result = string
        for number, _string in dictionary.items():
            result = result.replace(number, _string)
        return result
    
    
    def _create_question_and_answer(self, row, column:str):
        self._create_question(column)
        self.messages = self.messages + \
            [{"role": "assistant", "content": interview_util.AUKLET_MAPPING.get(str(row[column]), "NA")},]
            
    def _create_question(self, column:str):
        question = copy.deepcopy(interview_util.MESSAGE_QUESTION_AUKLET)
        image = interview_util_images.IMAGE_MAPPING_AUKLET[column]
        question[0]['content'] = question[0]['content'] + image
        self.messages = self.messages + question.copy()
  
    
test = Interview("user-study\SimulatedUsers-Final_August4.csv")
test.conduct()
# answered_questions =  ["Q" + str(i) for i in range(1, 20+1)]
# unanswered_question = answered_questions.pop(19)


# for elements in test.create_template(test.df.to_dict(orient='records')[0], answered_questions, unanswered_question):
#     for key, item in elements.items():
#         print(key)
#         print(item)
    
# test.create_template(test.df.to_dict(orient='records')[0], answered_questions, unanswered_question)