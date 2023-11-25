import interview_util_prompts
import interview_util_images

MESSAGE_BASE = [
    {"role": "system", "content": interview_util_prompts.SYSTEM}, 
    {"role": "user", "content": interview_util_prompts.USER_AGE},
    {"role": "assistant", "content": ""},
    {"role": "user", "content": interview_util_prompts.USER_SEX},
    {"role": "assistant", "content": ""},
    {"role": "user", "content": interview_util_prompts.USER_EMPLOYMENT_STATUS},
    {"role": "assistant", "content": ""},
    {"role": "user", "content": interview_util_prompts.USER_ML_EXPERIENCE_1},
    {"role": "assistant", "content": ""},
    {"role": "user", "content": interview_util_prompts.USER_ML_EXPERIENCE_2},
    {"role": "assistant", "content": ""},
    {"role": "user", "content": interview_util_prompts.OBJECTIVE_DESCRIPTION_1},
    {"role": "user", "content": interview_util_prompts.OBJECTIVE_DESCRIPTION_2},
    {"role": "user", "content": [
        {"type": "text", "text":interview_util_prompts.WARM_UP_TASK_1_LEAST}
    ] + interview_util_images.WARM_UP_TASK_1_LEAST_IMAGES},
    {"role": "user", "content": [
        {"type": "text", "text":interview_util_prompts.WARM_UP_TASK_1_RHINOCEROS}
    ] + interview_util_images.WARM_UP_TASK_1_RHINOCEROS_IMAGES},
    {"role": "user", "content": interview_util_prompts.WARM_UP_TASK_1},
    {"role": "assistant", "content": ""},
    {"role": "user", "content": interview_util_prompts.OBJECTIVE_DESCRIPTION_3},
    {"role": "user", "content": [
        {"type": "text", "text":interview_util_prompts.WARM_UP_TASK_2_RHINOCEROS}
    ] + []},
    {"role": "user", "content": [
        {"type": "text", "text":interview_util_prompts.WARM_UP_TASK_2_LEAST}
    ] + []},
    {"role": "user", "content": [
        {"type": "text", "text":interview_util_prompts.WARM_UP_TASK_2_PARAKEET}
    ] + []},
    {"role": "user", "content": [
        {"type": "text", "text":interview_util_prompts.WARM_UP_TASK_2_CRESTED}
    ] + []},
    {"role": "user", "content": interview_util_prompts.WARM_UP_TASK_2},
    {"role": "assistant", "content": ""},
    {"role": "user", "content": interview_util_prompts.OBJECTIVE_DESCRIPTION_4},
    {"role": "user", "content": interview_util_prompts.UNDERSTANDING_CHECK},
    {"role": "assistant", "content": ""},
]