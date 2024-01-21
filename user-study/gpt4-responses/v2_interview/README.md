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

#### Profiling options
There are two levels of profiling, which can be chosen with the following options:
- `--with_profiling` includes all the demographic data about a human and the answers to the warmup questions (what features indicate each class)
- `--without_profiling` includes neither

*NOTE: for the `--without_profiling` option, each question will only be given once to the LLM. In particular, the user options explained in the following will be ignored.*

#### User options
To set a number of users to simulate, use the `--number_users` option. By default, users will be chosen randomly from the human dataset. This can be changed using the `--select_users` option, which has the three options `random`, `first`, and `last`.

For example, to simulate the first 5 humans in the dataset, run
```
    python v2_interview.py --number_users=5 --select_users=first
```

#### Prompting/Reasoning options
To select a prompt varation, use the `--reasoning` option. The available options are
- `none`: without reasoning
- `profile_first`: profile users, then ask for answer + reasoning
- `heatmap_first`: first generate heatmap descriptions, then profile users and ask for answer and reasoning (i.e. our attempt at splitting the reasoning)
By default, option `none` will be used.


#### Question/Agreement options
For the prediction questions, there are two ways to choose which questions will be simulated.
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

3. Similarly, one can choose to simulate the agreement questions with the `agreement` option. There are multiple additional options for this:
- `--questions`: which of the agreement questions to simulate (by default: all questions, if `--with_example` is set, without the example question)
- `--example`: which question to show the LLM as an example (by default: the first one)
- `--with_accuracy` or `--without_accuracy`: to set whether to include the number of questions that the user answered correctly in the prompt (by default: with accuracy)
- `--with_average` or `--without_average`: whether to include the average human score for the agreement questions as profiling (by default: without average)
- `--fixed_average` or `--user_average`: whether to include the average human score for the agreement questions as profiling or use a fixed value (4) (by default: user average)
- `--with_example` or `--without_example` : whether to include a question as example (by default: with example) - note that if `--without_example` is set, any arguments to the previous `--example` option will be ignored

Example:
```
    python v2_interview.py agreement --without_accuracy --questions 2 3 4
```

*NOTE: the questions that are actually simulated are computed as the questions in the `--questions` argument minus the `--example` question.*

## Outputs

All generated outputs can be found in the [out](out/) folder.
There is one subfolder with results from the agreement question simulations containing separate files for simulations with/without accuracy:
```
> agreement
```
For the bird questions, there are multiple subfolders:
```
> no_reason
> reason_heatmap_first
> reason_profile_first
```
In each subfolder, there are two more subfolders corresponding to the profiling options:
```
> no_profile
> profile
```
containing both a protocol and a results file.