from core.report import Report
from collections import defaultdict
from model.student import Student
from model.classroom import Classroom
import os

class Annual(Report):

    def __init__(self, classrooms, year=None):
        self._classrooms = classrooms
        self._year       = year

        years      = sorted(set(c._year for c in self._classrooms if c._year))
        year_label = ", ".join(years) if years else "N/A"
        super().__init__(f"Annual School Report - {year_label}")
        self._lines = []

    def generate_report(self):
        if not self._classrooms:
            print("  No classrooms found for the selected year.")
            return

        sep          = "=" * 60
        all_students = [s for c in self._classrooms for s in c.students]

        if not all_students:
            print("  No students found for the selected year.")
            return
        total        = len(all_students)
        passed       = sum(1 for s in all_students if s.is_passing())
        overall      = round(sum(s.overall_average() for s in all_students) / total, 2) if total else 0

        years      = sorted(set(c._year for c in self._classrooms if c._year))
        year_label = ", ".join(years) if years else "N/A"

        self._lines = [
            sep,
            f"       ANNUAL SCHOOL REPORT - {year_label}",
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

        for c in self._classrooms:
            if not c.students:
                continue
            top = max(c.students, key=lambda s: s.overall_average())
            self._lines.append(
                f"  {c.class_id:<8} {len(c.students):>9} "
                f"{c.class_average():>7.1f} {c.pass_rate():>6.1f}% "
                f"  {top.name:<22} ({top.overall_average():.1f})"
            )

        grade_dist = {}
        for s in all_students:
            g = s.grade_letter()
            grade_dist[g] = grade_dist.get(g, 0) + 1

        self._lines += [sep, "  GRADE DISTRIBUTION", "  " + "-" * 35]
        for grade in ["A", "B", "C", "D", "E", "F"]:
            count = grade_dist.get(grade, 0)
            self._lines.append(f"  {grade:<4}  {count:>3}")

        self._lines.append(sep)
        return "\n".join(self._lines)

    def content_report(self):
        if not self._lines:
            self.generate_report()
        if not self._lines:
            return ""
        return "\n".join(self._lines)

    def save_to_file(self):
        years      = sorted(set(c._year for c in self._classrooms if c._year))
        year_label = "_".join(y.replace("-", "_") for y in years) if years else "unknown"

        base_dir     = os.path.dirname(os.path.abspath(__file__))      # .../src/report
        project_root = os.path.dirname(os.path.dirname(base_dir))       # .../SMAP_DEVELOP
        file_path    = os.path.join(project_root, "outputs", "report", "annual", f"annual_report_{year_label}.txt")

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.content_report())
        print(f"Annual Report saved to: {file_path}")


if __name__ == '__main__':
    myStudent = Student("Devit", "s002", "Male", "23/07/2006", "devit@gmail.com", "ci0007", 2)
    demo  = Classroom("ci001", "10a", "a001", "t004", 30, "2025-2026")
    demo2 = Classroom("ci002", "10a", "a001", "t004", 30, "2025-2026")
    demo.add_student(myStudent)
    test = Annual([demo, demo2])
    print(test.generate_report())
    test.save_to_file()