import speech_recognition as sr
import win32com.client
import webbrowser
import openai
import pyaudio
import os
from _datetime import datetime
import cv2
from config import apikey
import random

def say(text):
    speaker = win32com.client.Dispatch('SAPI.SpVoice')
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 0.5
        r.energy_threshold = 200
        audio = r.listen(source)
        try:
            print('Recognising...')
            query = r.recognize_google(audio, language='en-in')
            print(f'user said :{query}')
            return query
        except Exception as e:
            return 'cannot recognize your voice'

def capture_picture():
    cam_port = 0
    while True:
        cam = cv2.VideoCapture(cam_port)
        result, image = cam.read()

        if result:
            cv2.putText(image, 'press s to capture', (100,100), cv2.FONT_HERSHEY_PLAIN, 3,(0,0,255),2)
        else:
            print("No image detected. Please! try again")
        cv2.imshow('smileeee', image)
        a = cv2.waitKey(1)
        if (a == ord('s')):
            cv2.imwrite("picture.png", image)
        elif(a == ord('q')):
            break
    cam.release()
    cv2.destroyWindow('smileeee')

def gpt(prompt):
    openai.api_key = apikey
    text = f'Chatgpt response for - {prompt} \n ------------------------- \n\n'
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response['choices'][0]['text'])

    text += response['choices'][0]['text']
    if not os.path.exists('Openai'):
        os.mkdir('Openai')
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)

chatStr=''

def chat(prompt):
    openai.api_key = apikey
    global chatStr
    print(chatStr)
    chatStr += f'Nidhi: {prompt}\nJarvis: '
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response['choices'][0]['text'])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response['choices'][0]['text']

if __name__ == '__main__':
    say('hello I am jarvis A I')
    while True:
        print('Listening....')
        query = takeCommand()
        if 'drop my needle'.lower() in query.lower():
            say('On It!')
            # webbrowser.open('https://youtu.be/Xv17jj9BhEg?t=3')
            music_path = "AC_DC-Back in black ringtone.mp3"
            os.startfile(music_path)
            # quit()
        elif 'the time'.lower() in query.lower():
            strfTime = datetime.now().strftime('%H:%M')
            say(f'The time is {strfTime}')
        elif 'click a picture'.lower() in query.lower():
            capture_picture()
        elif 'using artificial intelligence'.lower() in query.lower():
            gpt(prompt=query)
        elif 'Jarvis Quit'.lower() in query.lower():
            exit()
        elif 'reset chat'.lower() in query.lower():
            chatStr=''
        # say(query)
        else:
            print('chatting....')
            chat(query)






