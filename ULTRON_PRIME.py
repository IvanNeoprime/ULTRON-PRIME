import cv2
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

import wikipedia

def searchWikipedia(query):
    """Busca no Wikipedia e retorna os resultados."""
    try:
        wikipedia.set_lang("pt")  # Configura o idioma para português
        result = wikipedia.summary(query, sentences=2)  # Resumo de duas frases
        speak("Segundo as minhas fontes:")
        print(result)
        speak(result)  # O assistente fala a resposta do Wikipedia
    except wikipedia.exceptions.DisambiguationError:
        speak("Sua pesquisa retornou múltiplos resultados. Por favor, seja mais específico.")
    except wikipedia.exceptions.PageError:
        speak("Não encontrei informações relevantes.")
    except Exception as e:
        speak("Houve um erro ao processar a solicitação.")
        print(e)


#uso da camera a partir do openCV
def Start():
    """iniciar camera"""
    speak("activando camera...")
    face_cascade = cv2.CascadeClassifier (cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.color_BGR2GRAY)
        faces = face_cascade.detectMulticolorScale(gray, ScaleFactor = 1.1, miNehbors=5, minisize=(20, 20))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y+h), (255, 0, 0), 2)
        cv2.imshow("camera - pressione 'q' para sair", frame)

        if cv2.waitkey (1) & 0xff == ord ('q'):
            break

        cap.relase()
        cv2.destroyAllwindows()
        speak("desligando camera")        



def sendEmail(to, content):
    """Envia um e-mail."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('Email', 'senha')
        server.sendmail('teu e-mail', to, content)
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
            speak("abrindo Youtube")
            webbrowser.open('youtube.com')

        # Abrir Google
        elif 'abrir google' in query:
            webbrowser.open('google.com')

        #temperatura
        elif 'tempo' in query:
            webbrowser.open('https://mz.freemeteo.com/clima/maputo/7-dias/lista/?gid=1040652&language=portuguesebr&country=mozambique')


        #buscar infos da net wikipedia
        elif 'pesquisar' in query:
            speak("O que você deseja pesquisar mestre?")
            search_query = takeCommand().lower()
            if search_query != "None":
                searchWikipedia(search_query)   

        # Informar as horas
        elif 'horas' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Mestre, agora são {strTime} minutos.")

        # Enviar e-mail
        elif 'email para ....' in query:
            try:
                speak("O que devo escrever, Mestre?")
                content = takeCommand()
                to = 'teupaicalvo79@gmail.com'
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Lamento, Mestre, mas não consegui enviar o e-mail.")
                               
        # Encerrar o programa
        elif 'sair' in query or 'quit' in query:
            speak("Encerrando o sistema, Mestre. Até logo.")
            break
