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
            if teacher.person_id == teacher_id:
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
                'student_id': student.person_id,
                'student_name': student.name,
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
                'student_id': student.person_id,
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
        return [s for s in students if name_lower in s.name.lower()]
    
    def add_student(self, student):
        students = self.load_student()
        for existing in students:
            if existing.person_id == student.person_id:
                raise ValueError(f"Student ID {student.person_id} already exists")
        students.append(student)
        # student.
        self.save_student(students)
    
    def update_student(self, student_id, updates):
        students = self.load_student()
        for student in students:
            if student.person_id == student_id:
                for key, value in updates.items():
                    if hasattr(student, key):
                        setattr(student, key, value)
                self.save_student(students)
                return True
        return False
    def delete_student(self, student_id):
        students = self.load_student()
        original = len(students)
        students = [s for s in students if s.person_id != student_id]
        if len(students) < original:
            self.save_student(students)
            return True
        return False
    
    def load_classroom(self, year=None):
        students = self.load_student()
        teachers = self.load_teacher()
        teachers_by_id = {t.person_id: t for t in teachers}
 
        classrooms = []
        try:
            with open(self.rooms_file, "r") as f:
                reads = csv.DictReader(f)
                for row in reads:
                    class_id    = row["class_id"]
                    class_level = row["class_level"]
                    room        = row["room"]
                    capacity    = int(row["capacity"])
                    row_year    = row["year"]
                    teacher     = teachers_by_id.get(row["homeroom_teacher"])
 
                    # skip classrooms not in the requested year
                    if year and row_year != year:
                        continue
 
                    classroom = Classroom(class_id, class_level, room, teacher, capacity, row_year)
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
    
    
    
    
    def get_classroom(self, class_id):
        classrooms = self.load_classroom()
        for classroom in classrooms:
            if classroom.class_id == class_id:
                return classroom
        return None  
    


    def get_available_years(self):
        """Return sorted list of all unique academic years from rooms.csv."""
        years = set()
        try:
            with open(self.rooms_file, "r") as f:
                for row in csv.DictReader(f):
                    if row.get("year"):
                        years.add(row["year"].strip())
        except Exception as e:
            print("Error reading years:", e)
        return sorted(years)
 
    def load_classroom_by_year(self, year):
        """Return only classrooms that belong to the given academic year."""
        return [c for c in self.load_classroom() if c._year == year]
    

    def generate_class_report_plot(self, class_id):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
 
        classroom = self.get_classroom(class_id)
        if not classroom:
            print("No data found for this class.")
            return
 
        students     = classroom.students
        subj_avgs    = classroom.subject_averages()
        subjects     = list(subj_avgs.keys())
        averages     = list(subj_avgs.values())
        student_avgs = [s.overall_average() for s in students]
 
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
 
        paired       = sorted(zip(student_avgs, [s.name for s in students]), reverse=True)
        sorted_avgs  = [a for a, _ in paired]
        sorted_names = [n for _, n in paired]
 
        fig, axs = plt.subplots(3, 1, figsize=(10, 15))
 
        axs[0].barh(subjects, averages)
        axs[0].set_title(f"Subject Averages — {class_id}")
 
        axs[1].bar(grade_labels, [grade_counts[g] for g in grade_labels])
        axs[1].set_title(f"Grade Distribution — {class_id}")
 
        axs[2].barh(range(len(sorted_names)), sorted_avgs)
        axs[2].set_yticks(range(len(sorted_names)))
        axs[2].set_yticklabels([f"#{i+1} {n}" for i, n in enumerate(sorted_names)])
        axs[2].invert_yaxis()
        axs[2].set_title(f"Student Ranking — {class_id}")
 
        plt.tight_layout()
 
        save_dir  = os.path.join("outputs", "graphs", "class")
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, f"class_report_{class_id}.png")
        plt.savefig(save_path, dpi=300)
        print(f"Saved to: {save_path}")
 
    def generate_annaul_report_plot(self, year=None):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from collections import defaultdict
 
        classrooms = self.load_classroom_by_year(year) if year else self.load_classroom()
        if not classrooms:
            print("No classrooms found.")
            return
 
        all_students = [s for c in classrooms for s in c.students]
        if not all_students:
            print("No student found.")
            return
 
        active_classes = [c for c in classrooms if c.students]
 
        # Chart 1: best class per grade level (e.g. 7A, 8B, 9A...)
        classes_by_level = defaultdict(list)
        for c in active_classes:
            classes_by_level[c.class_level].append(c)
 
        level_labels   = []
        top_class_avgs = []
        top_class_ids  = []
        for level, classes in sorted(classes_by_level.items()):
            best = max(classes, key=lambda c: c.class_average())
            level_labels.append(level)
            top_class_avgs.append(best.class_average())
            top_class_ids.append(best.class_id)
 
        # Chart 2: top student per class (within the selected year)
        top_scores = []
        top_labels = []
        for c in sorted(active_classes, key=lambda c: c.class_level):
            top = max(c.students, key=lambda s: s.overall_average())
            top_scores.append(top.overall_average())
            top_labels.append(f"{c.class_id} {c.class_level} - {top.name}")
 
        # Chart 3: grade distribution school-wide
        grade_labels = ["A", "B", "C", "D", "E", "F"]
        grade_counts = {g: 0 for g in grade_labels}
        for s in all_students:
            grade_counts[s.grade_letter()] += 1
 
        title_label  = year if year else "All Years"
        chart2_height = max(6, len(active_classes) * 0.4)
 
        fig, axs = plt.subplots(3, 1, figsize=(12, 12 + chart2_height))
        fig.suptitle(f"Annual School Report — {title_label}", fontsize=15, fontweight="bold")
 
        # Chart 1: best class per grade level
        axs[0].bar(level_labels, top_class_avgs,
                   color=[self._score_color(v) for v in top_class_avgs])
        axs[0].set_ylim(0, 100)
        axs[0].set_title("Best Class per Grade Level")
        axs[0].set_ylabel("Average Score")
        axs[0].axhline(y=50, color="red", linestyle="--", label="Pass Mark")
        axs[0].legend()
        for i, (v, cid) in enumerate(zip(top_class_avgs, top_class_ids)):
            axs[0].text(i, v + 1, f"{v:.1f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
            axs[0].text(i, v / 2, cid, ha="center", va="center", fontsize=8, fontweight="bold", color="white", rotation=90)
 
        # Chart 2: top student per class
        axs[1].barh(range(len(top_labels)), top_scores,
                    color=[self._score_color(v) for v in top_scores])
        axs[1].set_yticks(range(len(top_labels)))
        axs[1].set_yticklabels(top_labels, fontsize=9)
        axs[1].invert_yaxis()
        axs[1].axvline(x=50, color="red",   linestyle="--", label="Pass Mark")
        axs[1].axvline(x=70, color="green", linestyle=":",  label="Good (70)")
        axs[1].set_xlim(0, 100)
        axs[1].set_title("Top Student per Class")
        axs[1].set_xlabel("Overall Average Score")
        axs[1].legend()
        for i, v in enumerate(top_scores):
            axs[1].text(v + 1, i, f"{v:.1f}", va="center", fontsize=8, fontweight="bold")
 
        # Chart 3: grade distribution
        counts     = [grade_counts[g] for g in grade_labels]
        grd_colors = ["#2ecc71", "#27ae60", "#f1c40f", "#e67e22", "#e74c3c", "#c0392b"]
        axs[2].bar(grade_labels, counts, color=grd_colors)
        axs[2].set_title("School-wide Grade Distribution")
        axs[2].set_ylabel("Number of Students")
        for i, c in enumerate(counts):
            if c > 0:
                axs[2].text(i, c + 0.1, str(c), ha="center", fontsize=9, fontweight="bold")
 
        plt.tight_layout()
 
        filename = f"annual_report_{year.replace('-', '_')}.png" if year else "annual_report_all.png"
        return self._save_plot(plt, "annual", filename)
 
    def _score_color(self, value):
        if value >= 70:
            return "green"
        elif value >= 50:
            return "orange"
        return "red"
 
    def _save_plot(self, plt, folder, filename):
        save_dir = os.path.join("outputs", "graphs", folder)
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, filename)
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Saved to: {path}")
        return path
    def generate_transcript_plot(self, student_id):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        import os
        
        student = self.get_student(student_id)
        if student == None:
            print(f"Not found student {student_id}")
            return
        subjects = list(student.scores.keys())
        start_month = 1
        end_month = len(student.scores[subjects[0]]) 
        months = list(range(start_month, end_month + 1))
        data = {}
        for subject in subjects:
            data[subject] = student.scores[subject]
        
        fig, axs = plt.subplots(1, 2, figsize=(16, 6))
        
        #plot line chart
        for subject, scores in data.items():
            axs[0].plot(months, scores, marker = 'o', label=subject)
        axs[0].set_title(f"Monthly Trend — {student.name}")
        axs[0].set_xlabel("Month")
        axs[0].set_ylabel("Score")
        axs[0].set_xticks(months)
        axs[0].set_ylim(0, 100)
        axs[0].grid(True)
        axs[0].legend()
        
        #plot bar chart
        month_avg = []
        for i in range(len(months)):
            month_scores = [data[s][i] for s in subjects]
            avg = np.mean(month_scores)
            month_avg.append(avg)
        # Plot bar chart
        axs[1].bar(months, month_avg)
        axs[1].set_title(f"Monthly Average — {student.name}")
        axs[1].set_xlabel("Month")
        axs[1].set_ylabel("Average Score")
        axs[1].set_ylim(0, 100)
        axs[1].set_xticks(months)
        #save
        save_dir = os.path.join("outputs", "graphs", "transcript")
        os.makedirs(save_dir, exist_ok=True)
        file_name = f"transcript_{student_id}.png"
        save_path = os.path.join(save_dir, file_name)
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"Saved to: {save_path}")
        
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


    print("\n--- FIND STUDENT ---")
    student = dm.get_student("STU001")
    if student:
        print(student.name)   

    find_class_id = classrooms[0].class_id
    find_student_in_class = classrooms[0].students
    print(find_class_id)
    for i in find_student_in_class:
        print(i.scores)

    dm.generate_class_report_plot("CLS0482")
    dm.generate_annaul_report_plot("2020-2021")


    

          
                    
                
                
        
                
        