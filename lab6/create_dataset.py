# create_dataset.py - writes corpus.json and queries.json (5 synthetic documents, 10 labelled queries)
# Run once: python create_dataset.py     (refuses to overwrite existing files)
# ALL TEXT IS SYNTHETIC TEACHING DATA, NOT REAL UNIVERSITY OR COMPANY POLICY.
import json
from pathlib import Path

docs = {
"late": (
 "Assessment Handbook, Section 4 (synthetic teaching text). Coursework deadlines are published on the "
 "learning portal at the start of each semester and apply to every enrolled student unless a written "
 "exception is granted. Late submission is normally penalized by ten percent of the available marks for "
 "each calendar day after the deadline, and work more than three days late is not marked. Illness "
 "extensions require medical evidence before the deadline. Evidence must be a signed certificate from a "
 "registered doctor that names the dates of illness, and the coordinator will not accept certificates that "
 "are handwritten on plain paper or submitted after the deadline has passed unless the student was "
 "hospitalised. Students who cannot obtain a certificate in time should contact the coordinator by email "
 "on the same day so that a provisional extension of up to forty-eight hours can be recorded while "
 "evidence is gathered. Group projects follow the same rule, but every member must provide evidence "
 "separately. Extensions never apply to quizzes that are held during class time, because those "
 "assessments are completed in a single supervised session. Appeals about penalties must be made within "
 "seven days of the published mark."),
"password": (
 "IT Service Guide, Account Access (synthetic teaching text). Every student and staff member receives one "
 "university account that is used for email, the learning portal and the campus wireless network. Reset a "
 "forgotten password using the recovery link. The link is shown on the login page and sends a one-time code "
 "to the mobile number or alternate email address that was registered during enrolment, and the code stays "
 "valid for fifteen minutes before it expires and a new request is needed. Never share recovery codes with "
 "anyone, including staff who claim to work for the help desk, because genuine staff will never ask for "
 "them. If the registered mobile number is no longer in use, the recovery link cannot send a code, and the "
 "person must visit the IT counter in the main library with a photo identity card so that the contact "
 "details can be updated before a reset is possible. Accounts are locked for thirty minutes after five "
 "failed sign-in attempts, and a locked account cannot be reset until the lock period has ended. New "
 "passwords must contain at least twelve characters and must not repeat any of the previous five passwords."),
"assignment": (
 "Submission Guide (synthetic teaching text). Most courses collect coursework electronically so that every "
 "submission receives a timestamp and a receipt. Upload assignments through the learning portal. Each "
 "upload page lists the accepted file types, the maximum file size and the closing time, and the portal "
 "sends a confirmation email within a few minutes of a successful upload. Submit the final file as a PDF "
 "unless the course outline names a different format, and keep the receipt until the marks are published. "
 "Emailed submissions are not accepted, except when the portal has been unavailable for more than two hours "
 "before the deadline and the coordinator has announced a temporary alternative in writing. Several files "
 "may be uploaded for one assignment, but only the most recent upload before the closing time is marked, so "
 "students who correct a mistake must upload the complete work again rather than a single replacement page. "
 "Source code must be submitted as a single zip archive that does not contain virtual environments or "
 "private credentials. Late uploads remain possible for twenty-four hours after the closing time and are "
 "marked with a fifteen percent deduction."),
"contractor": (
 "Workplace Policy, Remote Work (synthetic teaching text). The organisation supports flexible working where "
 "the role allows it and where service levels are protected. Employees may request remote work with manager "
 "approval, and an approved arrangement can last up to six months before it is reviewed. Contractors can "
 "work remotely only if the signed contract permits it. Employee rules do not apply to contractors, because "
 "contractors are engaged through separate agreements that define the place of work, the working hours and "
 "the equipment they must use. A contractor whose agreement is silent about remote work must attend the "
 "office until the contract manager confirms a change in writing, and verbal permission from a team lead is "
 "not sufficient. All remote workers must use the company laptop and the approved virtual private network "
 "when they open internal systems, and personal devices may be used only for video meetings that do not "
 "display confidential files. Remote work from another country requires separate approval from the legal "
 "team and is never granted automatically, even for employees who already have an approved arrangement."),
"printer": (
 "Equipment Troubleshooting, Office Printers (synthetic teaching text). Office printers are shared between "
 "teams, so a fault should be reported to the help desk once the first checks have been completed. For "
 "blank printer pages, check ink levels and run the cleaning utility. Print a test page afterwards to "
 "confirm that the nozzles are working, and repeat the cleaning utility no more than twice because each "
 "cleaning cycle uses a noticeable amount of ink. Warning: switch the printer off and unplug it before "
 "opening any cover, and never touch the metal rollers or the heating unit, which stay hot for several "
 "minutes after printing. If the test page is still blank after two cleaning cycles, replace the ink "
 "cartridge with one that is approved for the printer model, since third-party cartridges are a frequent "
 "cause of empty output. Scanners and copiers use different procedures, and a blank scanner image is "
 "normally caused by a document placed face up or by the wrong scanning source being selected, so the "
 "printer steps should not be applied to scanners. Paper jams must be cleared only by following the "
 "diagram inside the front cover."),
}
evidence = {
 "late": "Illness extensions require medical evidence before the deadline.",
 "password": "Reset a forgotten password using the recovery link.",
 "assignment": "Upload assignments through the learning portal.",
 "contractor": "Contractors can work remotely only if the signed contract permits it.",
 "printer": "For blank printer pages, check ink levels and run the cleaning utility.",
}
questions = [   # (query, doc, split) - 4 dev + 4 test answerable, 2 unanswerable
 ("What is required for illness extensions?", "late", "dev"),
 ("How do I reset a forgotten password?", "password", "dev"),
 ("Where do I upload assignments?", "assignment", "dev"),
 ("Can contractors work remotely?", "contractor", "dev"),
 ("What do I do for blank printer pages?", "printer", "test"),
 ("How can I recover my login access?", "password", "test"),
 ("How should I hand in my coursework?", "assignment", "test"),
 ("What proof is needed when I was ill?", "late", "test"),
 ("What are tomorrow's flight prices?", None, "test"),
 ("Who won the football match?", None, "test"),
]
queries = [dict(query=q, doc=d, evidence=evidence[d] if d else None, split=s) for q, d, s in questions]

for d, t in docs.items():
    assert evidence[d] in t, d
    assert 150 <= len(t.split()) <= 250, (d, len(t.split()))

for name, data in [("corpus.json", docs), ("queries.json", queries)]:
    if Path(name).exists():
        raise FileExistsError("Refusing to overwrite " + name)
    Path(name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Created corpus.json and queries.json")
for d, t in docs.items():
    print(d, "words:", len(t.split()))
