import speech_recognition as sr
import googletrans as gt
import configparser
import logging
import tkinter
from playsound import playsound
from gtts import gTTS


def speech_to_text(audioData, language):
    """
    Translates gathered audio to text
    Returns: string
    """
    logging.info("Transcribing collected audio...")
    # using google speech to text api
    transcribedAudio = speech_recognizer.recognize_google(audioData, language=language)
    logging.info("Transcribed audio: {}".format(transcribedAudio))
    return transcribedAudio


def recorder():
    """
    Gathers audio data
    Returns: speech_recognition.AudioData
    """
    with sr.Microphone() as mic:
        logging.info("Microphone is open")
        audio = speech_recognizer.listen(mic)
    logging.info("Audio collected...")
    return audio


def translate(inputLang, outputLang, string):
    """
    Translate input string to output language
    Returns: string
    """
    translator = gt.Translator(service_urls=['translate.googleapis.com'])
    translatedString = translator.translate(string, dest=outputLang, src=inputLang)
    logging.info(
        "Translated from {} to {}: {}".format(
            inputLang, outputLang, translatedString.text
        )
    )
    return translatedString


def text_to_speech(text, language, fileName="output.mp3"):
    """
    Turns the string to speech
    Returns: string (file name)
    """
    try:
        output = gTTS(text, lang=language)
        output.save(fileName)
        logging.info("Speech saved to {}".format(fileName))
        return fileName
    except:
        return False


def play_translation(file):
    """
    Plays the saved audio file
    """
    logging.info("Playing translated text...")
    playsound(file)
    logging.info("Successfully outputted audio from {}".format(file))


def translation_parameters():
    """
    GUI for language selection
    Returns: string, string (or False, False)
    """
    root = tkinter.Tk()
    speechLang = tkinter.StringVar(value="English")
    transLang = tkinter.StringVar(value="Hindi")

    dropBoxItems = []
    for lang in languages:
        dropBoxItems.append(languages[lang])

    tkinter.Label(root, text="What language are you speaking: ").pack()
    tkinter.OptionMenu(root, speechLang, *dropBoxItems).pack()
    tkinter.Label(root, text="What language are you translating to: ").pack()
    tkinter.OptionMenu(root, transLang, *dropBoxItems).pack()
    tkinter.Button(root, text="Submit", command=root.destroy).pack()

    root.mainloop()

    found = [False, False]
    for lang in languages:
        if languages[lang] == speechLang.get():
            found[0] = lang
            logging.info("Input language selected: {}".format(languages[lang]))
        if languages[lang] == transLang.get():
            found[1] = lang
            logging.info("Output language selected: {}".format(languages[lang]))

    return found[0], found[1]


def main():
    logging.basicConfig(level=logging.INFO)

    inputLang, outputLang = translation_parameters()

    if inputLang and outputLang:
        recordedAudio = recorder()
        transcribedAudio = speech_to_text(recordedAudio, inputLang)
        translatedString = translate(inputLang, outputLang, transcribedAudio)
        translatedAudioFile = text_to_speech(translatedString.text, outputLang)
        play_translation(translatedAudioFile)
    else:
        logging.warning("Insufficent Languages Detected... Closing Application")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    speech_recognizer = sr.Recognizer()

    languagesConfig = configparser.ConfigParser()
    languagesConfig.read("languages.ini")
    languages = languagesConfig["LANGUAGES"]
    
    main()
