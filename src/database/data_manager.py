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
        
    def generate_annaul_report(self):
        import matplotlib
        matplotlib.use('Agg') 
        import matplotlib.pyplot as plt
        import os
       
        classrooms=self.load_classroom()
        if not classrooms:
            print("No classrooms found.")
            return
        all_students=[s for c in classrooms for s in c.students]
        if not all_students:
            print("No student found.")
            return
        subjects = list(all_students[0].scores.keys()) if all_students else []
        active_classes = [c for c in classrooms if c.students]
            # Chart 1: group classes by year, find highest avg class per year
        from collections import defaultdict
        classes_by_year = defaultdict(list)
        for c in active_classes:
            classes_by_year[c._year].append(c)

        year_labels    = []   # x axis — each year
        top_class_avgs = []   # y axis — highest class avg that year
        top_class_ids  = []   # label — which class was the best
        for year,classes in sorted(classes_by_year.items()):
            best=max(classes,key=lambda c: c.class_average())
            year_labels.append(year)
            top_class_avgs.append(best.class_average())
            top_class_ids.append(best.class_id)
        # chart 2 top performer per class
        top_scores = []
        top_labels = []
        for c in active_classes:
            top = max(c.students,key=lambda s:s.overall_average())
            top_scores.append(top.overall_average())
            top_labels.append(f"{c.class_id}-{top.name}")
        #chart 3 grade distribution school-wide
        grade_labels = ["A", "B", "C", "D", "E", "F"]
        grade_counts = {g: 0 for g in grade_labels}
        for s in all_students:
            grade_counts[s.grade_letter()] += 1
        
        #implement and figure all plots
        fig, axs = plt.subplots(3,1, figsize=(12,18))
        fig.suptitle("Annual School Report — 2024/2025", fontsize=15, fontweight="bold")
        #chart 1 highest class per year
        axs[0].bar(year_labels, top_class_avgs,
               color=[self._score_color(v) for v in top_class_avgs])
        axs[0].set_ylim(0, 100)
        axs[0].set_title("Highest Performing Class per Year")
        axs[0].set_ylabel("Average Score")
        axs[0].axhline(y=50, color="red", linestyle="--", label="Pass Mark")
        axs[0].legend()
        # Label each bar with class ID and score
        for i, (v, cid) in enumerate(zip(top_class_avgs, top_class_ids)):
            axs[0].text(i, v + 1, f"{cid}\n{v:.1f}", ha="center", fontsize=9, fontweight="bold")
        # ── Chart 2: Top performer per class (horizontal bar) ─────────────────
        axs[1].barh(range(len(top_labels)), top_scores,
                    color=[self._score_color(v) for v in top_scores])
        axs[1].set_yticks(range(len(top_labels)))
        axs[1].set_yticklabels(top_labels, fontsize=9)
        axs[1].invert_yaxis()
        axs[1].axvline(x=50, color="red",   linestyle="--", label="Pass Mark")
        axs[1].axvline(x=70, color="green", linestyle=":",  label="Good (70)")
        axs[1].set_xlim(0, 100)
        axs[1].set_title("Top Performer per Class")
        axs[1].set_xlabel("Overall Average Score")
        axs[1].legend()
        for i, v in enumerate(top_scores):
            axs[1].text(v + 1, i, f"{v:.1f}", va="center", fontsize=8, fontweight="bold")

        # ── Chart 3: Grade distribution (vertical bar) ────────────────────────
        counts     = [grade_counts[g] for g in grade_labels]
        grd_colors = ["#2ecc71", "#27ae60", "#f1c40f", "#e67e22", "#e74c3c", "#c0392b"]
        axs[2].bar(grade_labels, counts, color=grd_colors)
        axs[2].set_title("School-wide Grade Distribution")
        axs[2].set_ylabel("Number of Students")
        for i, c in enumerate(counts):
            if c > 0:
                axs[2].text(i, c + 0.1, str(c), ha="center", fontsize=9, fontweight="bold")
        # check student make sure graph is corrected by meng seang
        # total = 0
        # for c in classrooms:
        #     print(f"\n--- {c.class_id} ({len(c.students)} students) ---")
        #     print(f"  {'ID':<10} {'Name':<22} {'Avg':>6} {'Grade'}")
        #     print(f"  {'-'*45}")
        #     for s in c.students:
        #         avg = s.overall_average()
        #         grade = s.grade_letter()
        #         print(f"  {s.person_id:<10} {s.name:<22} {avg:>6.1f} {grade}")
        #     total += len(c.students)       
        # print(f"\n{'='*45}")
        # print(f"Total: {total} students across {len(classrooms)} classes")
        plt.tight_layout()
        return self._save_plot(plt, "annual", "annual_report.png") 
    def _score_color(self, value):
        if value >= 70:
            return "green"
        elif value >= 50:
            return "orange"
        return "red"      
    def _save_plot(self, plt, folder, filename):
        import os
        save_dir = os.path.join("outputs", "graphs", folder)
        os.makedirs(save_dir, exist_ok=True)
        path = os.path.join(save_dir, filename)
        plt.savefig(path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Saved to: {path}")
        return path     
        
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
    dm.generate_annaul_report()


    

          
                    
                
                
        
                
        