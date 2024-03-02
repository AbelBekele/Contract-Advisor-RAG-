# File: my_llama_index.py

from llama_index.llms.openai import OpenAI
from llama_index.core.schema import MetadataMode
from llama_index.core import SimpleDirectoryReader
import nest_asyncio
from dotenv import load_dotenv
import os
from llama_index.core.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor,
    KeywordExtractor,
    BaseExtractor,
)
from llama_index.extractors.entity import EntityExtractor
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.question_gen import LLMQuestionGenerator
from llama_index.core.question_gen.prompts import DEFAULT_SUB_QUESTION_PROMPT_TMPL

nest_asyncio.apply()

class Metadata_extraction:
    def __init__(self, document_path):
        load_dotenv(override=True)
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        self.llm = OpenAI(temperature=0.0, model="gpt-3.5-turbo", max_tokens=512)
        self.text_splitter = TokenTextSplitter(
            separator=" ", chunk_size=512, chunk_overlap=128
        )
        self.document_path = document_path
        self._configure_pipeline()

    def _configure_pipeline(self):
        extractors = [
            TitleExtractor(nodes=5, llm=self.llm),
            KeywordExtractor(keywords=10, llm=self.llm),
        ]
        transformations = [self.text_splitter] + extractors
        self.pipeline = IngestionPipeline(transformations=transformations)

    def run_llama_index(self):
        contract_doc = SimpleDirectoryReader(input_files=[self.document_path]).load_data()
        contract_nodes = self.pipeline.run(documents=contract_doc)
        return contract_nodes

    def generate_questions(self, prompt_template):
        question_gen = LLMQuestionGenerator.from_defaults(
            llm=self.llm,
            prompt_template_str=prompt_template + DEFAULT_SUB_QUESTION_PROMPT_TMPL,
        )
        # Add your logic to generate questions here
        # ...

# Example usage:
# my_llama_index = MyLlamaIndex(document_path="../data/Robinson_Advisory.pdf")
# nodes = my_llama_index.run_llama_index()
# questions = my_llama_index.generate_questions("Your custom prompt: ")
