import getpass 
import datetime
from personality.personality import Robot_Persona
from conversation.llm_pipeline import sendMessage
#prototype messaging
def main() -> None:
    name = getpass.getuser()
    birthday_pet = datetime.datetime.now()
    person = Robot_Persona(birthday_pet,name)
    intro = "you're " + str(person.name) + " and you're " + str(person.persona) + " please respond approapriately"
    sendMessage(intro)
    while True:
        message = input("type message here : ")
        sendMessage(message)
if __name__ == "__main__":
    main()