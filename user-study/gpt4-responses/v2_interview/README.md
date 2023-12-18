## Requirements

Required packages can be found in [the requirements file](requirements.txt).

## How to run

The main script is `v2_interview.py`, which can be run as follows:
```
    python v2_interview.py
```
and will by default simulate all 20 questions for all 50 users.

### Options

For an overview over all options, see
```
    python v2_interview.py --help
```

##### Profiling options
There are three levels of profiling, which can be chosen with the `--profiling` option.
- `full` includes all the demographic data about a human and the answers to the warmup questions (what features indicate each class)
- `minimal` includes only the answers to the warmup questions
- `none` includes neither

*NOTE: for the `none` option, each question will only be given once to the LLM. In particular, the user options explained in the following will be ignored.*

##### User options
To set a number of users to simulate, use the `--number_users` option. By default, users will be chosen randomly from the human dataset. This can be changed using the `--select_users` option, which has the three options `random`, `first`, and `last`.

For example, to simulate the first 5 humans in the dataset, run
```
    python v2_interview.py --number_users=5 --select_users=first
```

##### Question options
There are two ways to choose which questions will be simulated.
1. `auto` automatically chooses a number of questions (can be chosen with `--number_questions`, default: 20) in one of three ways (can be chosen with `--select_questions`, default: `balanced`):
    - `random`
    - `balanced` (keeps the number of questions similar between classes)
    - `first`

For example, to simulate the first 5 questions, run
```
    python v2_interview.py auto --number_questions=5 --select_questions=first
```

2. `manual` allows you to choose individiual questions by their number. At least one number must be given with the `--questions` option.

For example, to simulate questions 1, 7, and 13, run
```
    python v2_interview.py manual --questions 1 7 13
```

## Outputs

All generated outputs can be found in the [out](out/) folder.
- `interview_protocol.txt` contains all prompts and the corresponding LLM outputs
- `simulated_interview_results.csv` contains only the question answers for each user