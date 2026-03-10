from core.report import Report
from model.student import Student
from model.classroom import Classroom
class Annual(Report):
 def __init__(self, classrooms:list[Classroom]):
  super().__init__("Annual School Report 2024–2025")
  self._classrooms = classrooms
  self._lines =[]
 def generate_report(self):
  sep = "="*60
  line ="_"*70
  all_student = [s for cls in self._classrooms for s in cls]
  total = len(all_student)
  passed= sum(1 for s in all_student if s.is_passing())
  overall = round(sum(s.overall_average() for s in all_student) / total, 2) if total else 0

  self._lines = [
      sep,
      "       ANNUAL SCHOOL REPORT — 2024/2025",
      sep,
      f"  Total Students  : {total}",
      f"  Passed          : {passed}  ({passed/total*100:.1f}%)" if total else "  Passed: 0",
      f"  Failed          : {total-passed}",
      f"  School Average  : {overall:.2f}",
      sep,
      "  CLASS SUMMARY",
      f"  {'Class':<8} {'Students':>9} {'Avg':>7} {'Pass%':>7} {'Top Student':<22}",
      "  " + "-" * 58,
  ]
  for cls in self._classrooms:
      if not cls.students: continue
      top = max(cls.students)
      self._lines.append(
          f"  {cls.class_id:<8} {len(cls):>9} "
          f"{cls.class_average():>7.1f} {cls.pass_rate():>6.1f}% "
          f"  {top.name:<22} ({top.overall_average():.1f})"
      )


  
  
