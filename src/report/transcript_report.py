from core.report import Report
from model.student import Student, SUBJECTS, PASS_MARK
import os

class TranscriptReport(Report):
    def __init__(self,student , year):
        super().__init__(f"Transcript - {student.name}")
        self._student=student
        self._year = year
        self._lines=[]
    def generate_report(self):
        s=self._student
        line= "-" * 45
        sep= "=" *50
        self._lines=[
            sep,
            "        OFFICIAL STUDENT TRANSCRIPT",
            f"        Academic Year {self._year}",
            sep,
            f" Name          : {s.name}",
            f" Student ID    : {s.person_id}",
            f" Class         : {s.class_id}",
            f" Sex           : {s.sex}",
            f" Date of Birth : {s.dob}",
            f" Email         : {s.email}",
            f" Attendance    : {s.attendance}%",
            sep,
            f"  {'Subject':<12} {'Avg':>7}  {'Grade':>10}  Status",
            "  "+line,
        ]
        for subject in SUBJECTS:
            avg=s.subject_average(subject)
            grade=s.grade_letter(avg)
            status="PASS" if avg>= PASS_MARK else "FAIL"
            self._lines.append(f"  {subject:<12} {avg:>8} {grade:>6} {status:>9}")
        fail_sub=s.failing_subjects()
        overall_avg = s.overall_average()  
        self._lines += [
            "  " + line,
            f"  Overall Average : {overall_avg:.2f}",   
            f"  Final Grade     : {s.grade_letter()}",
            f"  Result          : {'PASSED' if s.is_passing() else 'FAILED'}",
        ]
        if fail_sub:
            self._lines.append(f"  Failing Subjects: {', '.join(sorted(fail_sub))}")
    def content_report(self):
        if not self._lines:
            self.generate_report()
        return "\n".join(self._lines)
    
    def save_to_file(self):
        student_id = self._student.person_id
        class_id   = self._student.class_id
 
        base_dir     = os.path.dirname(os.path.abspath(__file__))       # .../src/report
        project_root = os.path.dirname(os.path.dirname(base_dir))       # .../SMAP_DEVELOP
        file_path    = os.path.join(
            project_root, "outputs", "report", "transcript",
            f"{student_id}_{class_id}.txt"
        )
 
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
 
        with open(file_path, "w") as f:
            f.write(self.content_report())
 
        print(f"Transcript saved → {file_path}")

if __name__ == "__main__":
    s = Student(
        name="Devit",
        person_id="S001",
        class_id="A1",
        sex="M",
        dob="2005-01-01",
        email="devit@test.com",
        attendance=90
    )
    s.scores = {
        "Math": [80, 90],
        "English": [70, 75],
        "Physics": [50, 60]
    }
    rpt = TranscriptReport(s)
    rpt.generate_report()
    print(rpt.content_report())
    rpt.save_to_file("transcript_test.txt")
    print("File saved as transcript_test.txt")
    rpt.save_to_file()
    
    
    
    
    
