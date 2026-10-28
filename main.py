import getpass 
import datetime
from pathlib import Path
from personality.personality import Robot_Persona
from conversation.llm_pipeline import sendMessage, ollama_start
from input.wakeword import wakework_detection, stream
from input.record import record_until_silence, transcribe
#prototype messaging

def main() -> None:
    #ollama_start()
    intro = ""
    memory = Path("/conversation/memory.txt")
    if memory.is_file():
        memory = memory
    else: 
        name = getpass.getuser()
        birthday_pet = datetime.datetime.now()
        person = Robot_Persona(birthday_pet,name)
        intro = "you're " + str(person.name) + " and you're " + str(person.persona) + "your birthday is " + str(person.birthday) + " please respond approapriately"
    sendMessage(intro,True)
    state = 0
    while True:
        match state:
            case 0: #idle wakeword
                if wakework_detection():
                   state = 1
                
            case 1: #wakeword activated and listening for commands
                listened_text = transcribe(record_until_silence(stream))
                print(listened_text)
                sendMessage(listened_text,True)
                state = 0
            




if __name__ == "__main__":
    main()