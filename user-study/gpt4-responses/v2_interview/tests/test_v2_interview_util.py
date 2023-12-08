
import sys
# setting path
sys.path.append('../v2_interview')

import pytest

from utils.api_messages import (
    get_msg
)

# Current folder: IDP-simulated-user-exp\user-study\gpt4-responses\v2_interview
# Execute: pytest -vv tests 

def test_test():
    assert True

# @pytest.mark.xfail
def test_test_2():
    assert False