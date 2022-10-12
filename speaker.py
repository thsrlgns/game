from pickle import TRUE
import time, os 
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound



def listen(recognizer, audio):
    try:
        text=r.recognize_google(audio, language='ko')
        print('[나]'+text)
        answer(text)
    except sr.UnknownValueError:
        print('인식실패')
    except sr.RequestError:
        print('요청실패')    


def answer(input_text):
    answer_text=''
    if '안녕' in input_text:
        answer_text='안녕하세요? 반갑습니다.'
    elif '예진' in input_text:
        answer_text='성별은 여자이고 나이는 24살입니다'
    elif '기훈' in input_text:
        answer_text='안녕하세요? 반갑습니다.'
    elif '날씨' in input_text:
        answer_text='오늘 기온은 20도이고 맑습니다.'
    elif '고마워' in input_text:
        answer_text='별 말씀을요'
    elif '종료' in input_text:
        answer_text='다음에 또 봐요'
        stop_listening(wait_for_stop=False)
    else:
        answer_text='다시 한번 말씀해주시겠어요?'
    speak(answer_text)


def speak(text):
    print('[인공지능]'+ text)
    file_name='voice.mp3'
    tts=gTTS(text=text, lang='ko')
    tts.save(file_name)
    playsound(file_name)
    if os.path.exists(file_name):
        os.remove(file_name)


r=sr.Recognizer()
m=sr.Microphone()


speak('무엇을 도와드릴까요')
stop_listening= r.listen_in_background(m,listen)

while True:
    time.sleep(0.1)

