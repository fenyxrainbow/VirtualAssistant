# Importações necessárias
import os
import speech_recognition as sr
from gtts import gTTS
import pygame
import webbrowser
import wikipediaapi

# Configuração do idioma padrão
LANGUAGE = "pt"

# Inicializa o pygame para reprodução de áudio
pygame.mixer.init()

# Módulo 1: Texto para Áudio (Text to Speech)
def text_to_speech(text, lang=LANGUAGE):
    """
    Converte texto em áudio usando gTTS.
    :param text: Texto a ser convertido em áudio.
    :param lang: Idioma do texto (padrão é português).
    """
    try:
        tts = gTTS(text=text, lang=lang)
        audio_file = "output.mp3"
        tts.save(audio_file)

        # Reproduz o áudio usando pygame
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Aguarda a reprodução terminar
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.stop()  # Garante que o áudio é interrompido antes da exclusão
        os.remove(audio_file)  # Remove o arquivo de áudio após a reprodução
    except Exception as e:
        print(f"Erro ao converter texto em áudio: {e}")

# Módulo 2: Fala para Texto (Speech to Text)
def speech_to_text():
    """
    Captura áudio do microfone e converte em texto.
    :return: Texto reconhecido.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando o microfone para ruído ambiente...")
        recognizer.adjust_for_ambient_noise(source)  # Calibra o microfone
        print("Diga algo...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="pt-BR").lower()
            print(f"Você disse: {text}")
            return text
        except sr.UnknownValueError:
            print("Não foi possível entender a fala.")
            return None
        except sr.RequestError:
            print("Erro na conexão com o serviço de reconhecimento de voz.")
            return None

# Módulo 3: Comandos de Voz
def execute_command(command):
    """
    Executa comandos de voz.
    :param command: Comando de voz reconhecido.
    """
    if not command:
        return

    if "wikipedia" in command:
        search_term = command.replace("wikipedia", "").strip()
        wiki = wikipediaapi.Wikipedia(LANGUAGE)
        page = wiki.page(search_term)

        if page.exists():
            summary = page.summary[:500]  # Limita o áudio aos primeiros 500 caracteres
            print(summary)
            text_to_speech(summary)
        else:
            msg = f"Não encontrei informações sobre {search_term} na Wikipedia."
            print(msg)
            text_to_speech(msg)

    elif "youtube" in command:
        text_to_speech("Abrindo o YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "farmácia" in command or "farmacia" in command:
        text_to_speech("Procurando a farmácia mais próxima.")
        webbrowser.open("https://www.google.com/maps/search/farmácia")

    elif "sair" in command or "parar" in command:
        text_to_speech("Até logo!")
        os._exit(0)  # Sai do programa imediatamente

    else:
        text_to_speech("Não entendi o comando.")

# Função principal do assistente virtual
def virtual_assistant():
    """
    Sistema de assistência virtual que responde a comandos de voz.
    """
    text_to_speech("Olá, como posso ajudar você hoje?")
    while True:
        command = speech_to_text()
        execute_command(command)

# Execução do assistente virtual
if __name__ == "__main__":
    try:
        virtual_assistant()
    except KeyboardInterrupt:
        print("\nAssistente virtual encerrado.")
    except Exception as e:  # Captura qualquer outra exceção
        print(f"Ocorreu um erro: {e}")
        text_to_speech("Desculpe, ocorreu um erro. Encerrando o assistente virtual.")
        os._exit(1)