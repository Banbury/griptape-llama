import requests
from schema import Schema, Literal
from attrs import define, field
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from griptape.artifacts import TextArtifact, ListArtifact, ErrorArtifact

@define
class SearxSearch(BaseTool):
    url : str = field(default="http://127.0.0.1:8080", kw_only=True)

    @activity(config={
        "description": "Can be used to search the web.",
        "schema": Schema({
            Literal(
                "query",
                description="Search query"
            ): str
        })
    })
    def generate(self, params: dict) -> ListArtifact | ErrorArtifact:
        result = requests.get(f"{self.url}/search?q={params['values'].get('query')}&format=json")
        if result.status_code == 200:
            return ListArtifact(
                [TextArtifact(str(result)) for result in result.json()["results"]]
            )
        else:
            return ErrorArtifact(
                result.reason
            )