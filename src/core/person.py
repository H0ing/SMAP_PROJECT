from abc import ABC, abstractmethod
from datetime import datetime


class Person(ABC):
    def __init__(self, name, person_id, sex):
        self.__name = name
        self.__person_id = person_id
        self.__sex = sex

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        if not new_name:
            raise ValueError("Name can not be empty!")
        self.__name = new_name

    @property
    def person_id(self):
        return self.__person_id

    @person_id.setter
    def person_id(self, new_id):
        if not new_id:
            raise ValueError("ID can not be empty!")
        self.__person_id = new_id

    @property
    def sex(self):
        return self.__sex

    @sex.setter
    def sex(self, new_value):
        if not new_value:
            raise ValueError("Gneder can not be empty")
        self.__sex = new_value

    def __str__(self):
        return "f"

    @property
    def calculate_age(self):
        birth_year = int(self.__dob.split("/")[2])
        year_now = datetime.now().year
        return year_now - birth_year

    @property
    def __str__(self):
        return f"{self.__person_id} {self.name}"

    @property
    def to_dict(self):
        return {
            "id": self.__person_id,
            "name": self.__name,
            "gneder": self.__sex,
            "dob": self.__dob,
            "email": self.__email,
        }
