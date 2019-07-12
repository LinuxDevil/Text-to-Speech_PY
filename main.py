# importing libraries
import re
import wave
import pyaudio
import _thread
import time

# The main class
class PythonTextToSpeachITEAM:

    # defining the chunk
    CHUNK = 1024

    # initializing the words list to be the cmudict-0.7b.text as a string
    def __init__(self, words_pron_dict:str = 'cmudict-0.7b.txt'):
        self._l = {}
        # loading the words
        self._load_words_in_file(words_pron_dict)

    # a private function to load all the words to be prepared to check for pronunciations
    def _load_words_in_file(self, words_pron_dict:str):
        # opening the file as read
        with open(words_pron_dict, 'r') as file:
            # for every line in the file
            for line in file:
                # if the line doesn't start with ;;;
                if not line.startswith(';;;'):
                    # define a key value by splitting the line in spaces
                    key, val = line.split('  ', 2)
                    # find all matching regex
                    self._l[key] = re.findall(r"[A-Z]+",val)

    # a function to get all the pronunciations
    def get_pronunciations_and_prepare(self, str_input):
        # define a list of pronunciations
        list_pron = []
        # for every word in the words found by the regex
        for word in re.findall(r"[\w']+",str_input.upper()):
            # if the word is in the list
            if word in self._l:
                # add that word to the list of pronunciations
                list_pron += self._l[word]
        # print the list of pronunciations
        print(list_pron)
        # setup a delay for the speaking of each pronunciation
        delay=0
        # for every pronunciation in the list_pon
        for pron in list_pron:
            # start a new thread that calls the function _play_audio and pass the pronunciation and the delay as an argument
            _thread.start_new_thread(PythonTextToSpeachITEAM._play_pronunciation_audio, (pron, delay,))
            # increment the delay by 0.150
            delay += 0.150

    # a private function to play the sound of each pronunciation
    def _play_pronunciation_audio(sound, delay):
        try:
            time.sleep(delay)
            # open the wav file that is located inside the sounds/ and the name of that pronunciation . wav
            wf = wave.open("sounds/"+sound+".wav", 'rb')
            # play that audio
            p = pyaudio.PyAudio()
            # open a stream that has the format if the width and the channels and get an output
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            # reading the data from the Speaking.CHUNK
            data = wf.readframes(PythonTextToSpeachITEAM.CHUNK)

            # while there's data
            while data:
                # write that data
                stream.write(data)
                # re read the frames
                data = wf.readframes(PythonTextToSpeachITEAM.CHUNK)

            # stop the stream
            stream.stop_stream()
            # close the stream
            stream.close()

            p.terminate()
            return
        except:
            pass
    
 
 
# the main function
if __name__ == '__main__':
    # invoke the class to run
    tts = PythonTextToSpeachITEAM()
    # infinte loop to always get the user input for more sentences/words to say
    while True:
        tts.get_pronunciations_and_prepare(input('Enter a word or a sentence: '))
