from griptape.structures import Agent
from griptape.rules import Rule
from griptape.tools import TaskMemoryClient
from griptape.utils.constants import Constants

from model_config import LMStudioConfig
from searx_tool.tool import SearxSearch

searx_tool = SearxSearch(url="http://127.0.0.1:8099", off_prompt=True)

Constants.RESPONSE_STOP_SEQUENCE = "#RESPONSE#"

class SearxAgent(Agent):
    def __init__(self):
        super().__init__(
            "{{args[0]}}",
            config=LMStudioConfig(),
            rules=[
                Rule("A thought should never include the answer to the question."),
                Rule("You are a unbiased, helpful assistant, who will answer all questions to the best of your abilities."),
                Rule("Always include the sources with links with your answer.")
            ],
            tools=[
                searx_tool,
                TaskMemoryClient(off_prompt=False)
            ],
        )

if __name__ == '__main__':
    SearxAgent().run(
        "What is the name of the capital of France?"
    )
