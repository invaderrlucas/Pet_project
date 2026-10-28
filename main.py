import getpass 
import datetime
from pathlib import Path
from personality.personality import Robot_Persona
from conversation.llm_pipeline import sendMessage, ollama_start, load_memory, save_memory, payload 
from input.wakeword import wakework_detection, stream
from input.record import record_until_silence, transcribe
#prototype messaging

def main() -> None:
    ollama_start()
    memory = load_memory()
    if memory:
        # returning pet: restore who it is and what was said
        persona = memory["persona"]
        payload["prompt"] = memory["history"]
        print(f"Welcome back, {persona['name']}")
    else:
        # first boot: create a persona once and keep it forever
        person = Robot_Persona(datetime.datetime.now(), getpass.getuser())
        persona = {
            "name": person.name,
            "personality": person.persona.name,   # e.g. "friendly"
            "birthday": person.birthday.isoformat(),
        }
        intro = (f"You're {persona['name']}, your personality is "
                 f"{persona['personality']} and your birthday is "
                 f"{persona['birthday']}. Please respond appropriately.")
        sendMessage(intro, False)
        save_memory(persona)
    state = 0
    while True:
        match state:
            case 0: #idle wakeword

                if wakework_detection():
                   state = 1
                
            case 1: #wakeword activated and listening for commands
                listened_text = transcribe(record_until_silence(stream))
                print(listened_text)
                sendMessage(listened_text,False)
                state = 0
                
            




if __name__ == "__main__":
    main()