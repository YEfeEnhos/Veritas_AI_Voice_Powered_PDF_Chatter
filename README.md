# Voice activated multi-language chatbot on multiple pdf documents 
A ChatGTP-like search experince on multiple personal uploaded pdf documents that supports multiple languages brought by OpenAI's ada model supporting real time voice input powered by AssemblyAI's api
- - - -
# Introduction:
The chatbot App is a versatile Python application that not only enables you to chat with multiple PDF documents but also boasts voice activation and multi-language support. With this app, you can ask questions about the PDFs using natural language or simply use your voice to interact with the documents. The application will provide relevant responses based on the content of the loaded PDFs, making it a seamless and inclusive tool for a wide range of users. Please note that the app will exclusively respond to questions related to the loaded PDFs, and it's designed to understand and respond in multiple languages for your convenience.
- - - -
# How it works 
- - - -
<details>
           
<summary>     
# Dependencies Instalation
</summary>
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
</details>
- - - -
# Usage 
## To run the voice activated chatbot on your local device follow the steps below:
1. Run the `ask.py` file using the Streamlit CLI. Execute the following command:
```bash
streamlit run ask.py
```
2. The application will launch in your default web browser, displaying the user interface.
3. Load multiple PDF documents into the app by clicking on the `Load Documents` button appearing on the sidebar.
4. Click on the `Process` button to vectorize your PDF.
5. Ask questions in natural language about the loaded PDFs using the chat interface or click the `Start` button to start audio recording and click the `Stop` button to finish recording. The recorded audio file will automatically get converted into text and query the documents provided.
- - - -
# Note
The current app is specifically desing for ease of deployment and hence allows users to upload data rather than the need for setting up a vector database. A free-tier pinecone vector database can be implement. The schema below shows a flow-cart of how that would look like:
