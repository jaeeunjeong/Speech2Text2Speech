import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import time
from googletrans import Translator

# Translator 객체 초기화
translator = Translator()

# Recognizer 객체 초기화
r = sr.Recognizer()

# 마이크 객체 초기화
m = sr.Microphone()


async def listen():
    """음성을 듣고 텍스트로 변환하는 함수"""
    try:
        with m as source:
            print("듣고 있습니다...")
            r.adjust_for_ambient_noise(source)  # 주변 소음에 맞게 조정
            audio = r.listen(source)  # 마이크로부터 음성 듣기
            print("음성을 인식 중입니다...")
            text = r.recognize_google(audio, language='ko')  # 구글 음성 인식 API로 텍스트로 변환
            print(f"입력된 문장: {text}")
            if '사용 중단' in text:
                print("서비스 종료")
                exit()
            await answer(text)  # 비동기적으로 answer 함수 호출
    except sr.UnknownValueError:
        print("음성 인식 실패")
    except sr.RequestError as e:
        print(f"요청 실패: {e}")


async def answer(input_text):
    """입력된 텍스트에 답변하는 함수"""
    translator_text = await translate_to_english(input_text)  # 비동기적으로 번역
    print(f'[번역된 텍스트] {translator_text}')

    file_name = f'voice_{time.time()}.mp3'
    tts = gTTS(text=translator_text, lang='en')  # 번역된 텍스트로 음성 생성
    tts.save(file_name)
    playsound(file_name)  # 생성된 음성 파일 재생
    print("사용자의 목소리를 듣는 중입니다...")


async def translate_to_english(text):
    """한국어 텍스트를 영어로 번역하는 함수"""
    translated = await translator.translate(text, src='ko', dest='en')  # 비동기적으로 번역
    return translated.text


async def speak(text):
    """주어진 텍스트를 음성으로 읽는 함수"""
    print(f'읽을 텍스트: {text}')
    file_name = 'voice.mp3'
    tts = gTTS(text=text, lang='ko')  # 한국어로 음성 생성
    tts.save(file_name)
    playsound(file_name)  # 음성 파일 재생


# 프로그램 시작
if __name__ == "__main__":
    import asyncio

    while True:
        asyncio.run(listen())  # 비동기적으로 음성을 듣는 함수 실행
