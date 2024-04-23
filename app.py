from flask import Flask, render_template, request
from dotenv import load_dotenv
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate

from GPTModels.LLMFactory import LLMFactory

load_dotenv()
app = Flask(__name__)
model_factory = LLMFactory()

@app.route("/")
def home() :
    return render_template("index.html")


@app.route("/chatbot", methods={"POST"})
def chatbot() :
    user_input = request.form['message']
    LLM = request.form.get('model_type', 'openai')
    version = request.form.get('model_name', None)  

    
    model = model_factory.get_model(LLM, version)

    docs = load_and_split_documents()
    retrieved_docs = assess_relevance(user_input, docs)
    bot_response = decide_and_respond(user_input, retrieved_docs, model)
    return render_template("chatbot.html", user_input=user_input, bot_response=bot_response)




# Document loading and splitting
def load_and_split_documents(directory="data"):
    document_loader = PyPDFDirectoryLoader(directory)
    docs = document_loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    split_docs = text_splitter.split_documents(docs)
    return split_docs

def assess_relevance(question, docs):
    vectorstore = Chroma.from_documents(documents=docs, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    retrieved_docs = retriever.invoke(question)
    return retrieved_docs

# Relevance assessment function using a grading prompt
def is_content_relevant(question, context_text, model):
    grader_prompt = f"""
    You are a grader assessing the relevance of a retrieved document to a user question.
    If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant.
    Give a python value True or False to indicate whether the document is relevant to the question. 
    True if the the document is relevant to the question else False

    Retrieved document: {context_text}

    -----
    
    User question: {question}
    """

    relevant = model.generate_response(grader_prompt)
   
    return relevant

# Adaptive RAG and direct response logic
def decide_and_respond(question, retrieved_docs, model):
    context_text = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
    if not context_text.strip():
        return generate_direct_response(question, model)
    if is_content_relevant(question, context_text, model) == 'True':
        return generate_RAG_response(question, context_text, model)
    return generate_direct_response(question, model)

def generate_direct_response(question, model):
    print(question)
    return model.generate_response(question)
   

def generate_RAG_response(question, context, model):
    prompt = ChatPromptTemplate.from_template("""
    Answer the question based only on the following context: {context}
    ---
    Answer the question based on the above context: {question}
    """).format(context=context, question=question)
    
    return model.generate_response(prompt)


