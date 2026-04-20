from dotenv import load_dotenv
from pypdf import PdfReader
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document


def read_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    page = reader.pages[0]
    return page.extract_text()

def create_chunks(pdf_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=25)
    texts = text_splitter.split_text(pdf_text)
    return [Document(page_content=t) for t in texts]

def create_embeddings(text):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings.embed_query(text)

def create_vector_store(chunks):
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = Chroma(
        collection_name="pdf_collection",
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
    vector_store.add_documents(chunks)
    return vector_store

def main(question: str):
    pdf_text = read_pdf("pdf/sample.pdf")

    chunks = create_chunks(pdf_text)
    vector_store = create_vector_store(chunks)

    question_embedding = create_embeddings(question)
    results = vector_store.similarity_search_by_vector(
        question_embedding,
        k=2,
    )

    context = "\n\n".join([doc.page_content for doc in results])
    prompt = f"Use the context below to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}"

    model = init_chat_model("ollama:llama3.1")
    result = model.invoke(prompt)

    print(result.content)

main("What is the main topic of the document?")
