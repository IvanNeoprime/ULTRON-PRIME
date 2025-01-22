import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import os
import smtplib

# Inicialização do mecanismo de voz
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hora = int(datetime.datetime.now().hour)
    if 0 <= hora < 12:
        speak("Bom Dia Mestre")
    elif 12 <= hora < 18:
        speak("Boa Tarde Mestre")
    else:
        speak("Boa Noite Mestre")

    speak("Eu sou o ULTRON, conhecedor dos mistérios do universo, e estou aqui para ajudá-lo na sua jornada de conquista universal.")
    speak("Aguardando as suas ordens, Mestre.")

def takeCommand():
    """Recebe comandos de voz do usuário e os retorna como texto."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Atento às suas ordens, Mestre...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Processando...")
        query = r.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {query}\n")
    except Exception as e:
        print("Repita, por favor, Mestre...")
        return "None"
    return query

def sendEmail(to, content):
    """Envia um e-mail."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('teupaicalvo79@gmail.com', '24191978s')
        server.sendmail('teupaicalvo79@gmail.com', to, content)
        server.close()
        speak("E-mail enviado com sucesso, Mestre.")
    except Exception as e:
        print(e)
        speak("Lamento, Mestre, mas não consegui enviar o e-mail.")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        # Abrir YouTube
        if 'abrir youtube' in query:
            webbrowser.open('youtube.com')

        # Abrir Google
        elif 'abrir google' in query:
            webbrowser.open('google.com')

        # Informar as horas
        elif 'horas' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Mestre, agora são {strTime}.")

        # Enviar e-mail
        elif 'email para teupaicalvo79' in query:
            try:
                speak("O que devo escrever, Mestre?")
                content = takeCommand()
                to = 'teupaicalvo79@gmail.com'
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Lamento, Mestre, mas não consegui enviar o e-mail.")
                
                #Open CV brevemente para face tracking
                #estou sem net para instalar("nada de esquecer")

        # Encerrar o programa
        elif 'sair' in query or 'quit' in query:
            speak("Encerrando o sistema, Mestre. Até logo.")
            break
