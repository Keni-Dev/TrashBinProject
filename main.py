import speech_recognition as sr
import serial, pygame, pyttsx3, sys, time

"""
HA↗HA↘HA⬆HA↗HA⬇HA↙HA➡
"""

"""
Speech recognition script 
"""

# Gets the arduino board
board = serial.Serial('COM4', 115200)

# Handles the things needed for speech recognition
r = sr.Recognizer()
mic = sr.Microphone()

keyword = 'hey' # We need this to say to start up the script

def main(source): # This function handles the commands/words that you've said
    print('Adjusting...')
    r.adjust_for_ambient_noise(source, duration=1)

    print('You can speak now')
    

    SpeakText('Listening')
    
    audio = r.listen(source)

    print('Recognizing now...')
    SpeakText('Recognizing now')

    try:
        output_text = r.recognize_google(audio)
        output_text = output_text.lower()
        print(f'Word: {output_text}')
        DetectWords(output_text, source)

    except sr.UnknownValueError: # Handles if your word/command isn't recognized
        print('Didn\'t recognize the word')
        SpeakText("Word not recognized, please try again")
        return main(source)
    
    except KeyboardInterrupt:
        board.write(b'0')
        


def awake(source): # This function handles the keyword that needed to run
    r.adjust_for_ambient_noise(source, duration=0.75)
    print('Listening...')
    audio = r.listen(source)
    print('Detected')

    try: # This will run if the word recognized
        text = r.recognize_google(audio)
        text = text.lower()

        print(f'Word: {text}')

        if keyword in text:
            print('Keyword detected')
            SpeakText("Hello Kenny")
            main(source)
        else:
            awake(source)

    except KeyboardInterrupt:
        board.write(b'0')
        return
    
    except sr.UnknownValueError: # Will return if you haven't said the keyword
        return awake(source)

    except:
        return awake(source)



def DetectWords(word, source): # This function detects if the word you said is a valid command/word
    if 'open' in word:
        board.write(b'1')
        SpeakText("Opening")
        main(source)

    elif 'close' in word:
        board.write(b'0')
        SpeakText("Closing")
        main(source)

    elif 'restart' in word:
        board.write(b'2')
        SpeakText('Restarting')
        time.sleep(1)
        main(source)

    elif 'bye' in word:
        board.write(b'0')
        SpeakText('Bye bye')
        awake(source)

    elif 'quiet' in word:
        SpeakText("No, you shut up")

        pygame.mixer.init()
        path = 'D:\\Documents\\Trash-bin-Project\\Sounds\\Pekora.wav'
        pekora = pygame.mixer.Sound(path)
        pekora.play()
        pygame.time.wait(int(pekora.get_length() * 1000))

        main(source)
    
    elif 'off' in word:
        board.write(b'0')
        SpeakText('Turning off')
        sys.exit()
        
    else:
        SpeakText(f'{word} is not a command')
        print('Not a word u idiot')
        main(source)
        

def SpeakText(word): # This function handles the speaking of the text
    engine = pyttsx3.init()
    engine.say(word)
    engine.runAndWait()

if __name__ == '__main__': # This will run at the start of the script
    with mic as source:
        awake(source)