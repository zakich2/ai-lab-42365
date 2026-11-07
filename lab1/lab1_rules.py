# lab1_rules.py - transparent rule-based scholarship screener (extended)
# Run: python lab1_rules.py
# ALL THRESHOLDS ARE SYNTHETIC LAB ASSUMPTIONS, NOT REAL SCHOLARSHIP POLICY.
# "Review" only flags an application for a human reviewer; it is NOT an award.

MIN_SCORE = 70        # original condition (synthetic)
MIN_ATTENDANCE = 75   # new condition 1: attendance_ok (synthetic, percent)

def screen(score, complete, attendance, has_disciplinary_record):
    """Return (decision, reason). Every rule is explicit and named."""
    failed = []
    if score < MIN_SCORE:
        failed.append("score_ok failed (score < 70)")
    if not complete:
        failed.append("documents_complete failed")
    if attendance < MIN_ATTENDANCE:                      # new condition 1
        failed.append("attendance_ok failed (attendance < 75)")
    if has_disciplinary_record:                          # new condition 2
        failed.append("clean_record failed (disciplinary record present)")
    if failed:
        return "Hold", "; ".join(failed)
    return "Review", "all four conditions satisfied"

# (name, (score, complete, attendance, has_disciplinary_record), expected, why chosen)
TESTS = [
    ("pass",            (82, True, 90, False), "Review", "all conditions clearly met"),
    ("low_attendance",  (82, True, 60, False), "Hold",   "only attendance_ok fails"),
    ("disciplinary",    (82, True, 90, True),  "Hold",   "only clean_record fails"),
    ("boundary",        (70, True, 75, False), "Review", "score and attendance exactly on thresholds"),
]

if __name__ == "__main__":
    print("NOTE: thresholds are synthetic lab assumptions.")
    all_ok = True
    for name, inp, expected, why in TESTS:
        actual, reason = screen(*inp)
        ok = actual == expected
        all_ok &= ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
        print(f"   input    : score={inp[0]}, complete={inp[1]}, attendance={inp[2]}, record={inp[3]}")
        print(f"   expected : {expected}")
        print(f"   actual   : {actual}")
        print(f"   reason   : {reason}")
        print(f"   why case : {why}")
    print("ALL TESTS PASSED" if all_ok else "SOME TESTS FAILED")
    