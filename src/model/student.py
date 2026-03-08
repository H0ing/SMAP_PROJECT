from core.person import Person
SUBJECTS   = ("Math", "Physics", "Chemistry", "Biology", "History", "Literature", "English")
CLASS_LEVELS  = ("10A", "10B", "11A", "11B", "12A", "12B")
PASS_MARK  = 50.0
class Student(Person):
    def __init__(self, name, person_id, gender, dob, email, class_level):
        super().__init__(name, person_id, gender)
        self._class_level=class_level
        self._dob=dob
        self._email=email
        self._score={s: [] for s in SUBJECTS}
        self._total_day=0
        self._attendance=0
    @property
    def class_id(self): return self.__class_id
    @class_id.setter
    def class_id(self, new_class_id):
        if not new_class_id:
            raise ValueError("Class id can not be empty!")
        self.__class_id=new_class_id
        
    @property
    def attendance(self):
        if self._total_day==0:
            return 0.0
        return round(self.attendance/self._total_day*100,1)
    @property
    def dob(self): return self._dob
    @dob.setter
    def dob(self, new_dob):
        if not new_dob:
            raise ValueError("Dob can not be empty!")
        self._dob=new_dob
    @property 
    def email(self): return self._email
    @email.setter
    def email (self, new_email):
        if not new_email:
            raise ValueError("Email can not be empty!")
        self._email=new_email
    @property
    def score(self): return self._score
    def set_attendance(self, day_present, total_day):
        try:
            if (day_present<0 or total_day<=0 or day_present>total_day):
                raise ValueError("Invalid attendance value")
            self._attendance=day_present
            self._total_day=total_day
        except ValueError as e:
            print(f"set_attendance failed: {e}")
        finally:
            print("Process set attnedace already execute")
    
    def add_score(self, subject, score):
        try:
            if subject not in self._score.keys():
                raise ValueError(f"Unknown subject: {subject}")
            if not (0<= score <=100):
                raise ValueError(f"Score must be 0-100, got {score}") 
            self._score[subject].append(round(float(score),1))
            print(f"Score added: {self.person_id} | {subject} | {score}")
        except ValueError as e:
            print(f"Add score failed: {e}")
        finally:
            print("Process add score already execute")
    def subject_average(self, subject):
        scores=self._scores.get(subject, [])
        if not scores:
            return 0
        return round(sum(scores) / len(scores), 1)
    def overall_average(self):
        if not self._scores:
            return 0
        averages=[]
        for subject in self._scores:
            averages.append(self.subject_average(subject))
        return round(sum(averages) / len(averages), 1)
    def is_passing(self):
        return self.overall_average()>=PASS_MARK
    def grade_letter(self, score=None):
        if score is None:
            score = self.overall_average()
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
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
            "name": self.name,
            "gender": self.gender,
            "dob": self.dob,
            "email": self.email,
            "class_id": self._class_level,
            "scores": self._scores,
            "attendance": self._attendance,
            "total_days": self._total_days
        }
    def __str__(self):
        avg = self.overall_average()
        return (f"Student({self.person_id}: {self.name} | "
                f"Class {self._class_id} | Avg {avg:.1f} {self.grade_letter()})")
  