from dotenv import load_dotenv
from pypdf import PdfReader
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


def read_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    return page.extract_text()

def main(question: str):
    pdf_text = read_pdf("pdf/sample.pdf")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=25)
    chunks = text_splitter.split_text(pdf_text);

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vector_store = Chroma(
        collection_name="example_collection",
        embedding_function=embeddings,
    )
    vector_store.add_documents(chunks)

    model = init_chat_model("ollama:llama3.1")
    result = model.invoke(question)
    print(result.content)

main("What is the main topic of the document?")