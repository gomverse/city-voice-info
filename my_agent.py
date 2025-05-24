"""
사용자의 음성을 인식해서 텍스트로 변환 후 명령을 수행하는 프로그램

- 목표
서울 날씨 -> 현재 서울의 날씨는 *입니다. 온도는 *도 입니다
서울 시간과 날짜 -> 서울 기준 현재 *년 *월 *일이고 시간은 *시 *분 입니다
로스엔젤레스 시간 -> 로스엔젤레스 기준 현재 시간은 *시 *분 입니다

받을 건 4개
도시이름, 날짜, 시간, 날씨
만약 입력이 4개보다 적다면 기본값 설정

"""

import datetime


def get_today_text():
    today = datetime.date.today()
    return f"오늘은 {today.year}년 {today.month}월 {today.day}일 입니다"


def get_time_text():
    formatted = datetime.datetime.now().strftime("%p %I시 %M분")
    formatted = formatted.replace("AM", "오전").replace("PM", "오후")
    return f"지금 시간은 {formatted}입니다"


city_names = ["서울", "뉴욕", "파리"]
keywords = [city_names, "날짜", "시간", "날씨"]

user_text1 = "서울의 시간과 날짜"
user_text2 = "뉴욕의 날짜"

print(any(city in user_text1 for city in city_names))

import speech_recognition as sr
import datetime
import requests
from io import BytesIO
from navertts import NaverTTS
from pydub import AudioSegment
from pydub.playback import play

r = sr.Recognizer()
microphone = sr.Microphone()

API_KEY = "3bf5025e7a056c6a9f654fd7714db04b"  # API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
city = None

request_url = f"{BASE_URL}?appid={API_KEY}&q={city}&lang=kr"
response = requests.get(request_url)

if response.status_code == 200:  # 200은 성공

    data = response.json()
    city_name = data["name"]
    weather = data["weather"][0]["description"]
    temperature = round(data["main"]["temp"] - 273.15, 2)  # 켈빈 온도 사용

    print("City:", city_name)
    print("Weather:", weather)
    print("Temperature:", temperature, "celsius")

else:
    print("An error occurred.", response.status_code)


#############################
def get_today_text():
    today = datetime.date.today()
    return f"오늘은 {today.year}년 {today.month}월 {today.day}일 입니다"


def get_time_text():
    formatted = datetime.datetime.now().strftime("%p %I시 %M분")
    formatted = formatted.replace("AM", "오전").replace("PM", "오후")
    return f"지금 시간은 {formatted}입니다"


def command_naver_tts(user_command):
    """naver tts의 음성"""

    COMMANDS = {
        "input_command": lambda: "명령을 내려주세요",
        "fail_recognize": lambda: "인식할 수 없습니다",
        "exit": lambda: "종료합니다",
        "today": get_today_text,
        "time": get_time_text,
    }

    tts_text = COMMANDS.get(user_command, lambda: "")()
    tts = NaverTTS(tts_text, lang="ko")
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp = BytesIO(fp.getvalue())
    my_sound = AudioSegment.from_file(fp, format="mp3")
    play(my_sound)


while True:
    with microphone as source:
        r.adjust_for_ambient_noise(source)  # 배경 소음을 측정하고
        command_naver_tts("input_command")
        audio = r.listen(source)  # 일정 크기 이상의 소리가 들리면 녹음
    try:
        text = r.recognize_google(audio, language="ko")
    except:
        command_naver_tts("fail_recognize")
    else:
        if "종료" in text:
            command_naver_tts("exit")
            break
        if "날짜" in text:
            command_naver_tts("today")
        if "시간" in text:
            command_naver_tts("time")
