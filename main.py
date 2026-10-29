import getpass 
import datetime
import time
from pathlib import Path
from personality.personality import Robot_Persona
from conversation.llm_pipeline import sendMessage, ollama_start, load_memory, save_memory, payload 
from input.wakeword import wakework_detection, stream
from input.record import record_until_silence, transcribe
import threading, queue
import pygame
from animation.face import Face
from output.speech import speak
from input.wakeword import wakework_detection, stream, flush_stream


#prototype messaging
events = queue.Queue()
def voice_loop(persona):
    state = 0
    while True:
        match state:
            case 0:
                if wakework_detection():
                    events.put(("state", "listening"))
                    state = 1
            case 1:
                listened_text = transcribe(record_until_silence(stream))
                print(listened_text)
                stream.stop_stream()
                if listened_text:
                    reply = sendMessage(listened_text, False)
                    speak(reply)
                flush_stream()
                state = 0

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
        intro = sendMessage(intro, False)
        
        save_memory(persona)
    threading.Thread(target=voice_loop, args=(persona,), daemon=True).start()

    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.mouse.set_visible(False)
    face = Face(screen)
    clock = pygame.time.Clock()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                return
        while not events.empty():
            kind, value = events.get_nowait()
            if kind == "state":
                face.set_state(value)
            elif kind == "look":
                face.look_at(*value)
        face.update(clock.tick(30) / 1000)
        face.draw()
        pygame.display.flip()
                
            




if __name__ == "__main__":
    main()