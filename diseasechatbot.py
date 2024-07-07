from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import os
import get_password
import re
os.environ["OPENAI_API_KEY"] = get_password.getpass()


class DiseaseChatbot:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        # text_splitter = RecursiveCharacterTextSplitter(
        #     chunk_size=500, chunk_overlap=200)
        # folder = "C:\\Users\\User\\Desktop\\CCdiary-python\\mentaldata"
        # doc_loader = DirectoryLoader(folder, glob="*.docx", loader_cls=UnstructuredWordDocumentLoader)
        # doc_documents = doc_loader.load()
        # texts = text_splitter.split_documents(doc_documents)
        # vector_store = FAISS.from_documents(texts, self.embeddings)
        # vector_store.save_local("C:\\Users\\User\\Desktop\\CCdiary-python\\mentaldata\\faiss_index")
        vector = FAISS.load_local("C:\\Users\\User\\Desktop\\CCdiary-python\\mentaldata\\faiss_index"
                                  , self.embeddings, allow_dangerous_deserialization=True)
        self.retriever = vector.as_retriever(search_type="similarity", search_kwargs={"k": 2})
        system_prompt = (
            "Use the following pieces of retrieved context to answer "
            "the question."
            "\n\n"
            "{context}"
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
                ("system", "If the question is not relevant to the context or you don't know the answer."),
                ("system", "just answer 'The question is not in my scope'"),
                ("system", "You should answer the question in gentle and friendly tone."),
                ("system", "Answer question to the best of your ability in {language}"),
            ]
        )
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        self.chain = create_retrieval_chain(self.retriever, question_answer_chain)

    def get_answer(self, input_text,language):
        response = self.chain.invoke(
            {"input": input_text,
             "language": language}
           )
        response = re.sub(r'\n+', '\n', response['answer'])
        response = response.replace('*', '')
        return response





