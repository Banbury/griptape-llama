# Using griptape with LM Studio
This repository contains a full example for using the agent framework [griptape](https://docs.griptape.ai) with LM Studio and Llama 3.
The code in this repository demonstrates, how to connect to LM Studio, how to write a simple agent using this connection and writing a custom tool.

griptape's Tool calling works surprisingly well with Llama 3 - at least in this relatively simple use case.
I will have to make more experiments to see, how Llama 3 deals with more complex scenarios.

## Installation
Clone the repository to a local directory. I suggest creating a virtual environment first.
To install the Python requirements use the following command on the command line:
```sh
pip install -r requirements.txt
```

You will also need [LM Studio](https://lmstudio.ai/), a local install of [Searx](https://github.com/searx/searx-docker), and a Llama 3 model (the code was tested with `bartowski/NeuralDaredevil-8B-abliterated-GGUF`). You will also need to load an embedding model in LM Studio server.

## Running the code
```sh
mesop gui.py
```
This command will launch a simple web gui with a chat box at `http://localhost:32123/`. (Being a Google product it only runs in Chrome.) 

You can ask the bot simple questions, which it will try to answer using the search tool. 

In my experiments I got an answer about half of the time. Which is still much better than any other agent framework I have tried (like Autogen).
