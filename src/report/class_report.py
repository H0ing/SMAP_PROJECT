from model.classroom import Classroom
from core.report import Report
from model.student import Student
import os



class ClassReport(Report):
    

    def __init__(self, classroom):
        super().__init__(f"Class Report - {classroom.class_id}")
        self._classroom = classroom
        self._lines = None
      

    def generate_report(self):
        cls = self._classroom
        sep = "=" * 60
        subj_avgs = cls.subject_averages()

        self._lines = [
            sep,
            f"       CLASS REPORT - {cls.class_id} - {cls.class_level}",
            f"       Academic Year {cls._year}",
            sep,
            f"  Total Students  : {cls.len}",
            f"  Class Average   : {cls.class_average():.2f}",
            f"  Pass Rate       : {cls.pass_rate():.1f}%",
            f"  Failing Students: {len(cls.failing_students())}",
            sep,
            "  SUBJECT AVERAGES",
            "  " + "-" * 35,
        ]
        for subj, avg in subj_avgs.items():
            self._lines.append(f"  {subj:<14} {avg:>6.1f}  ")

        self._lines += [sep, "  STUDENT RANKING (Top to Bottom)", "  " + "-" * 50]
        ranked = sorted(cls.students, reverse=True)
        for rank, st in enumerate(ranked, 1):
            avg = st.overall_average()
            self._lines.append(
                f"  {rank:>3}. {st.name:<20} {avg:>6.1f}  "
                f"{st.grade_letter():>3}  "
                f"{'Pass' if st.is_passing() else 'FAIL'}"
            )
        self._lines.append(sep)

    def content_report(self):
        if not self._lines:
            self.generate_report()
        return "\n".join(self._lines)
    def save_to_file(self):
        class_id = self._classroom.class_id
        class_level = self._classroom.class_level
        base_dir = os.path.dirname(os.path.abspath(__file__))      # give : SMAP_DEVELOP/src/report
        project_root = os.path.dirname(os.path.dirname(base_dir))  # give : SMAP_DEVELOP/
        file_path = os.path.join(project_root, "outputs", "report", "class", f"{class_id}_{class_level}.txt")

        # check the directory and create it if not exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True) 
    
        with open(file_path, 'w') as file:
            file.write(self.content_report())
            print(f"Class ID: {class_id} \n Class LevelL: {class_level} \n Class Report class save sucessfully.")



if __name__ == '__main__':
    myStudent = Student("devit", "s002", "Male", "23/07/2006", "devit@gamil.com", "ci0007",2)
    demo = Classroom("ci001", "10a", "a001", "t004", 30, "2025-2026")
    demo.add_student(myStudent)
    # print(demo.len)
    test_report_class = ClassReport(demo)
    print(test_report_class.content_report())
    test_report_class.save_to_file()

