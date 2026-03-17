from model.student import Student, SUBJECTS


class Classroom:
    def __init__(self, class_id, class_level, room, homeroom_teacher, capacity, year):
        self._class_id = class_id
        self._room = room
        self._class_level = class_level
        self._homeroom_teacher = homeroom_teacher
        self._students = []  # list of student
        self._capacity = capacity
        self._year = year

    @property
    def class_id(self):
        return self._class_id
    
    @property
    def class_level(self):
        return self._class_level

    @class_id.setter
    def class_id(self, new_class_id):
        if new_class_id:
            self._class_id = new_class_id
        raise ValueError("Class ID should not empty")

    @property
    def students(self):
        return self._students

    # add student
    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("Only Student instances allowed")
        if student in self._students:
            raise ValueError(f"Student {student.student_id} already in class")
        self._students.append(student)  # otherwise append

    def remove_student(self, student_id):
        sizestudents = len(self._students)
        self._students = [s for s in self._students if s.student_id != student_id]
        return (
            len(self._students) < sizestudents
        )  # true if remove student from the class succeed

    def get_student(self, student_id):
        for s in self._students:
            if s.person_id == student_id:
                return s
        return None

    def class_average(self):
        if not self._students:
            return 0.0
        total = sum(s.overall_average() for s in self._students)
        return round(total / len(self._students), 2)

    def top_students(self, n=3):
        return sorted(self._students, key=lambda s: s.overall_average(), reverse=True)[:n]

    def failing_students(self):
        return [s for s in self._students if not s.is_passing()]

    def pass_rate(self):
        if not self._students:
            return 0.0
        passed = sum(1 for s in self._students if s.is_passing())
        return round(passed / len(self._students) * 100, 1)

    def subject_averages(self):
        result = {}
        for subject in SUBJECTS:
            scores = [
                s.subject_average(subject)
                for s in self._students
                if subject in s.scores
            ]
            result[subject] = round(sum(scores) / len(scores), 2) if scores else 0.0
        return result

    # Magic methods
    def iter(self):
        return iter(self._students)
    
    @property
    def len(self):
        return len(self._students)

    def getitem(self, index):
        return self._students[index]

    def contains(self, student):
        return student in self._students



if __name__ == "__main__":
    myStudent = Student("devit", "s002", "Male", "23/07/2006", "devit@gamil.com", "ci0007", 12)
    demo = Classroom("ci001", "10a", "a001", "t004", 30, "2025-2026")
    demo.add_student(myStudent)
    print(f"Number of students in class: {demo.len}")
    print(f"Student name: {demo.get_student('s002').name}")