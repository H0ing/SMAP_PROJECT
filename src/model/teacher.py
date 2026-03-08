from core.person import Person


class Teacher(Person):
    def __init__(self, name, teacher_id, gender, subject, salary, room):
        super().__init__(name, teacher_id, gender)
        self._subject = subject
        self._salary = salary
        self._room = room

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, new_subject=None):
        if new_subject == None:
            raise ValueError("Subject can not be empty")
        self._subject = new_subject

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, new_salary=None):
        if new_salary == None:
            raise ValueError("Subject can not be empty")
        self._salary = new_salary

    @property
    def room(self):
        return self._room

    @room.setter
    def subject(self, new_room=None):
        if new_room == None:
            raise ValueError("Subject can not be empty")
        self._room = new_room

    def __str__(self):
        return (
            f"Teacher({self.person_id}: {self.name} | {self.__subject} | {self.__room})"
        )

    def to_dict(self):
        return {
            "teacher_id": self.teacher_id,
            "name": self.name,
            "gender": self.gender,
            "subject": self._subject,
            "salary": self._salary,
            "room": self._room,
        }
