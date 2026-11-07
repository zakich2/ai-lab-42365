# lab2_model.py - stateful classroom agent: remembers previous mode and
# only sends a command when the target mode CHANGES.
# Run: python lab2_model.py     (modes are simulated; no hardware is controlled)

class StatefulClassroomAgent:
    def __init__(self):
        self.previous_mode = None          # internal storage

    def target_mode(self, temp, occupied):
        if not occupied:                   # empty room has priority
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"                      # exactly 20 or 26 -> IDLE

    def act(self, temp, occupied):
        target = self.target_mode(temp, occupied)
        send_command = target != self.previous_mode
        self.previous_mode = target
        return target, send_command

if __name__ == "__main__":
    agent = StatefulClassroomAgent()
    percepts = [
        (29, True),    # first percept -> COOL, command sent
        (29, True),    # repeated percept -> no command
        (20, True),    # lower boundary -> IDLE
        (26, True),    # upper boundary -> IDLE (same mode, no command)
        (19, True),    # transition -> WARM
        (29, True),    # transition WARM -> COOL
        (29, False),   # empty room -> ECO
        (29, False),   # empty room again -> no command
    ]
    print("step | previous_mode | percept | target | command")
    for step, p in enumerate(percepts, 1):
        prev = agent.previous_mode
        target, send = agent.act(*p)
        print(step, prev, p, target, "SEND" if send else "no-command", sep=" | ")
