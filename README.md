# Data Recipes Assistant

This repo contains code for the Data Recipes Assistant. This is an approach where the user can create
data analysis recipes (code snippets) for downloading and analyzing data, where the process is LLM-assisted. So for example
"Plot of map of the population of Mali by state". Recipes can be reviewed by the user, modified, and saved
to build a library of reusable items. These can be served via a chat interface which uses less expensive LLMs.

The workflow allows the user to conversationally create recipes.

The reasons for this approach are:

- Transparency, the code generating answers is saves and can be reviewed
- Performance, the output of complex powerful LLM code generation is cached for future use
- Cost, creation of recipes is high-cost/low transaction volume, the use of recipes by end users if low-cost/high transaction volume

The hierachy of remembered information is:

- Memory: Saved results for a task, eg "What's the total population of Mali?". The code to generate is saved so memories can be refreshed
- Recipe: A more generic version of memories that can be applied to more contexts, for example "Get the total population for any country"
- Functions: Helper functions the user can provide for use in recipes

Under-the-hood, it consistens of two parts:

- A back-end server using promptflow for the LLM workflow
- A front-end streamlit app which interacts with this server

LLMs are used throughout for generating code, reviewing memory results, analyzing function interfaces and more.

## Setup

1. cp `.env.example` `.env`
2. Set Keys and model in .env file (Search Lastpass for 'data recipes assistant')
3. Create a conda environment (see below)

## To run Using Conda

1. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html) by selecting the installer that fits your OS version. Once it is installed you may have to restart your terminal (closing your terminal and opening again)
2. In this directory, open terminal
3. `conda env create -f environment.yml`
4. `conda activate promtpflow-serve`
5. You might need to force the conda python to be used with (on Mac): export PATH=`conda env list | grep "\*" | awk '{print $3"/bin"}'`:$PATH
6. In VS Code - current directory opened - install promptflow extension and select conda environment as Python runtime
7. `cd assistant`
8. Populate recipes with initial set of API skills: `python3 ./tools/create_api_skills.py`

## To run using docker Docker

1. `docker docker compose up -d`
2. Go to: (http://localhost:8501/)[http://localhost:8501/]   

## To run in promptflow

1. Open VS Code with this repo
2. Navigate to the folder in 'flows/recipes_assistant``
3. Open `flow.dag.yaml`
4. Click the little 'Open in visual editor' at the top-left of file window
5. Configure connections in promptflow viewer by clicking on nodes and adding conntections as-needed, follow instructions. The endpoints and API keys are on Azure. Here is an example or connection 'azure_openai' ...

```
$schema: https://azuremlschemas.azureedge.net/promptflow/latest/AzureOpenAIConnection.schema.json
name: "azure_openai"
type: azure_open_ai # snake case
api_key: "<user-input>" # Don't replace the '<user-input>' placeholder. The application will prompt you to enter a value when it runs.
api_base: "https://dkopenai2.openai.azure.com/"
api_type: "azure"
api_version: "2023-07-01-preview"
```

Once the above is set, there is a little link 'create connection' which you must click on, where you'll be prompted for the API key.


## TO run batch evaluation (IN PROGRESS)

1. Set up as described in previous section
2. Click the little beaker to evaluate/batch run
3. Inpor file, choose `data.jsonl` (this is where the input and validation data is)
4. When prompted for field mapping in the yaml file, select `input` and `context`
5. Click the tiny 'Run' in the yaml file
6. When done, click Promptflow add-on in laft bar
7. Click the refresh on runs, then check on the one at the top
8. Click visualize

## To create Dockerfile for promtpflow

1. `cd flows/recipes_assistant`
2. `pf flow build --source .  --output . --format docker`

## To set up using with HDeXpert generated datafiles

1. Check out [hdexpert](https://github.com/datakind/hdexpert) repo
2. Set up according to the README
3. Follow instructions to create assistant. This should populate a folder called 'data'
4. Copy that folder here
5. Link to the data folder here 
   - `cd flows/recipes_assistant/work`
   - `ln -s ../../data data`
   - `cd ../../ui/work`
   - `ln -s ../../data data`

Note that the docker build takes care of this with bind mounts.