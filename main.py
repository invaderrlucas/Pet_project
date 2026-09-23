import getpass 
import datetime
from pathlib import Path
from personality.personality import Robot_Persona
from conversation.llm_pipeline import sendMessage
#prototype messaging
def main() -> None:
    memory = Path("/conversation/memory.txt")
    if memory.is_file():
        memory = memory
    else: 
        name = getpass.getuser()
        birthday_pet = datetime.datetime.now()
        person = Robot_Persona(birthday_pet,name)
        intro = "you're " + str(person.name) + " and you're " + str(person.persona) + "your birthday is " + str(person.birthday) + " please respond approapriately"
    sendMessage(intro)
    while True:
        message = input("type message here : ")
        sendMessage(message)
if __name__ == "__main__":
    main()