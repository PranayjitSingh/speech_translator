import speech_recognition as sr
import googletrans as gt
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
    transcribedAudio = r.recognize_google(audioData, language=language)
    logging.info("Transcribed audio: {}".format(transcribedAudio))
    return transcribedAudio


def recorder():
    """
    Gathers audio data
    Returns: speech_recognition.AudioData
    """
    with sr.Microphone() as mic:
        logging.info("Microphone is open")
        audio = r.listen(mic)
    logging.info("Audio collected...")
    return audio


def translate(inputLang, outputLang, string):
    """
    Translate input string to output language
    Returns: string
    """
    translator = gt.Translator()
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
            logging.info("Input language selected: {}".format(lang))
        if languages[lang] == transLang.get():
            found[1] = lang
            logging.info("Output language selected: {}".format(lang))

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
    r = sr.Recognizer()
    languages = {
        "af": "Afrikaans",
        "ar": "Arabic",
        "bn": "Bengali",
        "bs": "Bosnian",
        "ca": "Catalan",
        "cs": "Czech",
        "cy": "Welsh",
        "da": "Danish",
        "de": "German",
        "el": "Greek",
        "en": "English",
        "eo": "Esperanto",
        "es": "Spanish",
        "et": "Estonian",
        "fi": "Finnish",
        "fr": "French",
        "gu": "Gujarati",
        "hi": "Hindi",
        "hr": "Croatian",
        "hu": "Hungarian",
        "hy": "Armenian",
        "id": "Indonesian",
        "is": "Icelandic",
        "it": "Italian",
        "ja": "Japanese",
        "jw": "Javanese",
        "km": "Khmer",
        "kn": "Kannada",
        "ko": "Korean",
        "la": "Latin",
        "lv": "Latvian",
        "mk": "Macedonian",
        "ml": "Malayalam",
        "mr": "Marathi",
        "my": "Myanmar (Burmese)",
        "ne": "Nepali",
        "nl": "Dutch",
        "no": "Norwegian",
        "pl": "Polish",
        "pt": "Portuguese",
        "ro": "Romanian",
        "ru": "Russian",
        "si": "Sinhala",
        "sk": "Slovak",
        "sq": "Albanian",
        "sr": "Serbian",
        "su": "Sundanese",
        "sv": "Swedish",
        "sw": "Swahili",
        "ta": "Tamil",
        "te": "Telugu",
        "th": "Thai",
        "tl": "Filipino",
        "tr": "Turkish",
        "uk": "Ukrainian",
        "ur": "Urdu",
        "vi": "Vietnamese",
    }
    main()
