# Using griptape with LM Studio
This repository contains a full example for using griptape wit LM Studio and Llama 3.
The code in this repository demonstrates, how to connect to LM Studio, how to write a simple agent using this connection and writing a custom tool.
griptape's Tool calling works surprisingly well with Llama 3 - at least in this relatively simple use case.
I will have to make more experiments to see, how Llama 3 deals with more complex scenarios.

## Installation
Clone the repository to a local directory. I suggest creating a virtual environment first. The Python code itself only requires griptape to be installed. See the [griptape documentation](https://docs.griptape.ai/stable/griptape-framework/) for details.

```sh
pip install "griptape[all]" -U
```

You will also need [LM Studio](https://lmstudio.ai/), a Llama 3 model (the code was tested with `bartowski/NeuralDaredevil-8B-abliterated-GGUF`) and a local install of [Searx](https://github.com/searx/searx-docker).

## Running the code
```sh
python searx.py
```
This command will launch the program with a currently hard-coded prompt. Change the string at line 31 in `searx.py` to ask a different question.

## Planned features
 * To make the testing of agents easier I plan to write a simple UI with [Mesop](https://google.github.io/mesop).