#initial import of libraries 
import streamlit as st
from dotenv import load_dotenv
import websockets
import asyncio
import base64
import json
import pyaudio
from configure import api_key
import os
from pathlib import Path
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub

#set variable that stores audio to default ("Listening...")
#set session_state["run"]= False => the mic is not recording 
if "text" not in st.session_state:
    st.session_state["text"] = "Listening..."
    st.session_state["run"] = False
#become true when document is uploaded
def uploaded():
    st.session_state.upload = True
#set session_state["run"] = True => the mic is recording 
def start_listening():
    st.session_state["run"] = True

#testing function allowing for the download of transcription.txt file 
#no longer in use 
def download_transcription():
    read_txt = open('transcription.txt', 'r')
    st.download_button(
		label="Download transcription",
		data=read_txt,
		file_name='transcription_output.txt',
		mime='text/plain')
	
#set session_state["run"]= False => the mic is not recording 
def stop_listening():
    st.session_state["run"] = False

#Setting values for stream variables
FRAMES_PER_BUFFER =  3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

# Open an audio stream with above parameter settings
stream = p.open(
   format=FORMAT,
   channels=CHANNELS,
   rate=RATE,
   input=True,
   frames_per_buffer=FRAMES_PER_BUFFER
)


async def send_receive():
	URL = f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={RATE}"

	print(f'Connecting websocket to url ${URL}')
	
	#websocet instantiated
	async with websockets.connect(
		URL,
		extra_headers=(("Authorization", st.secrets['api_key']),),
		ping_interval=5,
		ping_timeout=20
	) as _ws:

		r = await asyncio.sleep(0.1)
		print("Receiving messages ...")

		session_begins = await _ws.recv()
		print(session_begins)
		print("Sending messages ...")

		#send request to Assembly AI API
		async def send():
			while st.session_state['run']:
				try:
					data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow = False)
					
					#convert voice recording to base 64
					data = base64.b64encode(data).decode("utf-8")
					
					#convert base 64 to JSON
					json_data = json.dumps({"audio_data":str(data)})
					
					r = await _ws.send(json_data)

				except websockets.exceptions.ConnectionClosedError as e:
					print(e)
					assert e.code == 4008
					break

				except Exception as e:
					print(e)
					assert False, "Not a websocket 4008 error"

				r = await asyncio.sleep(0.01)

		#JSON filed recieved from API
		async def receive():
			while st.session_state['run']:
				try:
					result_str = await _ws.recv()
					#Convert returned JSON to txt
					result = json.loads(result_str)['text']

					if json.loads(result_str)['message_type']=='FinalTranscript':
						print(result)
						st.session_state['text'] = result
						st.write(st.session_state['text'])
						
						#Create transcription.txt file 
						transcription_txt = open('transcription.txt', 'a')
						transcription_txt.write(st.session_state['text'])
						transcription_txt.write(' ')
						transcription_txt.close()


				except websockets.exceptions.ConnectionClosedError as e:
					print(e)
					assert e.code == 4008
					break

				except Exception as e:
					print(e)
					assert False, "Not a websocket 4008 error"
			
		send_result, receive_result = await asyncio.gather(send(), receive())
                    
#convert pdf files to txt
def get_pdf_text(pdf_docs):
    #empty sting 
    text = ""
    #iterate the list 
    for pdf in pdf_docs:
        #convert each document to pages
        pdf_reader = PdfReader(pdf)
        #covert each page to text 
        for page in pdf_reader.pages:
            text += page.extract_text()
    #string 
    return text


def get_text_chunks(text):
    #longchain --> non-reccursive text spliter 
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    #generate chunks of 1000 characters from the text 
    
    chunks = text_splitter.split_text(text)
    #list 
    return chunks


def get_vectorstore(text_chunks):
    
    #comment and uncomment to select which enviroment to use 
    embeddings = OpenAIEmbeddings() 
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") 
    #hugging face => free to use but rate limited 
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    #turn embeding into vectors 
    
    return vectorstore


        

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm,retriever=vectorstore.as_retriever(),memory=memory)
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    
    
    

    for i, message in reversed(list(enumerate(st.session_state.chat_history))):
        #decide if its users turn or the bots turn 
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

 

def main():
    load_dotenv()
    st.set_page_config(page_title="Uber ChatBot")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "upload" not in st.session_state:
        st.session_state.upload = False

    st.header("Uber Voice Activated ChatBot")
   
    user_question = st.text_input("Ask a question to UberAI:")

    st.subheader("Voice your question:")
       
    
    col1, col2 = st.columns(2)

    col1.button('Start :microphone:', on_click=start_listening)
    col2.button('Stop', on_click=stop_listening)
    
    asyncio.run(send_receive())

    #If transcription.txt exists set user_question to the String stored in the txt file
    if Path('transcription.txt').is_file():
        read_txt = open('transcription.txt', 'r')
        user_question = read_txt.read()
        os.remove('transcription.txt')
   
   #If user_question has any value either from the text or audio input start querying
    if user_question:
	#if PDF files are uploaded generate response 
        if st.session_state.upload:
         handle_userinput(user_question)
	#if PDF files are not uploaded generate error message 
        else:
         error_message = '<p style="font-family:sans-serif; color:Red; font-size: 42px;">Please process documents first!</p>'
         st.markdown(error_message, unsafe_allow_html=True)
    with st.sidebar:
        
        st.subheader("Your documents")
        #recieve a list filed with pdf files 
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
		uploaded()
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)




if __name__ == '__main__':
    main()
