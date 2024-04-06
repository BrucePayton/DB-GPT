"""from dbgpt.rag.embedding import DefaultEmbeddingFactory

embeddings = DefaultEmbeddingFactory.remote(
  api_url="http://localhost:8100/api/v1/embeddings",
  api_key="{your_api_key}",
  model_name="text2vec"
)"""

"""from dbgpt.rag.chunk_manager import ChunkManager, ChunkParameters
from dbgpt.rag.knowledge.factory import KnowledgeFactory
from dbgpt.rag.knowledge.base import KnowledgeType, ChunkStrategy

# get a knowledge object
knowledge_factory = KnowledgeFactory()
# import the pdf.file as document knowledge
document_path = r"D:\Research\AGI\2312.17449_db_gpt_paper.pdf"
document_knowledge = knowledge_factory.create(datasource=document_path, knowledge_type=KnowledgeType.DOCUMENT)

# Now we get chunks, we can do the inverted Indexing
# Now we embedding this chunk, and go on see what will happen
from dbgpt.rag.embedding.embedding_factory import DefaultEmbeddingFactory
embedding_model = DefaultEmbeddingFactory.default(r"D:\Developer\Projects\pythonProject\reference_project\DB-GPT\DB-GPT\models\m3e-large")
# now we get an embedding model in our projects'default
# we want to embedding chunks first
from dbgpt.rag.operators import EmbeddingAssemblerOperator, KnowledgeOperator
from dbgpt.storage.vector_store.chroma_store import ChromaVectorConfig
from dbgpt.storage.vector_store.connector import VectorStoreConnector

knowledge_vector_connector = VectorStoreConnector.from_default(
    "Chroma",
    vector_store_config = ChromaVectorConfig(
        name="test_vstore",
        persist_path="/tmp/awel_rag_test_vector_store",
    ),
    embedding_fn=embedding_model
)

paper_chunk_parameters = ChunkParameters(chunk_strategy="CHUNK_BY_PARAGRAPH")

knowledge_embedding_assembler = EmbeddingAssemblerOperator(
    vector_store_connector=knowledge_vector_connector,
    chunk_parameters=paper_chunk_parameters
)

embedding_chunks = knowledge_embedding_assembler.assemble(document_knowledge)
print(len(embedding_chunks))"""

import asyncio

from dbgpt.model.proxy import OpenAILLMClient
from dbgpt.rag.retriever import QueryRewrite
from dbgpt.model.proxy import ZhipuLLMClient
input_api_key = "f8ff53a807d498950d68917ade0ed7bd.WL6AQUrmzxzaEnNj"
llm_client = ZhipuLLMClient(api_key=input_api_key)

async def main():
    query = "compare steve curry and lebron james"
    reinforce = QueryRewrite(
        llm_client=llm_client,
        model_name="gpt-3.5-turbo",
    )
    return await reinforce.rewrite(origin_query=query, nums=1)


if __name__ == "__main__":
    output = asyncio.run(main())
    print(f"output: \n\n{output}")

from dbgpt.core import(
    ChatPromptTemplate,
    HumanPromptTemplate,
    SystemPromptTemplate,
    SQLOutputParser
)