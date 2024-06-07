from transformers import AutoTokenizer
from griptape.drivers import OpenAiChatPromptDriver, OpenAiEmbeddingDriver, LocalVectorStoreDriver, DummyAudioTranscriptionDriver, DummyImageGenerationDriver, DummyImageQueryDriver, DummyTextToSpeechDriver
from griptape.tokenizers import HuggingFaceTokenizer
from griptape.config import BaseStructureConfig

class LMStudioConfig(BaseStructureConfig):
    def __init__(self, base_url="http://127.0.0.1:1234/v1"):
        tokenizer = HuggingFaceTokenizer(
            tokenizer=AutoTokenizer.from_pretrained("NousResearch/Meta-Llama-3-8B-Instruct"),
            max_output_tokens=1024,
        )

        prompt_driver=OpenAiChatPromptDriver(
            model="llama3:8b-instruct-q8_0",
            base_url=base_url,
            api_key="ollama",
            tokenizer=tokenizer,
            temperature=0.2,
            max_attempts=5
        )

        embedding_driver = OpenAiEmbeddingDriver(
            model="nomic-ai/nomic-embed-text-v1.5",
            base_url=base_url,
            api_key="whatever",
            tokenizer=tokenizer
        )

        super().__init__(
            prompt_driver=prompt_driver, 
            embedding_driver=embedding_driver,
            vector_store_driver=LocalVectorStoreDriver(embedding_driver=embedding_driver),
            image_generation_driver=DummyImageGenerationDriver,
            image_query_driver=DummyImageQueryDriver,
            text_to_speech_driver=DummyTextToSpeechDriver,
            audio_transcription_driver=DummyAudioTranscriptionDriver
        )
