# Voice activated multi-language chatbot on multiple pdf documents 
## A ChatGTP-like search experince on multiple personal uploaded pdf documents that supports multiple languages brought by OpenAI's ada model supporting real time voice input powered by AssemblyAI' api

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
# Usage 
## To run the voice activated chatbot on your local device follow the steps below:
1. Run the `ask.py` file using the Streamlit CLI. Execute the following command:
```bash
streamlit run ask.py
```
2. The application will launch in your default web browser, displaying the user interface.
3. Load multiple PDF documents into the app by clicking on the `Load Documents` button appearing on the sidebar.
4. Ask questions in natural language about the loaded PDFs using the chat interface or click the `Start` button to start audio recording and click the `Stop` button to finish recording. The recorded audio file will automatically get converted into text and query the documents provided.

