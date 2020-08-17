import datetime
import sys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pyttsx3
import speech_recognition as sr
import random
import re
import signal


WAKE_NAME = "larry"

GREETINGS = ["hi", "hello", "hola", "greetings", "hey there", "hey", "howdy"]

HOW_ARE_YOU_INPUT = ["how are you", "how's it going", "what's good", "how are you doing", "how are you today"]
HOW_ARE_YOU_OUTPUT = ["good. how are you?", "fine. and you?", "can't complain. how are you?", "great. and you?"]

JOKES_OUTPUT = ["How do you spot a blind man on a nude beach? It’s not hard.",
                "How does a rabbi make coffee? Hebrews it.",
                "I have many jokes about unemployed people, sadly none of them work.",
                "What’s the difference between a G-spot and a golf ball? A man will actually search for a golf ball.",
                "How did I quit smoking? I decided to smoke only after sex."]

X_PATHS = ["//*[contains(@class, 'qv3Wpe')]", "//*[contains(@class, 'rysD0c')]",
           "//*[contains(@class, 'TrT0Xe')]", "//*[contains(@class, 'Z0LcW')]",
           "//*[contains(@class, 'kno-rdesc')]", "//*[contains(@class, 'ILfuVd')]",
           "//*[contains(@class, 'JXRj4e')]", "//*[contains(@class, 'tw-data')]",
           "//*[contains(@class, 'WGwSK')]"]

VOICE_OPTIONS = ['com.apple.speech.synthesis.voice.fiona',
                 'com.apple.speech.synthesis.voice.Fred',
                 'com.apple.speech.synthesis.voice.karen'
                 'com.apple.speech.synthesis.voice.moira']


class VirtualAssistant(object):
    def __init__(self):
        options = Options()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def search_question(self, search_word):
        self.driver.get("https://google.com")
        search_result = ""

        # WebDriverWait(self.driver, 5).until(
        #     lambda driver: self.driver.find_element_by_xpath("//*[text()='English']")).click()
        WebDriverWait(self.driver, 5).until(
            lambda driver: self.driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')).send_keys(search_word)
        WebDriverWait(self.driver, 5).until(
            lambda driver: self.driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')).send_keys(Keys.RETURN)

        # Weather
        if re.findall(r"\bweather|\btemperature|\bdegrees", search_word):
            if self.driver.find_elements_by_xpath("//*[contains(@class, 'wob_t')]"):
                degrees = self.driver.find_elements_by_xpath("//*[contains(@class, 'wob_t')]")
                weather = self.driver.find_elements_by_xpath("//*[contains(@class, 'vk_gy')]")

                search_result = degrees[0].text + " degrees and " + weather[2].text
        else:

            for result in X_PATHS:
                try:
                    search_result = str(self.driver.find_element_by_xpath(result).text)
                    if len(search_result) > 0:
                        break
                except NoSuchElementException as e:
                    print("Searching...")
        search_result = re.sub("Description|Wikipedia|[^a-zA-Z0-9,. ]", "", search_result)
        return search_result


def greeting(sentence):
    # if the users input is a greeting, then return a randomly chosen greeting response
    for word in sentence.split():
        if word.lower() in GREETINGS:
            return random.choice(GREETINGS)

def how_are_you():
    return random.choice(HOW_ARE_YOU_OUTPUT)

def jokes():
    JOKES_OUTPUT.append(JOKES_OUTPUT[0])
    del JOKES_OUTPUT[0]
    return JOKES_OUTPUT[0]

def speak(text):
    engine = pyttsx3.init()
    # engine.setProperty('voice', VOICE_OPTIONS[0])
    engine.say(text)
    print(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio) # language='en-IN'
        except:
            pass
    return said.lower()


def timeout_handler(signum, frame):
    raise TimeoutException


if __name__ == '__main__':
    while True:
        print("Listening...")
        text = get_audio()
        print(text)

        if text.count(WAKE_NAME) > 0:
            speak("What can I help you with?")
            run = True
            while run:
                print("Listening...")
                text = get_audio()
                print(text)
                if text:
                    if re.findall(r"\bstop|\bquit|\bbye|\bthank you|\bthanks", text):
                        speak("See you next time")
                        sys.exit()
                    elif re.findall(r"\bjoke|\bfunny|\blaugh", text):
                        joke = jokes()
                        speak(joke)
                    elif re.findall(r"\btime|\bclock|\bdate", text):
                        speak(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
                    elif text in GREETINGS:
                        greet = greeting(text)
                        speak(greet)
                    elif text in HOW_ARE_YOU_INPUT:
                        response = how_are_you()
                        speak(response)
                    elif re.findall(r"\bgood\b|\bgreat\b|\bawesome\b|\bfine\b|\bok\b", text):
                        speak("Alright")
                    elif re.findall(r'\byour name', text):
                        speak(WAKE_NAME)
                    else:
                        signal.signal(signal.SIGALRM, timeout_handler)
                        signal.alarm(20)
                        try:
                            assistant = VirtualAssistant()
                            text = re.sub("what is|what was|who is|who was", "", text)
                            final_result = assistant.search_question(text)
                            signal.alarm(0)
                            assistant.driver.close()
                            assistant.driver.quit()
                            if final_result:
                                speak(final_result)
                            else:
                                speak("I'm sorry. Could you rephrase or try another question?")

                        except TimeoutException:
                            speak("Sorry, I couldn't find what you were looking for.")
            else:
                continue



