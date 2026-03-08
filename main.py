# from core.report import greeting
# from core.person import greet
# greeting()
# greet()




from model.student import Student, SUBJECTS, PASS_MARK
from report.transcript_report import TranscriptReport

# --- Create a mock student ---
student = Student(
    person_id="S001",
    name="Devit Test",
    class_id="2A",
    gender="Male",
    dob="2008-05-01",
    email="devit@test.com"
)

# Mock some attendance and scores
student._attendance = 45
student._total_day = 50

# Mock subject scores for testing
# Assuming Student class has a dictionary or similar for scores
student.scores = {
    "Math": [80, 90],
    "English": [70, 75],
    "Science": [50, 60],  # maybe failing
    "History": [85, 90]
}

# --- Create transcript report ---
report = TranscriptReport(student)

# --- Generate report ---
report.generate_report()

# --- Print report content ---
print(report.content_report())
