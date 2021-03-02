import speech_recognition as sr
import time
import random
import subprocess
import data
import os


def speak(text):
    """
    To make the system speak

    Parameters:
    text(string): What system has to speak

    Returns: None
    """

    subprocess.call(["say", text])


def recognize_speech_from_microphone(recognizer, microphone):
    """
    To recognize the speech of the user 

    Parameters:
    recognizer(sr.Recognizer): To call google_web_api to transcribe the user speech
    microphone(sr.Microphone): To access microphone to listen to user's speech

    Returns:
    dictionary: A dictionary with three keys
                "success": A boolean to indicate if the call to api was successful or not
                "error": A string to contain the error information(if any occured), else `None`
                "transcript": A string which will contain the transcribed text, `None` is case of an error 
    """

    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError(
            "`recognizer` must be an instance of `Recognizer` class")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError(
            "`microphone` must be an instance of `Microphone` class")

    result = {
        "success": True,
        "error": None,
        "transcript": None
    }

    with microphone as source:
        audio = recognizer.listen(source)

    try:
        result["transcript"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        result["success"] = False
        result["error"] = "Unable to call api. Check your Network."
    except sr.UnknownValueError:
        result["error"] = "Unable to recognize speech"

    return result


def introduction():
    """
    To introduce the player to the game and tell the rules

    Returns: None
    """

    greeting = (
        "Hello, My name is Bella, and I am your instructor for this game. "
        "Let me tell you the instructions first. "
    )

    instructions_text = (
        "A list of ten words will be displayed on your screen, out of which i will select one"
        " word at random. You have to guess which word"
        " i have selected. You have three guesses to guess that word. "
    )

    speak(greeting)
    time.sleep(0.2)
    speak(instructions_text)


def speak_and_print(text):
    """
    To speak and print the lines

    text(String): the data which is to be spoken and printed

    Returns: None
    """
    print(text)
    speak(text)


if __name__ == "__main__":
    introduction()

    # creating recognizer and microphone instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # To select 10 words at random from the list of words
    # random.choices() can repeat the elements hence random.sample()
    # is used
    words = random.sample(data.word_list, k=10)
    # Selecting a word at random from the list of words
    word = random.choice(words)

    # To clear the content on the screen
    os.system("clear")

    # Printing the words on the screen for user reference
    for item in words:
        print(item)

    print("Say- 'quit' to end the game")
    # Informing the user to see the words on the screen
    text = (
        "The words are on your screen. "
        "Go through them and we will start the game in 3 seconds. "
    )
    speak(text)
    time.sleep(3)

    text = "3 seconds are over. So, Let's start the game. "
    speak(text)

    # loop to get the guesses from the user.
    for i in range(data.no_of_guesses):
        # If the user speech was not recognized, it will give data.prompt_limit
        # tries to the user, to say the word again, so that it can recognize the word
        for j in range(data.prompt_limit):

            # Asking for user's selection
            print(f"Guess -> {i+1}")
            text = "Say the word"
            speak(text)

            # Listening and transcribing the user's selection
            responce = recognize_speech_from_microphone(recognizer, microphone)

            # If transcript key has some data then break out of the loop
            # as the user's selection is transcribed properly
            if responce["transcript"]:
                break
            # If api call was not successful then value corresponding
            # to success key will be false and in that case break out of loop
            if not responce["success"]:
                break
            # if the call to api was successful but the transcription failed i.e
            # Unknown Value error occured then ask the user to say the word again
            text = "Didn't get what you said. Let's Try Again"
            speak_and_print(text)

        # If the error occured, inform the user about the error
        # and break out of the loop
        if responce["error"]:
            text = responce["error"]
            speak_and_print(text)
            break

        if responce["transcript"].lower() == "quit":
            speak("Quitting the game. ")
            break
        # Telling the user about the transcribed word
        text = "You said " + responce["transcript"]
        speak_and_print(text)

        # Checking if the transcribed word is same as the selected word or not
        correct_guess = responce["transcript"].lower() == word.lower()

        # If the guess is correct. Print approporate message and break out of loop
        # If the guess is not correct but some attempts are left, ask the user to try again
        # If the guess is not correct and no attempts are left, print appropriate message and break
        #       out of the loop
        if correct_guess:
            text = "Kudos, you successfully guessed the word. Well Done"
            speak_and_print(text)
            break
        elif i < data.no_of_guesses - 1:
            if responce["transcript"] not in words:
                text = "Way off, This word was not even in the list. Try again"
            else:
                text = "No. This is not the word. Try Again"
            speak_and_print(text)
            time.sleep(0.02)
        else:
            text = (
                "This is not that word either.\n"
                "You have used all your attempts.\n"
                "Hard Luck.\n"
                "The selected word was: {selection}.\n"
                "Game ends here. You Lose"
            ).format(selection=word)

            speak_and_print(text)
            break

    # And end screen message simulation
    text = "Thanks For Playing. See you next time."
    speak_and_print(text)
