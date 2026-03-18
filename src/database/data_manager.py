import os
import csv
import json
from pathlib import Path
from model.teacher import Teacher
from model.student import Student
from model.classroom import Classroom
class DataManager:
    def __init__(self, data_path = "."):
        self.students_file = Path(data_path)  / "students.csv"
        self.scores_file = Path(data_path) / "scores.json"
        self.teachers_file = Path(data_path) / "teachers.csv"
        self.rooms_file = Path(data_path) / "rooms.csv"
    
    def load_teacher(self):
        teachers = []
        try:
            with open(self.teachers_file, "r") as f:
                reads = csv.DictReader(f)
                for row in reads:
                    row["salary"] = float(row["salary"])
                    teachers.append(Teacher.from_dict(row))
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print("Error loading teacher file:", e)
        finally:
            print("Process load teacher file executed!")
        return teachers
    def save_teacher(self, teachers):
        try:
            with open(self.teachers_file , "w", newline='') as f:
                fieldname = ["teacher_id", "name", "sex", "subject", "salary", "room"]
                writer = csv.DictWriter(f, fieldnames=fieldname)
                writer.writeheader()
                for teacher in teachers:
                    writer.writerow(teacher.to_dict())
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print("Error saving teacher file:", e)
        finally:
            print("Process save teacher file executed!")
    def get_teacher_by_id(self, teacher_id):
        teachers = self.load_teacher()
        for teacher in teachers:
            if teacher.teacher_id == teacher_id:
                return teacher
        return None
    def get_teacher_by_subject(self, subject):
        teachers = self.load_teacher()
        found_teacher = [t for t in teachers if t.subject.lower() == subject.lower()]
        return found_teacher
    
    
    #sudent file
    def load_student(self):
        scores_container = {}
        students = []
        try:
            with open(self.scores_file, "r") as f:
                score_data = json.load(f)
                for score in score_data:
                    scores_container[score["student_id"]] = score.get('scores', {})
        except FileNotFoundError:
            print("File scores data not found")
        except Exception as e:
            print("Error loading scores:" ,e)
        finally:
            print("Process load student score executed")
        
        try:
            with open(self.students_file, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # print(row)
                    row["attendance"] = float(row["attendance"])
                    row["scores"] = scores_container.get(row["student_id"], {})
                    # print(row)
                    students.append(Student.from_dict(row))
                    # print(Student.from_dict(row).scores)
        except FileNotFoundError:
            print("File student information not found")
        except Exception as e:
            print("Error loading student:" ,e)
        finally:
            print("Process load student information executed")

        # print(scores_container)
        return students
    
    def save_student(self, students):
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
        try:
            with open(self.students_file, "w", newline="") as f:
                fieldname = ['student_id', 'student_name', 'class_id', 'sex', 'dob', 'email', 'attendance']
                writer = csv.DictWriter(f, fieldnames=fieldname)
                writer.writeheader()
                writer.writerows(csv_rows)
        except FileNotFoundError:
            print("File student not found")
        except Exception as e:
            print("Error saving student:" ,e)
        finally:
            print("Process save student information executed")
        
        scores_data = []

        for student in students:
            scores_data.append({
                'student_id': student.student_id,
                'scores': student.scores
            })
        
        try:
            with open(self.scores_file, 'w') as f:
                json.dump(scores_data, f, indent=2)
        except FileNotFoundError:
            print("file json score not found")
        except Exception as e:
            print("Error saving scores:" ,e)
        finally:
            print("Process saving score executed")


    def get_student(self, student_id):
        students = self.load_student()  
        for student in students:
            if student.person_id == student_id:
                return student
        return None
    def find_students_by_class(self, class_id):
        students = self.load_student()
        return [s for s in students if s.class_id == class_id]
    def find_students_by_name(self, name):
        students = self.load_student()
        name_lower = name.lower()
        return [s for s in students if name_lower in s.student_name.lower()]
    
    def add_student(self, student):
        students = self.load_student()
        for existing in students:
            if existing.student_id == student.student_id:
                raise ValueError(f"Student ID {student.student_id} already exists")
        students.append(student)
        self.save_student(students)
    
    def update_student(self, student_id, updates):
        students = self.load_student()
        for student in students:
            if student.student_id == student_id:
                for key, value in updates.items():
                    if hasattr(student, key):
                        setattr(student, key, value)
                self.save_student(students)
                return True
        return False
    def delete_student(self, student_id):
        students = self.load_student()
        original = len(students)
        students = [s for s in students if s.student_id != student_id]
        if len(students) < original:
            self.save_student(students)
            return True
        return False
    
    def load_classroom(self):
        students = self.load_student()
        teachers = self.load_teacher()
        teachers_by_id = {}
        for t in teachers:
            teachers_by_id[t.person_id] = t
        
        classrooms = []
        try:
            with open(self.rooms_file, 'r') as f:
                reads = csv.DictReader(f)
                for row in reads:
                    class_id = row['class_id']
                    class_level = row['class_level']
                    room = row['room']
                    capacity = int(row["capacity"])
                    year = row['year']
                    teacher_id = row['homeroom_teacher']
                    teacher = teachers_by_id.get(teacher_id)
                    classroom = Classroom(class_id, class_level, room, teacher, capacity, year)
                    for student in students:
                        if student.class_id == class_id:
                            classroom.add_student(student)
                    classrooms.append(classroom)
        except FileNotFoundError:
            print("File classroom not found")
        except Exception as e:
            print("Error loading file classroom:", e)
        finally:
            print("Process loading file classroom executed") 
        
        return classrooms
    
    
    def generate_report(self, class_id):
        classroom = self.get_classroom(class_id)
        if not classroom:
            return None   
        return {
            'class_id': classroom.class_id,
            'class_level': classroom.class_level,
            'student_count': classroom.len,
            'class_average': classroom.class_average(),
            'pass_rate': classroom.pass_rate(),
            'subject_averages': classroom.subject_averages(),
            'top_students': [
                {'id': s.person_id, 'name': s.name, 'average': s.overall_average()}
                for s in classroom.top_students(5)
            ],
            'failing_count': len(classroom.failing_students())
        }
    
    def get_classroom(self, class_id):
        classrooms = self.load_classroom()
        for classroom in classrooms:
            if classroom.class_id == class_id:
                return classroom
        return None  
    

    def generate_class_report_plot(self, class_id):
        
        import matplotlib
        matplotlib.use('Agg') 
        import matplotlib.pyplot as plt
        import os

        # Get data 
        report = self.generate_report(class_id)
        students = self.find_students_by_class(class_id)

        if not report or not students:
            print("No data found for this class.")
            return

        subjects = list(report["subject_averages"].keys())
        averages = list(report["subject_averages"].values())

        student_names = [s.name for s in students]
        student_avgs  = [s.overall_average() for s in students]

        # Grade calculation 
        def get_grade(avg):
            if avg >= 90: return "A"
            elif avg >= 80: return "B"
            elif avg >= 70: return "C"
            elif avg >= 60: return "D"
            elif avg >= 50: return "E"
            else: return "F"

        grade_labels = ["A", "B", "C", "D", "E", "F"]
        grade_counts = {g: 0 for g in grade_labels}

        for avg in student_avgs:
            grade_counts[get_grade(avg)] += 1

        # Sort ranking 
        paired = sorted(zip(student_avgs, student_names), reverse=True)
        sorted_avgs  = [a for a, _ in paired]
        sorted_names = [n for _, n in paired]

        #  Create plots 
        fig, axs = plt.subplots(3, 1, figsize=(10, 15))

        # 1. Subject Averages
        axs[0].barh(subjects, averages)
        axs[0].set_title(f"Subject Averages — {class_id}")

        # 2. Grade Distribution
        counts = [grade_counts[g] for g in grade_labels]
        axs[1].bar(grade_labels, counts)
        axs[1].set_title(f"Grade Distribution — {class_id}")

        # 3. Student Ranking
        axs[2].barh(range(len(sorted_names)), sorted_avgs)
        axs[2].set_yticks(range(len(sorted_names)))
        axs[2].set_yticklabels([f"#{i+1} {n}" for i, n in enumerate(sorted_names)])
        axs[2].invert_yaxis()
        axs[2].set_title(f"Student Ranking — {class_id}")

        plt.tight_layout()

        # Save SMAP_DEVELOP/outputs/graphs/class/file_name.png
        # Build correct path
        save_dir = os.path.join("outputs", "graphs", "class")
        os.makedirs(save_dir, exist_ok=True)  # create folder if not exists

        file_name = f"class_report_{class_id}.png"
        save_path = os.path.join(save_dir, file_name)

        plt.savefig(save_path, dpi=300)

        print(f"Saved to: {save_path}")
        
    def generate_annaul_report():
        pass
    
    
if __name__ == "__main__":
    dm = DataManager("./data")

    print("\n--- LOAD STUDENTS ---")
    students = dm.load_student()
    for s in students:
        print(s.person_id, s.name, s.class_id , s.scores)

    print("\n--- LOAD TEACHERS ---")
    teachers = dm.load_teacher()
    for t in teachers:
        print(t.person_id, t.name, t.subject)

    print("\n--- LOAD CLASSROOMS ---")
    classrooms = dm.load_classroom()
    for c in classrooms:
        print(f"Class: {c.class_id}, Students: {c.len}")

    print("\n--- GENERATE REPORT ---")
    report = dm.generate_report("C1A")
    print(report)

    print("\n--- FIND STUDENT ---")
    student = dm.get_student("S001")
    if student:
        print(student.name)   

    find_class_id = classrooms[0].class_id
    find_student_in_class = classrooms[0].students
    print(find_class_id)
    for i in find_student_in_class:
        print(i.scores)

    dm.generate_class_report_plot("C1A")


    

          
                    
                
                
        
                
        