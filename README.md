CTF Exploit Analysis – Agent Failure Detection

Overview

This repository contains a system for classifying and handling agent failure scenarios in task-based environments, with applications in exploit development, AI agent evaluation, and automation testing.

Agents attempt tasks over iterations (0, 1, …, t), but progress is not always evident. This project aims to:

Identify failure scenarios by analyzing word distributions in logs from successful and failed runs.
Estimate the probability of agent failure using Bayesian inference on word frequencies.
Handle failure cases by designing a failure-handling system similar to @retry for agents.
This work can be used to:

Prompt agents to recover upon failure (e.g., stop a bad trajectory early).
Improve agent design by understanding failure patterns.

# <span style="color:red">Attension</span>: I would not take this approach in the future...
![Alt Text: This is a meme.](https://preview.redd.it/rprze5xd9fk31.png?width=1080&crop=smart&auto=webp&s=e9763816bec9ef566e9b2ab9afdf9daf753c3811)

