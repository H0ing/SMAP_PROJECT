from core.person import Person

SUBJECTS = (
    "Math",
    "Physics",
    "Chemistry",
    "Biology",
    "History",
    "Literature",
    "English",
)
CLASS_LEVELS = ("10A", "10B", "11A", "11B", "12A", "12B")
PASS_MARK = 50.0


class Student(Person):
    def __init__(self, name, person_id, sex, dob, email, class_id, attendance=0, scores = []):
        super().__init__(name, person_id, sex)
        self._class_id=class_id
        self._dob=dob
        self._email=email
        self._attendance=attendance
        self._scores = scores

           
    @property
    def class_id(self): return self._class_id
    @class_id.setter
    def class_id(self, new_class_id):
        if not new_class_id:
            raise ValueError("Class id can not be empty!")
        self._class_id=new_class_id
    @property
    def attendance(self): return self._attendance
    @property
    def dob(self):
        return self._dob

    @dob.setter
    def dob(self, new_dob):
        if not new_dob:
            raise ValueError("Dob can not be empty!")
        self._dob = new_dob

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        if not new_email:
            raise ValueError("Email can not be empty!")
        self._email = new_email

    @property
    def scores(self): 
        return self._scores

    def add_score(self, subject, score):
        try:
            if subject not in self._scores.keys():
                raise ValueError(f"Unknown subject: {subject}")
            if not (0<= score <=100):
                raise ValueError(f"Score must be 0-100, got {score}") 
            self._scores[subject].append(round(float(score),1))
            print(f"Score added: {self.person_id} | {subject} | {score}")
        except ValueError as e:
            print(f"Add score failed: {e}")
        finally:
            print("Process add score already execute")

    def subject_average(self, subject):
        scores = self._scores.get(subject, [])
        if not scores:
            return 0
        return round(sum(scores) / len(scores), 1)

    def overall_average(self):
        if not self._scores:
            return 0
        averages = []
        for subject in self._scores:
            averages.append(self.subject_average(subject))
        return round(sum(averages) / len(averages), 1)

    def is_passing(self):
        return self.overall_average() >= PASS_MARK

    def grade_letter(self, score=None):
        if score is None:
            score = self.overall_average()
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        elif score >= 50:
            return "E"
        else:
            return "F"

    def failing_subjects(self):
        failing = []
        for subject in self._scores:
            if self._scores[subject] and self.subject_average(subject) < 50:
                failing.append(subject)
        return failing

    def to_dict(self):
        return {
            "student_id": self.person_id,
            "student_name": self.name,   
            "sex": self.sex,
            "dob": self.dob,
            "email": self.email,
            "class_id": self._class_id,
            "scores": self._scores,
            "attendance": self._attendance,
        }

    def __str__(self):
        avg = self.overall_average()
        return (
            f"Student({self.person_id}: {self.name} | "
            f"Class {self._class_id} | Avg {avg:.1f} {self.grade_letter()})"
        )
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['student_name'],
            person_id=data['student_id'],
            sex=data['sex'],
            dob=data['dob'],
            email=data['email'],
            class_id=data['class_id'],
            attendance=data.get('attendance', 0),
            scores= data.get('scores', {})
        )
