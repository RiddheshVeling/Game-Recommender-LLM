# Using Langchain and Gemini to build the Game Recommendation System

# Necessary Imports
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma


GOOGLE_API_KEY = "YOUR API KEY"

# Loading the game data consisting of 120 games
loader = CSVLoader("game_data.csv")
data = loader.load()

# Splitting the text which would be later passed for embeddings
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(data)

# Create vector embeddings for the dataset
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# Passing the data to the Chroma DB Vector Database
search = Chroma.from_documents(texts, embeddings)

from langchain.prompts import ChatPromptTemplate
# from langchain.chains import create_stuff_documents_chain, create_retrieval_chain

# Creating a custom Chat Prompt Template
prompt = ChatPromptTemplate([
    ("system", "You are a Game Recommendation System. Respond to the user queries accordingly and recommend up to 3 games."),
    ("user", "{input}\n\nContext: {context}")
])

# Chaining our LLM with the Prompt
chain = create_stuff_documents_chain(llm, prompt)

# Setting up our ChromaDb as the retriever
retriever = search.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, chain)

# Code for final response
response = retrieval_chain.invoke({"input": "Suggest some action games."})
print(response["answer"])