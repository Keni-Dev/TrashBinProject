import PySimpleGUI as sg
import pyttsx3, sys, serial, pygame

"""
I CODED THIS JUST FOR MANUAL INPUT. 
Di na kailangan ng speech recognition. Just type in the words and marerecognize na ito ng script
"""

board = serial.Serial('COM4', 115200)

layout = [
    [sg.Input(key='INPUT')]
]
window = sg.Window('This is a fokin virus', layout, return_keyboard_events=True, finalize=True)
window['INPUT'].bind("<Return>", "_Enter")

def SpeakText(word): # This function handles the speaking of the text
    engine = pyttsx3.init()
    engine.say(word)
    engine.runAndWait()

def DetectWords(word): # This function handles the detection of the words/command
    if 'open' in word:
        board.write(b'1')
        SpeakText("Opening")

    elif 'close' in word:
        board.write(b'0')
        SpeakText("Closing")

    elif 'restart' in word:
        board.write(b'2')
        SpeakText('Restarting')

    elif 'bye' in word:
        SpeakText('Turning off')
        board.write(b'0')
        sys.exit()
        
    elif 'quiet' in word:
        SpeakText("No, you shut up")

        pygame.mixer.init()
        path = 'D:\\Documents\\Trash-bin-Project\\Sounds\\Pekora.wav'
        pekora = pygame.mixer.Sound(path)
        pekora.play()
        pygame.time.wait(int(pekora.get_length() * 1000))


    else:
        SpeakText(f'{word} is not a command')

def window_main():
    while True:
        event, values = window.read()
            
        var = values['INPUT']
        
        if event == sg.WIN_CLOSED:
            board.write(b'0')
            print('closing')
            break

        if event == 'INPUT_Enter':
            DetectWords(var)

            window['INPUT']('')
            
    
    print('closing')
    window.close()
    board.write(b'0')

if __name__ == '__main__':
    window_main()