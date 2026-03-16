from core.report import Report
from model.student import Student
from model.classroom import Classroom


class Annual(Report):
    def __init__(self, classrooms):
        super().__init__("Annual School Report 2024–2025")
        self._classrooms = classrooms
        self._lines = []

    def generate_report(self):
        sep = "=" * 60
        line = "_" * 70
        all_students = [s for cls in self._classrooms for s in cls.students]
        total = len(all_students)
        passed = sum(1 for s in all_students if s.is_passing())
        overall = round(sum(s.overall_average() for s in all_students) / total, 2) if total else 0

        self._lines = [
            sep,
            "       ANNUAL SCHOOL REPORT — 2024/2025",
            sep,
            f"  Total Students  : {total}",
            f"  Passed          : {passed}  ({passed / total * 100:.1f}%)" if total else "  Passed: 0",
            f"  Failed          : {total - passed}",
            f"  School Average  : {overall:.2f}",
            sep,
            "  CLASS SUMMARY",
            f"  {'Class':<8} {'Students':>9} {'Avg':>7} {'Pass%':>7} {'Top Student':<22}",
            "  " + "-" * 58,
        ]

        for cls in self._classrooms:
            if not cls.students:
                continue
            top = max(cls.students)
            self._lines.append(
                f"  {cls.getClassId:<8} {len(cls.students):>9} "
                f"{cls.class_average():>7.1f} {cls.pass_rate():>6.1f}% "
                f"  {top.name:<22} ({top.overall_average():.1f})"
            )

        # Grade distribution across all students
        grade_dist: dict[str, int] = {}
        for s in all_students:
            g = s.grade_letter()
            grade_dist[g] = grade_dist.get(g, 0) + 1

        self._lines += [sep, "  GRADE DISTRIBUTION", "  " + "-" * 35]
        for grade in ["A+", "A", "B", "C", "D", "F"]:
            count = grade_dist.get(grade, 0)
            bar = "█" * count
            self._lines.append(f"  {grade:<4}  {count:>3}  {bar}")

        self._lines.append(sep)
        return "\n".join(self._lines)  # returns the result

    def content_report(self):  #properly indented inside class
        if not self._lines:
            self.generate_report()
        return "\n".join(self._lines)

    def save_to_file(self, file_path):  # properly indented inside class
        pass


if __name__ == '__main__':
    myStudent = Student("devit", "s002", "Male", "23/07/2006", "devit@gmail.com", "ci0007", 2)
    demo = Classroom("ci001", "10a", "a001", "t004", 30, "2025-2026")
    demo2 = Classroom("ci002", "10a", "a001", "t004", 30, "2025-2026")
    demo.addStudent(myStudent)

    test_report_annual = Annual([demo, demo2])
    print(test_report_annual.generate_report())  # ✅ now prints actual content