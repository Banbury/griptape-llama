import mesop as me
import mesop.labs as mel

from searx import SearxAgent

agent = SearxAgent()

@me.page(path="/")
def app():
    with me.box(style=me.Style(margin=me.Margin.all(32))):
        mel.chat(transform, title="Chat", bot_user="Assistant")

def transform(input: str, history: list[mel.ChatMessage]):
    res = agent.run(input)
    yield res.output_task.output.value