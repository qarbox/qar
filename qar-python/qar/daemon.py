
import time

last_sleep = None

def sleep_up_to(seconds):
    global last_sleep

    now = time.time()

    if last_sleep is None:
        sleep_time = seconds
    else:
        elapsed = now - last_sleep
        sleep_time = seconds - elapsed
    
    last_sleep = now

    if sleep_time > 0:
        time.sleep(sleep_time)

class Daemon:
    def run(self):
        while self.running:
            self.tick()
            sleep_up_to(5)
    
    def tick(self):
        self.tick_update()
        self.tick_docker()
