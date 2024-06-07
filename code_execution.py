import logging
from griptape.drivers import LocalStructureRunDriver
from griptape.structures import Structure, Agent, Pipeline
from griptape.tasks import PromptTask, CodeExecutionTask, StructureRunTask
from griptape.utils import Chat
from griptape.utils.constants import Constants
from griptape.rules import Rule, Ruleset
from griptape.artifacts import BaseArtifact, TextArtifact, ErrorArtifact
from griptape.tools import StructureRunClient, TaskMemoryClient
from griptape.events import BaseEvent, StartPromptEvent, EventListener
from mdextractor import extract_md_blocks
from safeexecute import execute_python_code

from model_config import LMStudioConfig

# How long does it take to ride a horse from Winniepeg to Montreal?
# How do I pasteurize egg yolk and prepare ice cream with it?

Constants.RESPONSE_STOP_SEQUENCE = "#RESPONSE#"

model_config=LMStudioConfig()

agent_ruleset = Ruleset("AgentRuleset", rules=[
    Rule("When you use an action, don't forget the tag."),
    Rule("Any action can only be used once per step."),
    Rule("A thought should never include the answer to the question."),
])

analysisTask = PromptTask(
    "Answer the following question: {{ args[0] }}",
    id="analysis_task",
    rules=[
        Rule("You are a information broker. Your task is to answer questions by gathering information from reputable sources."),
        Rule("Cite your sources."),
        Rule("Write Python code to gather information. The code will be executed, and you will be told the result of the execution."),
        Rule("Return exactly one code block."),
        Rule("Always write the executable code in full."),
        Rule("Format the code as a Markdown code block."),
        Rule("If running the code produces an error, analyze the error and write the corrected code in full."),
        Rule("Add all requirements for running the code at the start of the code as comments, e.g. '# pip install <requirement>'.")
    ]    
)

def execute_code(task: CodeExecutionTask) -> BaseArtifact:
    output: str = task.full_context["parent_output"]
    blocks = extract_md_blocks(output)
    if (len(blocks) != 1):
        return ErrorArtifact(f"Error: There are {len(blocks)} code blocks. There should be exactly one code block.")
    result = execute_python_code(code=blocks[0])
    return TextArtifact(result)

codeTask = CodeExecutionTask(id="code_task", run_fn=execute_code)

def build_research_pipeline():
    return Pipeline(id="research_pipeline", config=model_config, tasks=[analysisTask, codeTask])

def build_research_agent():
    return Agent(
        "Input: {{ args[0] }}",
        id="research_agent",
        config=model_config,
        rulesets=[
            Ruleset("research_agent", rules=[
                Rule("You are a researcher. Your task is to answer questions factually."),
                Rule("Make sure that the input is a valid natural language question, for example \"What is the weather in Dublin?\"."),
                Rule("If the input is not a question, ask the user to rephrase their problem as a question."),
            ]),
            agent_ruleset
        ],
        tools=[
            StructureRunClient(
                name="ResearchAgent",
                description="""A tool for researching information.
                The tool will answer questions on any topic.
                """,
                driver=LocalStructureRunDriver(structure_factory_fn=build_research_pipeline), 
                off_prompt=True
            ),
            TaskMemoryClient(off_prompt=False)
        ]
    )

def handler(event: BaseEvent):
    if isinstance(event, StartPromptEvent):
        print("Prompt Stack Inputs:")
        for input in event.prompt_stack.inputs:
            print(f"{input.role}: {input.content}")
        print("Final Prompt String:")
        print(event.prompt)

agent = Agent(
    id="main_agent",
    # event_listeners=[EventListener(handler=handler, event_types=[StartPromptEvent])],
    logger_level=logging.DEBUG,
    config=model_config,
    rulesets=[
        Ruleset("main_agent", rules=[
            Rule("Your task is answering questions from users."),
        ]),
        agent_ruleset
    ],
    tools=[
        StructureRunClient(
            name="ResearchAgent",
            description="""An agent for researching information.
            The agent will answer questions on any topic.
            """,
            driver=LocalStructureRunDriver(structure_factory_fn=build_research_agent), 
            off_prompt=True
        ),
        TaskMemoryClient(off_prompt=False)
    ]
)

Chat(agent).start()