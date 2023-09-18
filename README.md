<img width="1436" alt="Screen Shot 2023-09-17 at 04 26 05" src="https://github.com/YEfeEnhos/UGH_Coding_RC_App_Development_Team/assets/91611406/9ee164f6-b54c-4f3d-977f-1390a949f8f2">

# Voice activated multi-language chatbot on multiple pdf documents 
A ChatGTP-like search experince on multiple personal uploaded pdf documents that supports multiple languages brought by OpenAI's ada model supporting real time voice input powered by AssemblyAI's api
- - - -
# Introduction:
The chatbot App is a versatile Python application that not only enables you to chat with multiple PDF documents but also boasts voice activation and multi-language support. With this app, you can ask questions about the PDFs using natural language or simply use your voice to interact with the documents. The application will provide relevant responses based on the content of the loaded PDFs, making it a seamless and inclusive tool for a wide range of users. Please note that the app will exclusively respond to questions related to the loaded PDFs, and it's designed to understand and respond in multiple languages for your convenience.
- - - -
# How it works 
![PDF-LangChain](https://github.com/YEfeEnhos/UGH_Coding_RC_App_Development_Team/assets/91611406/f4d78600-1acb-4cfd-b5e3-a5437d33431d)
## The application follows these steps to provide responses to your questions:
1. PDF Loading: The app reads multiple PDF documents and extracts their text content.
2. Text Chunking: The extracted text is divided into smaller chunks that can be processed effectively.
3. Language Model: The application utilizes a language model to generate vector representations (embeddings/locations in a x dimentional plane) of the text chunks. These chunks can either be temporarly stored (as this application does), or be stored in a vectore database (such as pinecone).
4. Similarity Matching: When you ask a question, the app compares it with the text chunks and identifies the most semantically similar ones (based on cosine similarity matrix, basically closest neighbor in the vector database).
5. Response Generation: The selected chunks are passed to the language model, which generates a response based on the relevant content of the PDFs (OpenAI LLM).
## The application follows these steps to get voice queries 
1. Pyaudio Instance: Stream parameteres such as `FRAMES_PER_BUFFER`, `FORMAT`, `CHANNELS`, and `RATE` are set to open a audio stream that stores input voice when `session.state` is `True`.
2. Web Socket: Utilizing our AssemblyAI `api_key` we instantiate a web-socket linked to AssemblyAI's API.
3. Conversion to Json: Collected audio file is then converted to base64 to then get converted into JSON, which is the format AssemblyAI's API expects the API request to take.
4. Display Text: While the user speaks the text is displayed on the screen, the AI is not prone to minor misspleings or illogical sentence structures, so if the user sees that tehir speech is interpreted differently they can repeat their sentence.
5. Conversion to .txt: After the user clicks `Stop` in other words `session.state` is `False`, AssemblyAI sends a JSON which we convert and compress it to a .txt file named `transcription.txt`. This is to avoid empty chracters generated when the user takes a second to breath or talks slowly. This wasy the data is regulated.
6. Querying: Via Path module from pathlib the system checks if `transcription.txt` exists. If it does, the system reads the file and sets the variable `user_question` to `transcription.txt`'s String content. This is then automatically asked to the chatbot which works as described above.
- - - -         
# Dependencies Instalation
## To install the dependencies and provide required information for the chatbot to run on your local device follow the steps below:
1. Clone the repository to your local machine 
2. Pip install required packages to the python enviroment you will run the code on:
```bash
pip install -r requirements.txt
```
 If you run into problems trying to pip install the pyaudio, first:
```bash
brew install portaudio
```
 Then run the previous script again. 
 
 3. Obtain an API key from OpenAI and add it to the .env file in the project directory.
 ```.env
OPENAI_API_KEY=your-openai-api-key
```
4.  Obtain an API key from AssemblyAPI and add it to the .streamlit/secrets.toml and configure.py file in the project directory.
 ```python
api_key = "your-assemblyai-api-key"
```
- - - -
# Usage 
## To run the voice activated chatbot on your local device follow the steps below:
1. Run the `ask.py` file using the Streamlit CLI. Execute the following command:
```bash
streamlit run ask.py
```
2. The application will launch in your default web browser, displaying the user interface.
3. Load multiple PDF documents into the app by clicking on the `Browse Documents` button appearing on the sidebar.
4. Click on the `Process` button to vectorize your PDF. Querying before processing any PDF files will result in a error.
5. Ask questions in natural language about the loaded PDFs using the chat interface or click the `Start` button to start audio recording and click the `Stop` button to finish recording. The recorded audio file will automatically get converted into text and query the documents provided.
- - - -
# Note
The current app is specifically desing for ease of deployment and hence allows users to upload data rather than the need for setting up a vector database. A free-tier pinecone vector database can be implement. The schema below shows a flow-cart of how that would look like:
![gpt-langchain-pdf](https://github.com/YEfeEnhos/UGH_Coding_RC_App_Development_Team/assets/91611406/d1eaa0c9-755f-4c90-9007-050b8b7cc7a8)
If you have any questions regarding this process feel free to contact me at _+90 542 830 07 66_ or enhyig.25@robcol.k12.tr
- - - -
# Related Documentations/Sources
https://platform.openai.com/docs/guides/embeddings/what-are-embeddings

https://www.assemblyai.com/docs/
