import math, random, time
import pygame

BG = (8, 8, 16)
EYE = (120, 220, 255)

# target eye height per state
EYE_HEIGHT = {"idle": 160, "listening": 200, "thinking": 70,
              "talking": 160, "sleeping": 10, "blushing" : 80, "Crying" : 80
              , "Sickly" : 10}

class Face:
    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = screen.get_size()
        self.state = "idle"
        self.eye_h = 160.0
        self.gaze = [0.0, 0.0]          # current, -1..1
        self.gaze_target = [0.0, 0.0]
        self.next_blink = time.time() + random.uniform(2, 5)
        self.blink_start = None
        self.next_glance = time.time() + random.uniform(2, 5)

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.gaze_target = [0.0, 0.3] if state == "sleeping" else [0.0, 0.0]

    def look_at(self, x, y):           # normalized -1..1
        self.gaze_target = [x, y]

    def blink(self, now):
        if self.state == "sleeping":
            return 1.0
        if self.blink_start is None and now >= self.next_blink:
            self.blink_start = now
        if self.blink_start is not None:
            t = (now - self.blink_start) / 0.18
            if t >= 1:
                self.blink_start = None
                self.next_blink = now + random.uniform(2, 6)
                return 1.0
            return 1 - math.sin(math.pi * t)   # close and reopen
        return 1.0

    def update(self, dt):
        now = time.time()
        target = EYE_HEIGHT[self.state]
        if self.state == "talking":
            target += 25 * math.sin(now * 12)
        if self.state == "thinking":
            self.gaze_target = [0.6 * math.sin(now * 1.5), -0.5]
        if self.state == "idle" and now >= self.next_glance:
            # look around now and then, return to center half the time
            if random.random() < 0.5:
                self.gaze_target = [random.uniform(-0.7, 0.7), random.uniform(-0.3, 0.3)]
            else:
                self.gaze_target = [0.0, 0.0]
            self.next_glance = now + random.uniform(2, 5)
        if self.set_state == "blush" :
            self.gaze_target = [0.0, 0.0]

        
        # ease toward targets so changes look smooth
        self.eye_h += (target - self.eye_h) * min(1, dt * 10)
        for i in (0, 1):
            self.gaze[i] += (self.gaze_target[i] - self.gaze[i]) * min(1, dt * 6)
        self.blink_factor = self.blink(now)

    def draw(self):
        self.screen.fill(BG)
        h = max(6, self.eye_h * self.blink_factor)
        ew = 140
        cx = self.w / 2 + self.gaze[0] * 60
        cy = self.h / 2 + self.gaze[1] * 40
        for dx in (-130, 130):
            rect = pygame.Rect(0, 0, ew, h)
            rect.center = (cx + dx, cy)
            pygame.draw.rect(self.screen, EYE, rect,
                             border_radius=int(min(ew, h) / 2.5))