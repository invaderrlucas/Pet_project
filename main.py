import getpass 
import datetime
from personality.personality import Robot_Persona
def main() -> None:
    name = getpass.getuser()
    birthday_pet = datetime.datetime.now()
    person = Robot_Persona(birthday_pet,name)

    
    print(person.returnInfo())
if __name__ == "__main__":
    main()