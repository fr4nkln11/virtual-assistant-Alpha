import PySimpleGUI as sg
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
import wolframalpha
import json
import requests
import random
import pyaudio
from ecapture import ecapture as ec

sg.theme('Black')


menu_def = [['&Menu', ['&About...', 'Donate', 'E&xit']]]


layout = [[sg.Menu(menu_def, tearoff=True)],
          [sg.Text('Welcome! I am your Virtual Assistant Spyro.', font=('Comic sans ms', 10))],
          [sg.Text('Time & Date:     ', font=('Comic sans ms', 8)),sg.Text('', size=(30,1), font=('Comic sans ms', 8), key='_DATE_')],
          [sg.Text('  ', size=(22,1)), sg.Image('ai2.gif', size = (90,90), key = "Prog_bar")],
          [sg.Text('Please Tap Speak to speak your query.', font=('Comic sans ms', 8))],
          [sg.Output(size=(80, 17), key='out')],
          [sg.Input(size=(80,1), key='-in-')],
          [sg.Button('Speak', size=(34, 3), button_color=('white', 'blue')), sg.Button('Type', size=(34, 3), bind_return_key=True, button_color=('white', 'blue'))]]




window = sg.Window('Spyro', location=(740,0), resizable=True).Layout(layout)

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')

def speak(text):
    engine.say(text)
    engine.runAndWait()




def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"user said:{statement}\n")

        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement


 
def tim():
    tim = datetime.datetime.now()
    return (tim.strftime("%H:%M:%S %Y-%m-%d"))



def main():
    while True:
        time = tim()
        button, value = window.Read(timeout=1)
        window.Element('_DATE_').Update(str(time))
        window.FindElement("Prog_bar").UpdateAnimation("ai2.gif", time_between_frames=100)
        if button == 'Speak':
            statement = takeCommand().lower()
            if statement==0:
                continue

            elif "hello" in statement or "hi" in statement or "hey" in statement:
                    hour=datetime.datetime.now().hour
                    if hour>=0 and hour<12:
                        speak("Hello,Good Morning")
                        print("Hello,Good Morning")
                    elif hour>=12 and hour<18:
                        speak("Hello,Good Afternoon")
                        print("Hello,Good Afternoon")
                    else:
                        speak("Hello,Good Evening")
                        print("Hello,Good Evening")

            elif "good bye" in statement or "ok bye" in statement or "stop" in statement:
                speak('your virtual assistant Spyro is shutting down,Good bye')
                print('your virtual assistant Spyro is shutting down,Good bye')
                break

            elif 'wikipedia' in statement:
                try:
                    speak('Searching Wikipedia...')
                    statement =statement.replace("wikipedia", "")
                    results = wikipedia.summary(statement, sentences=3)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except wikipedia.exceptions.DisambiguationError as e:
                    s = random.choice(e.options)
                    print(s)
                    speak(s)
                else:
                    continue
  
                

            elif 'open youtube' in statement:
                webbrowser.open_new_tab("https://www.youtube.com")
                speak("youtube is open now")
                print("youtube is open now")

            elif 'open google' in statement:
                webbrowser.open_new_tab("https://www.google.com")
                speak("Google chrome is open now")
                print("Google chrome is open now")

            elif 'open gmail' in statement:
                webbrowser.open_new_tab("gmail.com")
                speak("Google Mail open now")
                print("Google Mail open now")

            elif "weather" in statement:
                api_key="394d4ebf0a7de20604147666d665d2d0"
                base_url="https://api.openweathermap.org/data/2.5/weather?"
                speak("whats the city name")
                print("whats the city name")
                city_name=takeCommand()
                complete_url=base_url+"appid="+api_key+"&q="+city_name
                response = requests.get(complete_url)
                x=response.json()
                if x["cod"]!="404":
                    y=x["main"]
                    current_temperature = y["temp"]
                    current_humidiy = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    speak(" Temperature in kelvin unit is " +
                          str(current_temperature) +
                          "\n humidity in percentage is " +
                          str(current_humidiy) +
                          "\n description  " +
                          str(weather_description))
                    print(" Temperature in kelvin unit = " +
                          str(current_temperature) +
                          "\n humidity (in percentage) = " +
                          str(current_humidiy) +
                          "\n description = " +
                          str(weather_description))
                else:
                    speak(" City Not Found ")
                    print(" City Not Found ")

            elif 'time' in statement:
                strTime=datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"the time is {strTime}")
                print(f"the time is {strTime}")

            elif 'who are you' in statement or 'what can you do' in statement:
                speak('I am Spyro version 1 point O your virtual assistant. I am programmed to do minor tasks like'
                      'opening youtube,google chrome,gmail and facebook ,predict time,take a photo,search wikipedia, predict weather' 
                      'in different cities , get top headline news from CNN and you can ask me computational or geographical questions too!')
                print('I am Spyro version 1 point O your virtual assistant. I am programmed to do minor tasks like'
                      'opening youtube,google chrome,gmail and facebook ,predict time,take a photo,search wikipedia, predict weather' 
                      'in different cities , get top headline news from CNN and you can ask me computational or geographical questions too!')



            elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
                speak("I was built by Adrijan")
                print("I was built by Adrijan")

            elif "open facebook" in statement:
                webbrowser.open_new_tab("https://sl-si.facebook.com/")
                speak("Here is Facebook")
                print("Here is Facebook")

            elif 'news' in statement:
                news = webbrowser.open_new_tab("https://edition.cnn.com/")
                speak('Here are some headlines from the CNN,Happy reading')
                print('Here are some headlines from the CNN,Happy reading')

            elif "camera" in statement or "take a photo" in statement:
                ec.capture(0,"robo camera","img.jpg")

            elif 'search'  in statement:
                statement = statement.replace("search", "")
                webbrowser.open_new_tab(statement)

            elif 'ask' in statement:
                speak('I can answer to computational and geographical questions and what question do you want to ask now')
                question=takeCommand()
                app_id="47RWRU-LR6849249K"
                client = wolframalpha.Client('47RWRU-LR6849249K')
                res = client.query(question)
                answer = next(res.results).text
                speak(answer)
                print(answer)

            elif "joke" in statement:
                with open("joke.txt", "r") as m:
                    sents = m.read().split("\n\n")
                    se = random.choice(sents)
                    speak(se)
                    print(se)

            elif "commands" in statement:
                speak("commands are:"+
                      "hello, hi or hey"+
                      "good bye, ok bye or stop"+
                      "wikipedia 'your search'"+
                      "open youtube"+
                      "open google"+
                      "open gmail"+
                      "weather 'city name'"+
                      "time"+
                      "who are you or what can you do"+
                      "who made you or who created you"+
                      "open facebook"+
                      "news"+
                      "camera or take a photo"+
                      "search 'your choice'"+
                      "ask 'your choice'"+
                      "log off or sing out"+
                      "joke")
                print("commands are:"+"\n"+
                      "hello, hi or hey"+
                      "good bye, ok bye or stop"+"\n"+
                      "wikipedia 'your search'"+"\n"+
                      "open youtube"+"\n"+
                      "open google"+"\n"+
                      "open gmail"+"\n"+
                      "weather 'city name'"+"\n"+
                      "time"+"\n"+
                      "who are you or what can you do"+"\n"+
                      "who made you or who created you"+"\n"+
                      "open facebook"+"\n"+
                      "news"+"\n"+
                      "camera or take a photo"+"\n"+
                      "search 'your choice'"+"\n"+
                      "ask 'your choice'"+"\n"+
                      "log off or sing out"+"\n"+
                      "joke")
            


            elif "log off" in statement or "sign out" in statement:
                speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                print("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                subprocess.call(["shutdown", "/l"])


        if button == 'Type':
            window.Element('-in-').Update('')
            message = value['-in-']
            print("user type: "+message)
            if message==0:
                continue

            elif "hello" in message or "hi" in message or "hey" in message:
                    hour=datetime.datetime.now().hour
                    if hour>=0 and hour<12:
                        speak("Hello,Good Morning")
                        print("Hello,Good Morning")
                    elif hour>=12 and hour<18:
                        speak("Hello,Good Afternoon")
                        print("Hello,Good Afternoon")
                    else:
                        speak("Hello,Good Evening")
                        print("Hello,Good Evening")

            elif "good bye" in message or "ok bye" in message or "stop" in message:
                speak('your virtual assistant Spyro is shutting down,Good bye')
                print('your virtual assistant Spyro is shutting down,Good bye')
                break

            elif 'wikipedia' in message:
                try:
                    speak('Searching Wikipedia...')
                    message =message.replace("wikipedia", "")
                    results = wikipedia.summary(message, sentences=3)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except wikipedia.exceptions.DisambiguationError as e:
                    s = random.choice(e.options)
                    print(s)
                    speak(s)
                else:
                    continue
  
                

            elif 'open youtube' in message:
                webbrowser.open_new_tab("https://www.youtube.com")
                speak("youtube is open now")
                print("youtube is open now")

            elif 'open google' in message:
                webbrowser.open_new_tab("https://www.google.com")
                speak("Google chrome is open now")
                print("Google chrome is open now")

            elif 'open gmail' in message:
                webbrowser.open_new_tab("gmail.com")
                speak("Google Mail open now")
                print("Google Mail open now")

            elif "weather" in message:
                api_key="394d4ebf0a7de20604147666d665d2d0"
                base_url="https://api.openweathermap.org/data/2.5/weather?"
                city_name = message.replace('weather', '')
                complete_url=base_url+"appid="+api_key+"&q="+city_name
                response = requests.get(complete_url)
                x=response.json()
                if x["cod"]!="404":
                    y=x["main"]
                    current_temperature = y["temp"]
                    current_humidiy = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    speak(str(city_name)+
                          " Temperature in kelvin unit is " +
                          str(current_temperature) +
                          "\n humidity in percentage is " +
                          str(current_humidiy) +
                          "\n description  " +
                          str(weather_description))
                    print(str(city_name)+
                          " Temperature in kelvin unit = " +
                          str(current_temperature) +
                          "\n humidity (in percentage) = " +
                          str(current_humidiy) +
                          "\n description = " +
                          str(weather_description))
                else:
                    speak(" City Not Found ")
                    print(" City Not Found ")

            elif 'time' in message:
                strTime=datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"the time is {strTime}")
                print(f"the time is {strTime}")

            elif 'who are you' in message or 'what can you do' in message:
                speak('I am Spyro version 1 point O your virtual assistant. I am programmed to do minor tasks like'
                      'opening youtube,google chrome,gmail and facebook ,predict time,take a photo,search wikipedia, predict weather' 
                      'in different cities , get top headline news from CNN and you can ask me computational or geographical questions too!')
                print('I am Spyro version 1 point O your virtual assistant. I am programmed to do minor tasks like'
                      'opening youtube,google chrome,gmail and facebook ,predict time,take a photo,search wikipedia, predict weather' 
                      'in different cities , get top headline news from CNN and you can ask me computational or geographical questions too!')

            elif "who made you" in message or "who created you" in message or "who discovered you" in message:
                speak("I was built by Adrijan")
                print("I was built by Adrijan")

            elif "open facebook" in message:
                webbrowser.open_new_tab("https://sl-si.facebook.com/")
                speak("Here is Facebook")

            elif 'news' in message:
                news = webbrowser.open_new_tab("https://edition.cnn.com/")
                speak('Here are some headlines from the CNN,Happy reading')
                print('Here are some headlines from the CNN,Happy reading')
            

            elif "camera" in message or "take a photo" in message:
                ec.capture(0,"robo camera","img.jpg")

            elif 'search'  in message:
                message = message.replace("search", "")
                webbrowser.open_new_tab(message)

            elif 'ask' in message:
                question=message.replace('ask', '')
                app_id="47RWRU-LR6849249K"
                client = wolframalpha.Client('47RWRU-LR6849249K')
                res = client.query(question)
                answer = next(res.results).text
                speak(answer)
                print(answer)

            elif "joke" in message:
                with open("joke.txt", "r") as m:
                    sents = m.read().split("\n\n")
                    se = random.choice(sents)
                    speak(se)
                    print(se)

            elif "commands" in message:
                speak("commands are:"+
                      "hello, hi or hey"+
                      "good bye, ok bye or stop"+
                      "wikipedia 'your search'"+
                      "open youtube"+
                      "open google"+
                      "open gmail"+
                      "weather 'city name'"+
                      "time"+
                      "who are you or what can you do"+
                      "who made you or who created you"+
                      "open facebook"+
                      "news"+
                      "camera or take a photo"+
                      "search 'your choice'"+
                      "ask 'your choice'"+
                      "log off or sing out"+
                      "joke")
                print("commands are:"+"\n"+
                      "hello, hi or hey"+
                      "good bye, ok bye or stop"+"\n"+
                      "wikipedia 'your search'"+"\n"+
                      "open youtube"+"\n"+
                      "open google"+"\n"+
                      "open gmail"+"\n"+
                      "weather 'city name'"+"\n"+
                      "time"+"\n"+
                      "who are you or what can you do"+"\n"+
                      "who made you or who created you"+"\n"+
                      "open facebook"+"\n"+
                      "news"+"\n"+
                      "camera or take a photo"+"\n"+
                      "search 'your choice'"+"\n"+
                      "ask 'your choice'"+"\n"+
                      "log off or sing out"+"\n"+
                      "joke")
                      


            elif "log off" in message or "sign out" in message:
                speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
                print("Ok , your pc will log off in 10 sec make sure you exit from all applications.")
                subprocess.call(["shutdown", "/l"])
            


        elif button in (None, 'Exit'):
            break

        elif button == 'About...':
            sg.popup('About:', 'Created by Adrijan P.', 'Virtual Assistant:'+'\n\n'+'Spyro', 'Version 1.0')

        elif button == 'Donate':
            webbrowser.open_new_tab("https://www.paypal.com/donate/?cmd=_s-xclick&hosted_button_id=PFB6A6HLAQHC2&source=url")


    window.close()

        
main()
