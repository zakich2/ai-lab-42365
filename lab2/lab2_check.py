# lab2_check.py - assertions + noisy-sequence test around 26 C
# Run: python lab2_check.py
from lab2_model import StatefulClassroomAgent

# ---- 1. correctness checks -------------------------------------------------
a = StatefulClassroomAgent()
assert a.act(29, True) == ("COOL", True)
assert a.act(29, True) == ("COOL", False)    # repeated -> no command
assert a.act(20, True) == ("IDLE", True)     # boundary 20 is IDLE
assert a.act(26, True) == ("IDLE", False)    # boundary 26 is IDLE
assert a.act(19, True) == ("WARM", True)
assert a.act(29, False) == ("ECO", True)     # empty room priority
assert a.act(29, False) == ("ECO", False)
print("Correctness checks passed")

# ---- 2. noisy sequence: memory alone is NOT hysteresis ---------------------
noisy = [26.2, 25.8, 26.3, 25.7, 26.4, 25.6]
a = StatefulClassroomAgent()
sent = 0
print("\nNoisy sequence around 26 C (occupied room), plain stateful agent")
for t in noisy:
    target, send = a.act(t, True)
    sent += send
    print(t, target, "SEND" if send else "no-command")
print("Commands sent:", sent, "of", len(noisy), "readings -> flapping")

# ---- 3. proposed improvement: hysteresis band ------------------------------
class HysteresisAgent(StatefulClassroomAgent):
    """Start cooling above 26, but keep cooling until temp <= 25."""
    def target_mode(self, temp, occupied):
        if not occupied:
            return "ECO"
        if self.previous_mode == "COOL" and temp > 25:
            return "COOL"
        return super().target_mode(temp, occupied)

h = HysteresisAgent()
sent = 0
print("\nSame noisy sequence, hysteresis agent (stop cooling at <= 25 C)")
for t in noisy:
    target, send = h.act(t, True)
    sent += send
    print(t, target, "SEND" if send else "no-command")
print("Commands sent:", sent, "of", len(noisy), "readings")
