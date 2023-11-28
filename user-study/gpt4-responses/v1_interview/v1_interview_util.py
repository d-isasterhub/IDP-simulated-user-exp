import v1_interview_util_prompts
import v1_interview_util_images

MESSAGE_BASE_SYS = [
    {"role": "system", "content": v1_interview_util_prompts.SYSTEM}, 
]

MESSAGE_BASE_AGE = [
    {"role": "user", "content": v1_interview_util_prompts.USER_AGE},
]

MESSAGE_BASE_SEX = [
    {"role": "user", "content": v1_interview_util_prompts.USER_SEX},
]

MESSAGE_BASE_EMPLOY = [
    {"role": "user", "content": v1_interview_util_prompts.USER_EMPLOYMENT_STATUS},
]

MESSAGE_BASE_MLXP1 = [
    {"role": "user", "content": v1_interview_util_prompts.USER_ML_EXPERIENCE_1},
]

MESSAGE_BASE_MLXP2 = [
    {"role": "user", "content": v1_interview_util_prompts.USER_ML_EXPERIENCE_2},
]

# ^ One message: Profiling (maybe in the System part "Who is the assistant"; alternatively: One Assistant message (2-3 sentences))

# Omit WARMUP1, Check objective description if there is something we still need
MESSAGE_BASE_WARMUP1 = [
    {"role": "user", "content": v1_interview_util_prompts.OBJECTIVE_DESCRIPTION_1},
    {"role": "user", "content": v1_interview_util_prompts.OBJECTIVE_DESCRIPTION_2},
    {"role": "user", "content": [
        {"type": "text", "text":v1_interview_util_prompts.WARM_UP_TASK_1_LEAST}
    ] + v1_interview_util_images.WARM_UP_TASK_1_LEAST_IMAGES},
    {"role": "user", "content": [
        {"type": "text", "text":v1_interview_util_prompts.WARM_UP_TASK_1_RHINOCEROS}
    ] + v1_interview_util_images.WARM_UP_TASK_1_RHINOCEROS_IMAGES},
    {"role": "user", "content": v1_interview_util_prompts.WARM_UP_TASK_1},
]

MESSAGE_BASE_WARMUP2 = [
    {"role": "user", "content": v1_interview_util_prompts.OBJECTIVE_DESCRIPTION_3},
    {"role": "user", "content": [
        {"type": "text", "text":v1_interview_util_prompts.WARM_UP_TASK_2_RHINOCEROS}
    ] + v1_interview_util_images.WARM_UP_TASK_2_RHINOCEROS_IMAGES},
    {"role": "user", "content": [
        {"type": "text", "text":v1_interview_util_prompts.WARM_UP_TASK_2_LEAST}
    ] + v1_interview_util_images.WARM_UP_TASK_2_LEAST_IMAGES},
    {"role": "user", "content": [
        {"type": "text", "text":v1_interview_util_prompts.WARM_UP_TASK_2_PARAKEET}
    ] + v1_interview_util_images.WARM_UP_TASK_2_PARAKEET_IMAGES},
    {"role": "user", "content": [
        {"type": "text", "text":v1_interview_util_prompts.WARM_UP_TASK_2_CRESTED}
    ] + v1_interview_util_images.WARM_UP_TASK_2_CRESTED_IMAGES},
    {"role": "user", "content": v1_interview_util_prompts.WARM_UP_TASK_2},
]

MESSAGE_BASE_UNDERSTANDING = [
    {"role": "user", "content": v1_interview_util_prompts.OBJECTIVE_DESCRIPTION_4},
    {"role": "user", "content": v1_interview_util_prompts.UNDERSTANDING_CHECK},
]

MESSAGE_QUESTION_AUKLET = [
    {"role": "user", "content": 
        [
            {
                "type": "text", "text": v1_interview_util_prompts.CLASS_PREDICTION_Q1
            },
        ]
    }
]

# TODO: Scoring Questions

SEX_MAPPING = {'1' : 'Female', '2': 'Male'}

EMPLOYMENT_MAPPING = {
    '1': 'Working full-time',
    '2': 'Working part-time',
    '3': 'Unemployed and looking for work',
    '4': 'Freelancer',
    '5': 'Student',
    '6': 'Retired',
    '7': 'Other'
}

EXPERIENCE_MAPPING = {
    '1': 'No experience',
    '2': 'User',
    '3': 'Programmer / developer'
}

UNDERSTANDING_MAPPING = {
    '1': 'I will choose the label that I think is correct for the image',
    '2': 'I will choose the label that I think the model would predict'
}

AUKLET_MAPPING = {
    '1': 'Crested Auklet',
    '2': 'Least Auklet',
    '3': 'Parakeet Auklet',
    '4': 'Rhinoceros Auklet'
}