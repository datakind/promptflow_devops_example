# Introduction

![ReliefWeb Promptflow Demo](./rweb_flow.png)

This repo contains sample code for workshops on using Promptflow as part of operationlizing LLMs for humanitarian response. The example flow does the following:

1. Extracts entities from user input and converts them to a query on ReliefWeb
2. Runs query again Reliefweb API to get situation reports for the user's request
3. Summarized the response
4. Extracts references 
5. Presents results to the user

The flow also includes:

1. Content safety filtering
2. Prompt variants
3. State grounding
4. Dynamic grounding using deepeval

## Setup

1. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) by selecting the installer that fits your OS version. Once it is installed you may have to restart your terminal (closing your terminal and opening again)
2. In this directory, open terminal
3. `conda env create -f environment.yml`
4. `conda activate promtpflow-serve`

Promptflow can be run from the commandline, see [documentation](https://microsoft.github.io/promptflow/index.html) for further information, but a nice way to use it is to use VS Code which has a user interface for managing flows. To use this ..

1. Download [VS Code](https://code.visualstudio.com/download)
2. Install the [promptflow extension](https://marketplace.visualstudio.com/items?itemName=prompt-flow.prompt-flow)
3. Install the conda environment (see above)
4. Open a `flow.dag.yaml`
5. At top of file, click install dependencies
6. Select the conda environment `promptflow-serve`
7. Re-open `flow.dag.yaml`, select 'visual editor' at the top to see the lovely user interface
8. To run the flows click the play icon at the top of the promptflow user interface 

You will also need to configure LLM keys. The demo assumes Azure OpenAI, but scripts can also support OpenAI direct. To configure your LLM environment ...

1. Copy `.env.example` to `.env`
2. Set keys appropriately

## Azure versus OpenAI

The code is configured to run with Azure OpenAI. You can also run with OpenAI directly as follows:

1. In promptflow, create a new OpenAI conntection (in VS code select 'P' promptflow on left,click + under connections). For command line creation, see `.github/test_deploy,yml`)

2. Set connection in all LLM nodes in the flow using VS code (click on them, change connection)

3. In `deep_eval.py` ajust code to use OpenAIChat instead of AzureOpenAI. At some point this will be a settings

# Development

## Pre-commit hooks

The repo has been set up with black and flake8 pre-commit hooks. These are configured in the ``.pre-commit-config.yaml` file and initialized with `pre-commit autoupdate`.

On a new repo, you must run `pre-commit install` to add pre-commit hooks.

To run code quality tests, you can run `pre-commit run --all-files`