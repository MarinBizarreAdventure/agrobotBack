# How to use
Instructions
## Editor setup
I am writing python in vscode so the direnv extension will really help you have the flake environment loaded into the editor.
You will also need to install `direnv` as a package.

This will just help you manage other python extensions you may have installed since python on nix is a mess and it hurts.

The flake's role is just to set up some environment variables that depend on C libs or binaries that are otherwise linked using a dynamic linker. 
You know, `ld` and nix are so frustrating to work with.

## Project structure
There is a shared `extole` *"library"* in `/extole`.
It mostly has stuff that will help you operate with objects and extend them with other methods instead of just working with plain json.
Plain json is great too, but sometimes you just want life to be easier and have some interface.
The other directories serve as projects/packages you build independently with poetry.

## Project setup

1. Run `nix develop` or activate the env with `direnv`
2. Run `poetry install` 

### .env
In the repo root, add a `.env` file where you'll need following variables

1. `EXTOLE_JWT` - your token you grab from my.extole
2. `OPENAI_API_KEY` - if you don't have one, ask Ben to create one for you

### How to use
There are some scripts in the `pyproject.toml` file that can be edited.
Those are just entrypoints for larger, per-package scripts.

**Currently supported ones are:**

1. `poetry run report` - Playground to build an agent that will do Natural Language -> Report
2. `poetry run migrate` - Playground for campaign migration tools
3. `poetry run ai_migrate` - Run the agent code to see how it migrates components