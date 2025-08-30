# 🤖 Urdu/English Voice Assistant

A versatile voice and text-based chatbot powered by Google's Gemini 1.5 Flash model. This application provides a seamless conversational experience, allowing users to interact in either Urdu or English through a user-friendly Gradio web interface.

### Created by **Noman Amjad**

---

## ✨ Features

- **Dual-Mode Interaction:** Switch between a traditional text-based chat and a hands-free voice conversation.
- **Bilingual Support:** Fluent in both Urdu and English. The assistant recognizes the language and responds accordingly.
- **Real-Time Speech-to-Text:** Utilizes Google's speech recognition engine to accurately transcribe your voice commands.
- **Natural Text-to-Speech:** Generates clear and natural-sounding voice responses using Google's Text-to-Speech (gTTS) service.
- **Powered by Gemini:** Leverages the speed and power of the `gemini-1.5-flash` model for intelligent and context-aware responses.
- **Secure API Key Handling:** Your Gemini API key is managed securely within the session and is not exposed.
- **Easy to Deploy:** Includes configuration files for straightforward deployment on platforms like Hugging Face Spaces.

---

## 🚀 How It Works

The application follows a simple yet powerful workflow:

1.  **Input:** The user provides a Gemini API key and then either types a message or records audio using the microphone.
2.  **Processing (Voice Mode):**
    *   The recorded audio is sent to the `SpeechRecognition` library.
    *   The library transcribes the audio into text, specifically configured for Urdu (`ur-PK`).
3.  **AI Generation:**
    *   The user's text prompt (either typed or transcribed) is sent to the Google Gemini API along with the conversation history.
    *   The Gemini model generates a relevant and contextual response.
4.  **Output:**
    *   **Text Mode:** The response is displayed directly in the chat window.
    *   **Voice Mode:** The `langdetect` library identifies the language of the response. The text is then converted into an audio file using `gTTS`, which is played back automatically to the user.

---

## 🛠️ Setup and Installation

Follow these steps to run the project on your local machine.

### 1. Prerequisites

You need to have the following system-level dependencies installed.

- **For Debian/Ubuntu-based systems:**
  ```bash
  sudo apt-get update
  sudo apt-get install -y portaudio19-dev ffmpeg
  ```
- **For other operating systems:** Install the equivalent packages for PortAudio and FFmpeg.

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/voice-chatbot-updated-hf.git
cd voice-chatbot-updated-hf
```

### 3. Set Up a Python Environment

It is recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 4. Install Dependencies

Install all the required Python packages.

```bash
pip install -r requirements.txt
```

### 5. Get Your API Key

- You need a Google Gemini API key. You can obtain one from the [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## ▶️ How to Run

Once the setup is complete, you can launch the Gradio application with the following command:

```bash
python app.py
```

Open your web browser and navigate to the local URL provided (usually `http://127.0.0.1:7860`). Enter your Gemini API key in the designated field to start chatting.

---

## 📁 Project Structure

Here is an overview of the key files in this project:

```
.
├── .env              # Example environment file (not used directly by app.py)
├── app.py            # Main application script containing all logic and the Gradio UI
├── packages.txt      # System-level dependencies for Hugging Face Spaces
├── requirements.txt  # Python package dependencies
└── README.md         # This file
```

---

## ☁️ Deployment

This project is ready for deployment on [Hugging Face Spaces](https://huggingface.co/spaces).

1.  Create a new **Gradio SDK** Space on Hugging Face.
2.  Upload all the files from this repository.
3.  The `packages.txt` file will automatically instruct the Hugging Face platform to install the necessary system dependencies (`portaudio19-dev` and `ffmpeg`).
4.  The `requirements.txt` file will be used to install the Python packages.
5.  Your application will be live and ready to use!
