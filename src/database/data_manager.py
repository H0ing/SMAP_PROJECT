"""
DataManager Module - School Management System
NO CACHE VERSION - Simpler but reads files every time
"""

import os
import json
import csv
import shutil
from datetime import datetime
from pathlib import Path

# Constants
SUBJECTS = ["Math", "Physics", "Chemistry", "Biology", "History", "Literature", "English"]
GRADING_SCALE = {
    'A+': (90, 100), 'A': (85, 89), 'B': (80, 84), 
    'C': (70, 79), 'D': (60, 69), 'F': (0, 59)
}


class Student:
    """Student with personal info and scores."""
    
    def __init__(self, student_id, student_name, class_id, sex, dob, email, attendance, scores=None):
        self.student_id = student_id
        self.student_name = student_name
        self.class_id = class_id
        self.sex = sex
        self.dob = dob
        self.email = email
        self.attendance = attendance
        self.scores = scores if scores is not None else {}
    
    @property
    def age(self):
        """Calculate age from date of birth."""
        try:
            birth_date = datetime.strptime(self.dob, "%m/%d/%Y")
            today = datetime.now()
            years = today.year - birth_date.year
            birthday_passed = (today.month, today.day) >= (birth_date.month, birth_date.day)
            return years if birthday_passed else years - 1
        except:
            return 0
    
    def subject_average(self, subject):
        """Average for one subject."""
        if subject not in self.scores or not self.scores[subject]:
            return 0.0
        return round(sum(self.scores[subject]) / len(self.scores[subject]), 2)
    
    def overall_average(self):
        """Average across all subjects."""
        avgs = []
        for subject in SUBJECTS:
            if subject in self.scores:
                avgs.append(self.subject_average(subject))
        return round(sum(avgs) / len(avgs), 2) if avgs else 0.0
    
    def grade_letter(self):
        """Convert average to letter grade."""
        avg = self.overall_average()
        for grade, (low, high) in GRADING_SCALE.items():
            if low <= avg <= high:
                return grade
        return 'F'
    
    def is_passing(self):
        return self.overall_average() >= 60
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'student_name': self.student_name,
            'class_id': self.class_id,
            'sex': self.sex,
            'dob': self.dob,
            'email': self.email,
            'attendance': self.attendance,
            'scores': self.scores
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            student_id=data['student_id'],
            student_name=data['student_name'],
            class_id=data['class_id'],
            sex=data['sex'],
            dob=data['dob'],
            email=data['email'],
            attendance=data['attendance'],
            scores=data.get('scores', {})
        )


class Teacher:
    """Teacher with professional info."""
    
    def __init__(self, teacher_id, teacher_name, subject, gender, salary, room):
        self.teacher_id = teacher_id
        self.teacher_name = teacher_name
        self.subject = subject
        self.gender = gender
        self.salary = salary
        self.room = room
    
    def to_dict(self):
        return {
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher_name,
            'subject': self.subject,
            'gender': self.gender,
            'salary': self.salary,
            'room': self.room
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class Classroom:
    """Collection of students with analytics."""
    
    def __init__(self, class_id, class_level, homeroom_teacher=None):
        self._class_id = class_id
        self._class_level = class_level
        self._teacher = homeroom_teacher
        self._students = []
    
    @property
    def class_id(self):
        return self._class_id
    
    @property
    def class_level(self):
        return self._class_level
    
    @property
    def students(self):
        return list(self._students)
    
    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("Only Student instances allowed")
        if student in self._students:
            raise ValueError(f"Student {student.student_id} already in class")
        self._students.append(student)
    
    def remove_student(self, student_id):
        original = len(self._students)
        self._students = [s for s in self._students if s.student_id != student_id]
        return len(self._students) < original
    
    def get_student(self, student_id):
        for s in self._students:
            if s.student_id == student_id:
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
            scores = [s.subject_average(subject) for s in self._students if subject in s.scores]
            result[subject] = round(sum(scores) / len(scores), 2) if scores else 0.0
        return result
    
    # Magic methods
    def __iter__(self):
        return iter(self._students)
    
    def __len__(self):
        return len(self._students)
    
    def __getitem__(self, index):
        return self._students[index]
    
    def __contains__(self, student):
        return student in self._students


class DataManager:
    """
    Handles all file operations.
    NO CACHE - reads from disk every time.
    Simpler code, always fresh data.
    """
    
    def __init__(self, data_dir="."):
        self.data_dir = Path(data_dir)
        self.students_file = self.data_dir / "students_info.csv"
        self.scores_file = self.data_dir / "students_score.json"
        self.teachers_file = self.data_dir / "teachers.csv"
        self.rooms_file = self.data_dir / "rooms.csv"
        # NO CACHE VARIABLES HERE
    
    # ==================== STUDENTS ====================
    
    def load_students(self):
        """
        Load students from CSV + JSON.
        READS FILES EVERY TIME - no cache.
        """
        # Load scores into lookup dictionary
        scores_lookup = {}
        if self.scores_file.exists():
            with open(self.scores_file, 'r', encoding='utf-8') as f:
                scores_data = json.load(f)
                for entry in scores_data:
                    scores_lookup[entry['student_id']] = entry.get('scores', {})
        
        # Load students and attach scores
        students = []
        if self.students_file.exists():
            with open(self.students_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['attendance'] = int(row['attendance'])
                    row['scores'] = scores_lookup.get(row['student_id'], {})
                    students.append(Student.from_dict(row))
        
        return students  # Return directly, no cache storage
    
    def save_students(self, students):
        """Save to CSV and JSON."""
        # CSV: demographics only
        csv_rows = []
        for student in students:
            csv_rows.append({
                'student_id': student.student_id,
                'student_name': student.student_name,
                'class_id': student.class_id,
                'sex': student.sex,
                'dob': student.dob,
                'email': student.email,
                'attendance': student.attendance
            })
        
        with open(self.students_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['student_id', 'student_name', 'class_id', 'sex', 'dob', 'email', 'attendance'])
            writer.writeheader()
            writer.writerows(csv_rows)
        
        # JSON: scores only
        scores_data = []
        for student in students:
            scores_data.append({
                'student_id': student.student_id,
                'scores': student.scores
            })
        
        with open(self.scores_file, 'w', encoding='utf-8') as f:
            json.dump(scores_data, f, indent=2)
        
        # NO CACHE TO CLEAR
    
    def get_student(self, student_id):
        """Find one student by ID."""
        students = self.load_students()  # Always fresh load
        for student in students:
            if student.student_id == student_id:
                return student
        return None
    
    def add_student(self, student):
        """Add new student."""
        students = self.load_students()
        for existing in students:
            if existing.student_id == student.student_id:
                raise ValueError(f"Student ID {student.student_id} already exists")
        students.append(student)
        self.save_students(students)
    
    def update_student(self, student_id, updates):
        """Update student fields."""
        students = self.load_students()
        for student in students:
            if student.student_id == student_id:
                for key, value in updates.items():
                    if hasattr(student, key):
                        setattr(student, key, value)
                self.save_students(students)
                return True
        return False
    
    def delete_student(self, student_id):
        """Remove student."""
        students = self.load_students()
        original = len(students)
        students = [s for s in students if s.student_id != student_id]
        if len(students) < original:
            self.save_students(students)
            return True
        return False
    
    def find_students_by_class(self, class_id):
        """Get students in specific class."""
        students = self.load_students()
        return [s for s in students if s.class_id == class_id]
    
    def find_students_by_name(self, name):
        """Search by name (partial match)."""
        students = self.load_students()
        name_lower = name.lower()
        return [s for s in students if name_lower in s.student_name.lower()]
    
    # ==================== TEACHERS ====================
    
    def load_teachers(self):
        """Load all teachers from CSV."""
        teachers = []
        if self.teachers_file.exists():
            with open(self.teachers_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row['salary'] = float(row['salary'])
                    teachers.append(Teacher.from_dict(row))
        return teachers
    
    def save_teachers(self, teachers):
        """Save teachers to CSV."""
        with open(self.teachers_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['teacher_id', 'teacher_name', 'subject', 'gender', 'salary', 'room'])
            writer.writeheader()
            for teacher in teachers:
                writer.writerow(teacher.to_dict())
    
    def get_teacher(self, teacher_id):
        """Find teacher by ID."""
        teachers = self.load_teachers()
        for teacher in teachers:
            if teacher.teacher_id == teacher_id:
                return teacher
        return None
    
    def get_teachers_by_subject(self, subject):
        """Find teachers by subject."""
        teachers = self.load_teachers()
        return [t for t in teachers if t.subject.lower() == subject.lower()]
    
    # ==================== CLASSROOMS ====================
    
    def load_classrooms(self):
        """
        Build classrooms from rooms.csv.
        Links teachers and students each time.
        """
        teachers = self.load_teachers()
        students = self.load_students()
        
        # Build teacher lookup
        teachers_by_id = {}
        for t in teachers:
            teachers_by_id[t.teacher_id] = t
        
        classrooms = []
        if self.rooms_file.exists():
            with open(self.rooms_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    class_id = row['class_id']
                    class_level = row['class_level']
                    teacher_id = row['homeroom_teacher']
                    
                    # Get teacher object
                    teacher = teachers_by_id.get(teacher_id)
                    
                    # Create classroom
                    classroom = Classroom(class_id, class_level, teacher)
                    
                    # Add students belonging to this class
                    for student in students:
                        if student.class_id == class_level:
                            classroom.add_student(student)
                    
                    classrooms.append(classroom)
        
        return classrooms
    
    def get_classroom(self, class_id):
        """Find classroom by ID."""
        classrooms = self.load_classrooms()
        for classroom in classrooms:
            if classroom.class_id == class_id:
                return classroom
        return None
    
    # ==================== UTILITIES ====================
    
    def backup(self, backup_dir=None):
        """Create timestamped backup."""
        if backup_dir is None:
            backup_dir = self.data_dir / "backups"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Path(backup_dir) / f"backup_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)
        
        files = [self.students_file, self.scores_file, self.teachers_file, self.rooms_file]
        backed_up = []
        
        for file_path in files:
            if file_path.exists():
                dest = backup_path / file_path.name
                shutil.copy2(file_path, dest)
                backed_up.append(file_path.name)
        
        return {
            'backup_path': str(backup_path),
            'files': backed_up,
            'timestamp': timestamp
        }
    
    def generate_report(self, class_id):
        """Generate statistics report for classroom."""
        classroom = self.get_classroom(class_id)
        if not classroom:
            return None
        
        return {
            'class_id': classroom.class_id,
            'class_level': classroom.class_level,
            'student_count': len(classroom),
            'class_average': classroom.class_average(),
            'pass_rate': classroom.pass_rate(),
            'subject_averages': classroom.subject_averages(),
            'top_students': [
                {'id': s.student_id, 'name': s.student_name, 'average': s.overall_average()}
                for s in classroom.top_students(5)
            ],
            'failing_count': len(classroom.failing_students())
        }


# Example usage
if __name__ == "__main__":
    dm = DataManager("./school_data")
    
    # Each call reads from disk - no cache
    students = dm.load_students()
    print(f"Loaded {len(students)} students")
    
    # This reads files AGAIN - fresh data but slower
    same_students = dm.load_students()
    
    # Find specific student
    s = dm.get_student("S001")
    if s:
        print(f"{s.student_name}: {s.overall_average()}")