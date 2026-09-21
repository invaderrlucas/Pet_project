import random
from enum import Enum
#this is a placeholder meant to be overhall in later iteration.
class Personality(Enum):
    confident = 1
    out_going = 2
    friendly  = 3
    shy       = 4
    lazy      = 5
    funny     = 6 



class Robot_Persona:
    

    def __init__(self, birthday , name ):
        self.persona = personality_rand()
        self.birthday = birthday
        self.name = name
    def returnInfo(self):
        info_template = "Hi my name is {0}, personality is {1} and my birthday {2}"
        
        return info_template.format(self.name, self.persona, self.birthday )

def personality_rand():
    return Personality(random.randint(1,6))
    