import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from audiorecorder import audiorecorder
from io import BytesIO
from download_youtube import *



load_dotenv()
client = OpenAI()



def inicializar():
    st.set_page_config(
        page_title="Trancrever Audios GPT",
        page_icon="🎙️",
        initial_sidebar_state="expanded",
    )
    
def pagina_principal():
    st.title("🎙️ Trancrever Audios GPT")
    tab1, tab2, tab3 = st.tabs(["Microfone", "Audio", "Vídeos"])
    escutar_microfone(tab1)
    ler_audio(tab2)
    ler_video(tab3)

def transcrever_audio(audio):

    transcricao = client.audio.transcriptions.create(
        model='whisper-1',
        file = audio,
        prompt="traga o texto de audio em formato Markdown",
        language='pt',
        response_format="text",
    )
    return transcricao

def ler_video(tab):
    with tab:
        st.markdown('')
        url = st.text_input("URL youtube:")
        st.markdown('## Audio Transcrito:')
        if url is not None:
            with st.spinner('Baixando o Audio...'):
                audio = download_youtube(url)
            if audio is not None:
                with st.spinner('Aguarde a transcrição...'):
                    texto = transcrever_audio(audio)
                st.markdown(texto)


def ler_audio(tab):
    with tab:
        st.markdown('')
        uploaded_file = st.file_uploader("arquivo de áudio:", accept_multiple_files=False, type=['mp3', 'wav'])
        st.markdown('## Audio Transcrito:')
        if uploaded_file is not None:
            with st.spinner('Aguarde a transcrição...'):
                texto = transcrever_audio(uploaded_file)
            st.markdown(texto)

def escutar_microfone(tab):
    with tab:
        st.markdown('')
        audio = audiorecorder("","")
        audioio = BytesIO()
        audioio.name = "audio.wav"
        st.markdown('## Audio Transcrito:')
        if len(audio) > 0:
        # To play audio in frontend:
            audio.export(audioio, format="wav")
            audioio.seek(0)
            texto = transcrever_audio(audioio)
            st.write(texto)

if __name__ == "__main__":
    inicializar()
    pagina_principal()