from core.report import Report
from model.student import Student, SUBJECTS, PASS_MARK
class TranscriptReport(Report):
    def __init__(self,student : Student):
        super().__init__(f"Transcript - {student.name}")
        self._student=student
        self._lines=[]
    def generate_report(self):
        s=self._student
        line= "-" * 45
        sep= "=" *50
        self._lines=[
            sep,
            "        OFFICIAL STUDENT TRANSCRIPT",
            "        Academic Year 2024–2025",
            sep,
            f" Name          : {s.name}",
            f" Student ID    : {s.person_id}",
            f" Class         : {s.class_id}",
            f" Gender        : {s.gender}",
            f" Date of Birth : {s.dob}",
            f" Email         : {s.email}",
            f" Attendance    : {s.attendance}%",
            sep,
            f"  {'Subject':<12} {'Avg':>10}  {'Grade':>7}  Status",
            "  "+line,
        ]
        for subject in SUBJECTS:
            avg=s.subject_average(subject)
            grade=s.grade_letter()
            status="PASS" if avg>= PASS_MARK else "FAIL"
            self._lines.append(f"  {subject:<12} {avg:>8} {grade:>6} {status:>9}")
        fail_sub=s.failing_subjects()
        self._lines+=[
            "  "+line,
            f"  Overall Average : {avg:.2f}",
            f"  Final Grade     : {s.grade_letter()}",
            f"  Result          : {'✅ PASSED' if s.is_passing() else '❌ FAILED'}",
        ]
        if fail_sub:
            self._lines.append(f"  Failing Subjects: {', '.join(sorted(fail_sub))}")
    def content_report(self):
        if not self._lines:
            self.generate_report()
        return "\n".join(self._lines)
