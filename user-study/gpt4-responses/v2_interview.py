import openai

from v2_interview_util import (
    get_msg,
    get_msg_with_image
)

from v2_interview_util_prompts import (
    SYSTEM,
    USER
)

# TODO: modify SYSTEM
PROFILING = SYSTEM

# https://platform.openai.com/docs/api-reference/chat/create?lang=python
response = openai.ChatCompletion.create(
    model = "gpt-4-vision-preview",
    max_tokens = 300,
    messages = 
        get_msg(role="system", prompt=PROFILING) +\
        get_msg_with_image(role="user", prompt=USER, image="3-Crested.png")
)

actual_response = response["choices"][0]["message"]["content"]

# Question-Image mapping:
# 1. 0-Crested.png
# 2. 1-Crested.png
# 3. 2-Crested.png
# 4. 3-Crested.png
# 5. 4-Crested.png
# 6. 15-Least.png
# 7. 16-Least.png
# 8. 17-Least.png
# 9. 18-Least.png
# 10. 19-Least.png
# 11. 31-Parakeet.png
# 12. 32-Parakeet.png
# 13. 37-Parakeet.png
# 14. 38-Parakeet.png
# 15. 47-Parakeet.png
# 16. 50-Rhinoceros.png
# 17. 51-Rhinoceros.png
# 18. 53-Rhinoceros.png
# 19. 54-Rhinoceros.png
# 20. 55-Rhinoceros.png