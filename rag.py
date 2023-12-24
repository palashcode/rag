from langchain import hub
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import JSONLoader
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import StrOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
import dotenv


class RagProcessor:
    def __init__(self, file_path):
        dotenv.load_dotenv()
        self.file_path = file_path
        self.docs = self.get_docs()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(self.docs)

        self.vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
        self.retriever = self.vectorstore.as_retriever()

        self.prompt = hub.pull("rlm/rag-prompt")
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
        self.rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def get_docs(self):
        try:
            if self.file_path.endswith(".pdf"):
                loader = PyPDFLoader(self.file_path)
            elif self.file_path.endswith(".json"):
                loader = JSONLoader(
                    file_path=f"{self.file_path}",
                    jq_schema='.[] | "question=\(.content) answer=\(.answer) explanation=\(.comment)"',
                    text_content=False)
            else:
                raise ValueError("Unsupported file format")
            docs = loader.load()
            return docs
        except Exception as e:
            raise ValueError(f"Error loading documents: {str(e)}")

    def format_docs(self,docs):
        try:
            return "\n\n".join(doc.page_content for doc in docs)
        except Exception as e:
            raise ValueError(f"Error formatting documents: {str(e)}")

    def get_answer(self, question):
        try:
            return self.rag_chain.invoke(question)
        except Exception as e:
            raise ValueError(f"Error getting answer: {str(e)}")

    def delete_vectorstore(self):
        try:
            self.vectorstore.delete_collection()
        except Exception as e:
            raise ValueError(f"Error deleting vectorstore: {str(e)}")
