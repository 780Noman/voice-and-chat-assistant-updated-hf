import gradio as gr
import speech_recognition as sr
from gtts import gTTS
import tempfile
import google.generativeai as genai
from langdetect import detect
import os

# --- Configure Generative AI ---
def configure_genai(api_key):
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-1.5-flash"), None
    except Exception as e:
        return None, f"Failed to configure Generative AI: {e}"

# --- Speech Recognition ---
def recognize_audio(audio_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="ur-PK")
            return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results; {e}"
    except Exception as e:
        return f"Error during recognition: {e}"

# --- Generate AI Response ---
def generate_response(model, history):
    try:
        response = model.generate_content(history)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

# --- Text-to-Speech ---
def text_to_speech(text, lang="ur"):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts = gTTS(text=text, lang=lang)
            tts.save(fp.name)
            return fp.name
    except Exception:
        return None

# --- Chat Logic ---
def chat_with_model(message, history, api_key):
    if not api_key:
        return history + [[message, "Please enter your Gemini API key."]]

    model, error_msg = configure_genai(api_key)
    if error_msg:
        return history + [[message, error_msg]]

    history = history or []
    history.append([message, None])

    # Convert history to Gemini format
    messages = []
    for i, pair in enumerate(history):
        if pair[0]:
            messages.append({"role": "user", "parts": [pair[0]]})
        if pair[1]:
            messages.append({"role": "model", "parts": [pair[1]]})

    response = generate_response(model, messages)
    history[-1][1] = response
    return history

# --- Voice Chat Logic ---
def voice_chat_with_model(audio_path, history, api_key):
    if not api_key:
        return history + [[None, "Please enter your Gemini API key."]], None

    model, error_msg = configure_genai(api_key)
    if error_msg:
        return history + [[None, error_msg]], None

    if audio_path is None:
        return history, None

    user_text = recognize_audio(audio_path)
    if user_text.startswith("Sorry") or user_text.startswith("Could not request") or user_text.startswith("Error"):
        return history + [[None, user_text]], None

    history = history or []
    history.append([user_text, None])

    messages = []
    for i, pair in enumerate(history):
        if pair[0]:
            messages.append({"role": "user", "parts": [pair[0]]})
        if pair[1]:
            messages.append({"role": "model", "parts": [pair[1]]})

    response = generate_response(model, messages)
    history[-1][1] = response

    # Detect language for TTS
    try:
        lang = detect(response)
    except:
        lang = "en"
    audio_output_path = text_to_speech(response, lang=lang)

    return history, audio_output_path

# --- Gradio Interface ---
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Urdu/English Voice Assistant")
    gr.Markdown("### Created by **Noman Amjad**")

    api_key_input = gr.Textbox(label="Gemini API Key", type="password", placeholder="Enter your Gemini API key")

    with gr.Tab("Chat Mode"):
        chatbot = gr.Chatbot()
        msg = gr.Textbox(label="Type your message")
        clear = gr.Button("Clear Chat")

        msg.submit(chat_with_model, [msg, chatbot, api_key_input], chatbot)
        clear.click(lambda: None, None, chatbot, queue=False)

    with gr.Tab("Voice Mode"):
        voice_chatbot = gr.Chatbot()
        audio_input = gr.Audio(source="microphone", type="filepath", label="🎤 Speak now")
        voice_clear = gr.Button("Clear Voice Chat")
        audio_output = gr.Audio(label="Assistant's Voice", autoplay=True)

        audio_input.change(voice_chat_with_model, [audio_input, voice_chatbot, api_key_input], [voice_chatbot, audio_output])
        voice_clear.click(lambda: None, None, voice_chatbot, queue=False)

demo.launch()
