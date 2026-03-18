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

        # Collect all unique years from all classrooms
        years = sorted(set(c._year for c in self._classrooms if c._year))
        year_label = ", ".join(years) if years else "N/A"

        all_students = [s for cls in self._classrooms for s in cls.students]
        total  = len(all_students)
        passed = sum(1 for s in all_students if s.is_passing())
        overall = round(sum(s.overall_average() for s in all_students) / total, 2) if total else 0

        self._lines = [
            sep,
            f"       ANNUAL SCHOOL REPORT — {year_label}",  # shows all years
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
            # Bug 1 fixed: max() needs a key, otherwise it uses __lt__ which may not exist
            top = max(cls.students, key=lambda s: s.overall_average())
            self._lines.append(
                f"  {cls.class_id:<8} {len(cls.students):>9} "
                f"{cls.class_average():>7.1f} {cls.pass_rate():>6.1f}% "
                f"  {top.name:<22} ({top.overall_average():.1f})"
            )

        # Grade distribution across all students
        grade_dist: dict[str, int] = {}
        for s in all_students:
            g = s.grade_letter()
            grade_dist[g] = grade_dist.get(g, 0) + 1

        self._lines += [sep, "  GRADE DISTRIBUTION", "  " + "-" * 35]

        for grade in ["A", "B", "C", "D", "E", "F"]:
            count = grade_dist.get(grade, 0)
            self._lines.append(f"  {grade:<4}  {count:>3} ")

        self._lines.append(sep)
        return "\n".join(self._lines)

    def content_report(self):
        if not self._lines:
            self.generate_report()
        return "\n".join(self._lines)

    def save_to_file(self, filepath=None):
        import os
        years = sorted(set(c._year for c in self._classrooms if c._year))
        year_label = "_".join(years) if years else "unknown"

        if filepath is None:
            filepath = f"./outputs/reports/annual_report_{year_label}.txt"

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        content = self.content_report()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Annual report saved to: {filepath}")


if __name__ == '__main__':
    myStudent = Student("Devit", "s002", "Male", "23/07/2006", "devit@gmail.com", "ci0007", 2)
    demo  = Classroom("ci001", "10a", "a001", "t004", 30, "2025-2026")
    demo2 = Classroom("ci002", "10a", "a001", "t004", 30, "2025-2026")
    demo.add_student(myStudent)
    test = Annual([demo, demo2])
    print(test.generate_report())
    test.save_to_file()