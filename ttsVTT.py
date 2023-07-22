# https://betterprogramming.pub/how-to-integrate-chatgpt-with-voice-to-text-with-python-40300b8a77d1?gi=24e5d7b3c5de
# pip install playsound遇到问题时先试一下pip install --upgrade wheel
# pip install python-dotenv
import openai
import os
import sys
import playsound
import speech_recognition as sr
import streamlit as st

from typing import Text
from gtts import gTTS

# Set up the OpenAI API client
#openai.api_key = os.environ.get("OPEN_API_KEY")
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize the recognizer
r = sr.Recognizer()

def speak_chatgpt_text(text: str):

    # if you wish to use pyttsx3 import it first
    # Initialize pyttsx3 engine
    # engine = pyttsx3.init()
    # engine.setProperty('rate', 125)
    # engine.say(command)
    # engine.runAndWait()

    # Initialize gTTS engine
    lang_accent = 'com.au'
    filename = "tmp.mp3"
    tts = gTTS(text, tld=lang_accent)
    tts.save(filename)
    st.audio(filename)
#    playsound.playsound(filename)
    os.remove(filename)


def ask_chatgpt(prompt: str) -> Text:
    chat_gpt3_model_engine = "text-davinci-003"
    results = []
    # Generate a streamed response
    for resp in openai.Completion.create(engine=chat_gpt3_model_engine, prompt=prompt, max_tokens=512, n=1, stop=None, temperature=0.5, stream=True, ):
        text = resp.choices[0].text
        results.append(text)
        sys.stdout.write(text)
        sys.stdout.flush()

    return "".join(results)


def main():
    while True:
        # Exception handling to handle exceptions at runtime if
        # no user prompt given
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                print("Microphone is open now say your prompt...")
                # wait for a second to let the recognizer
                # adjust the energy threshold cbased on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)

                # listens for the user's input
                audio2 = r.listen(source2)

                # Using google to recognize audio
                my_prompt = r.recognize_google(audio2)
                my_prompt = my_prompt.lower()

                print("Did you say :", my_prompt)
                prompt_resp_text = ask_chatgpt(my_prompt)
                speak_chatgpt_text(prompt_resp_text)

        except Exception as e:
            print(e)
            print("Could not request results; {0}".format(e))


if __name__ == '__main__':

    configured_microphones = sr.Microphone.list_microphone_names()
    if configured_microphones:
        for index, name in enumerate(configured_microphones):
            print("Microphone with name \"{1}\" found for microphone(device_index{0})".format(index, name))
        main()
    else:
        print("No configured Microphones")