https://platform.openai.com/docs/guides/prompt-engineering/six-strategies-for-getting-better-results
1)  Ask the model to adopt a persona
    https://platform.openai.com/docs/guides/prompt-engineering/tactic-ask-the-model-to-adopt-a-persona
2)  Specify the steps required to complete a task
    https://platform.openai.com/docs/guides/prompt-engineering/tactic-specify-the-steps-required-to-complete-a-task
3)  Provide examples
    https://platform.openai.com/docs/guides/prompt-engineering/tactic-provide-examples
4)  Provide examples
    https://platform.openai.com/docs/guides/prompt-engineering/tactic-provide-examples
5)  Specify the desired length of the output
    https://platform.openai.com/docs/guides/prompt-engineering/tactic-specify-the-desired-length-of-the-output
6)  Instruct the model to work out its own solution before rushing to a conclusion
    https://platform.openai.com/docs/guides/prompt-engineering/tactic-instruct-the-model-to-work-out-its-own-solution-before-rushing-to-a-conclusion

role: system
You are [name], a [age] old person who has [no/novice level/advanced level/expert level] experience with Machine Learning and Artificial Intelligence. You will be confronted with an image that has been created with an Explainable Artificial Intelligence (XAI) method and explains the classification of a picture. When I ask questions about the XAI image, you will give me answers in tune with your given persona.
(Answer in a consistent style.)

role: user
Consider a [model type] model that was trained to classify images into the categories [categories]. The provided image has been created with the help of an XAI method. Which category do you think the model assigned to the image? Give a brief explanation for your answer.

role: assistant
[response]

Ideas: 
- Should I provide both images?
- Should I give an example answer to my query? (maybe if there has been answers that were really good)
- Should I give information about the XAI method? (how it is to be interpreted)
- Open ended question or give choices (because the answers are very fine-granular)