from model.classroom import Classroom
from core.report import Report
from model.student import Student



class ClassReport(Report):
    """Class-level report — overrides generate_report (Polymorphism)."""

    def __init__(self, classroom):
        super().__init__(f"Class Report - {classroom.getClassId}")
        self._classroom = classroom
        self._lines = None
      

    def generate_report(self):
        cls = self._classroom
        sep = "=" * 60
        subj_avgs = cls.subject_averages()

        self._lines = [
            sep,
            f"       CLASS REPORT — {cls.getClassId} - {cls.class_level}",
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
            bar = "█" * int(avg / 5)
            self._lines.append(f"  {subj:<14} {avg:>6.1f}  {bar}")

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
    def save_to_file(self, filepath):
        pass



if __name__ == '__main__':
    myStudent = Student("devit", "s002", "Male", "23/07/2006", "devit@gamil.com", "ci0007",2)
    demo = Classroom("ci001", "10a", "a001", "t004", 30, "2025-2026")
    demo.addStudent(myStudent)
    # print(demo.len)
    test_report_class = ClassReport(demo)
    print(test_report_class.content_report())
