import os
from database.data_manager import DataManager
from model.student import Student
from report.class_report import ClassReport
from report.transcript_report import TranscriptReport
from report.annual import Annual

dm = DataManager("./data")

def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def pause(text="\nPress enter key ...."):
    input(text)

# ─────────────────────────────────────────────
# Menu constants — [0] is always the LAST item
# displayed as option 0 (back/exit)
# ─────────────────────────────────────────────

HOME_OPTION = [
    "CRUD STUDENT OPERATION",   # 1
    "VIEW CLASSROOM",           # 2
    "VIEW TEACHER",             # 3
    "GENERATE REPORT",          # 4
    "GENERATE GRAPH",           # 5
    "EXIT"                      # 0
]

GENERATE_REPORT_OPTION = [
    "TRANSCRIPT REPORT",        # 1
    "CLASS REPORT",             # 2
    "ANNUAL REPORT",            # 3
    "BACK TO HOME"              # 0
]

GENERATE_GRAPH_OPTION = [
    "GRAPH TRANSCRIPT REPORT",  # 1
    "GRAPH CLASS REPORT",       # 2
    "GRAPH ANNUAL REPORT",      # 3
    "BACK TO HOME"              # 0
]

CRUD_OPTION_STUDENT = [
    "VIEW STUDENT",             # 1
    "UPDATE STUDENT",           # 2
    "ADD STUDENT",              # 3
    "DELETE STUDENT",           # 4
    "BACK TO HOME"              # 0
]

UPDATE_FIELDS = {
    "1": ("name",       "Full Name"),
    "2": ("class_id",   "Class ID"),
    "3": ("sex",        "Sex (M/F)"),
    "4": ("dob",        "Date of Birth (YYYY-MM-DD)"),
    "5": ("email",      "Email"),
    "6": ("attendance", "Attendance %"),
}

# ─────────────────────────────────────────────
# Display & validation helpers
# ─────────────────────────────────────────────

def display_option(option_menu, title="MENU"):
    print(f"\n{'='*40}")
    print(f"  {title}")
    print(f"{'='*40}")
    for index, text in enumerate(option_menu):
        display_index = (index + 1) % len(option_menu)
        print(f"  [{display_index}] {text}")
    print(f"{'─'*40}")

def check_option(option_bound, user_option):
    list_option = [str(i) for i in range(option_bound)]
    return user_option.strip() in list_option

def print_student(student):
    print(f"{'─'*40}")
    print(f"  ID       : {student.person_id}")
    print(f"  Name     : {student.name}")
    print(f"  Class    : {student.class_id}")
    print(f"  Sex      : {student.sex}")
    print(f"  DOB      : {student.dob}")
    print(f"  Email    : {student.email}")
    print(f"  Attend.  : {student.attendance}")
    print(f"{'─'*40}")

# ─────────────────────────────────────────────
# VIEW STUDENT
# ─────────────────────────────────────────────

def view_student():
    clear_screen()
    print("=" * 40)
    print("  VIEW STUDENT")
    print("=" * 40)
    print("  [1] View all students")
    print("  [2] Search by ID")
    print("  [3] Search by name")
    print("  [4] Search by class")
    print("─" * 40)
    choice = input("  Choose option: ").strip()

    if choice == "1":
        students = dm.load_student()
        if not students:
            print("  No students found.")
        else:
            print(f"\n  Total: {len(students)} student(s)")
            for s in students:
                print_student(s)

    elif choice == "2":
        sid = input("  Enter Student ID: ").strip()
        student = dm.get_student(sid)
        if student:
            print_student(student)
        else:
            print(f"  No student found with ID: {sid}")

    elif choice == "3":
        name = input("  Enter name to search: ").strip()
        results = dm.find_students_by_name(name)
        if results:
            print(f"\n  Found {len(results)} student(s):")
            for s in results:
                print_student(s)
        else:
            print(f"  No student found with name containing: '{name}'")

    elif choice == "4":
        class_id = input("  Enter Class ID: ").strip()
        results = dm.find_students_by_class(class_id)
        if results:
            print(f"\n  Found {len(results)} student(s) in class {class_id}:")
            for s in results:
                print_student(s)
        else:
            print(f"  No students found in class: {class_id}")

    else:
        print("  Invalid option.")

# ─────────────────────────────────────────────
# ADD STUDENT
# ─────────────────────────────────────────────

def add_student():
    clear_screen()
    print("=" * 40)
    print("  ADD STUDENT")
    print("=" * 40)

    student_id   = input("  Student ID            : ").strip()
    student_name = input("  Full Name             : ").strip()
    class_id     = input("  Class ID              : ").strip()
    sex          = input("  Sex (M/F)             : ").strip()
    dob          = input("  Date of Birth (YYYY-MM-DD): ").strip()
    email        = input("  Email                 : ").strip()

    while True:
        attendance_input = input("  Attendance %          : ").strip()
        try:
            attendance = float(attendance_input)
            break
        except ValueError:
            print("  Invalid input. Attendance must be a number.")

    new_student = Student.from_dict({
        "student_id"   : student_id,
        "student_name" : student_name,
        "class_id"     : class_id,
        "sex"          : sex,
        "dob"          : dob,
        "email"        : email,
        "attendance"   : attendance,
        "scores"       : {}
    })

    try:
        dm.add_student(new_student)
        print(f"\n  Student '{student_name}' added successfully!")
    except ValueError as e:
        print(f"\n  Error: {e}")

# ─────────────────────────────────────────────
# UPDATE STUDENT
# ─────────────────────────────────────────────

def update_student():
    clear_screen()
    print("=" * 40)
    print("  UPDATE STUDENT")
    print("=" * 40)

    student_id = input("  Enter Student ID to update: ").strip()
    student = dm.get_student(student_id)

    if not student:
        print(f"  No student found with ID: {student_id}")
        return

    print("\n  Current info:")
    print_student(student)

    print("\n  Which field to update?")
    for key, (field, label) in UPDATE_FIELDS.items():
        print(f"  [{key}] {label}")
    print("  [0] Cancel")
    print("─" * 40)

    choice = input("  Choose option: ").strip()

    if choice == "0":
        print("  Update cancelled.")
        return

    if choice not in UPDATE_FIELDS:
        print("  Invalid option.")
        return

    field, label = UPDATE_FIELDS[choice]
    new_value = input(f"  New {label}: ").strip()

    if field == "attendance":
        try:
            new_value = float(new_value)
        except ValueError:
            print("  Invalid input. Attendance must be a number.")
            return

    success = dm.update_student(student_id, {field: new_value})

    if success:
        print(f"\n  Student {student_id} updated successfully!")
        updated = dm.get_student(student_id)
        if updated:
            print_student(updated)
    else:
        print(f"  Failed to update student {student_id}.")

# ─────────────────────────────────────────────
# DELETE STUDENT
# ─────────────────────────────────────────────

def delete_student():
    clear_screen()
    print("=" * 40)
    print("  DELETE STUDENT")
    print("=" * 40)

    student_id = input("  Enter Student ID to delete: ").strip()
    student = dm.get_student(student_id)

    if not student:
        print(f"  No student found with ID: {student_id}")
        return

    print("\n  Student to delete:")
    print_student(student)

    confirm = input(f"\n  Are you sure you want to delete '{student.name}'? (y/n): ").strip().lower()

    if confirm == "y":
        success = dm.delete_student(student_id)
        if success:
            print(f"  Student '{student.name}' deleted successfully!")
        else:
            print("  Delete failed.")
    else:
        print("  Delete cancelled.")

# ─────────────────────────────────────────────
# CRUD Student sub-menu
# ─────────────────────────────────────────────

def handle_crud_student():
    while True:
        clear_screen()
        display_option(CRUD_OPTION_STUDENT, "CRUD STUDENT OPERATION")
        user_option = input(f"Choose option 0-{len(CRUD_OPTION_STUDENT) - 1}: ")

        if not check_option(len(CRUD_OPTION_STUDENT), user_option):
            print("Wrong option")
            pause()
            continue

        option = int(user_option)

        if option == 0:                  # BACK TO HOME
            break
        elif option == 1:                # VIEW STUDENT
            view_student()
        elif option == 2:                # UPDATE STUDENT
            update_student()
        elif option == 3:                # ADD STUDENT
            add_student()
        elif option == 4:                # DELETE STUDENT
            delete_student()

        pause()

# ─────────────────────────────────────────────
# Generate Report sub-menu
# ─────────────────────────────────────────────

def handle_generate_report():
    while True:
        clear_screen()
        display_option(GENERATE_REPORT_OPTION, "GENERATE REPORT")
        user_option = input(f"Choose option 0-{len(GENERATE_REPORT_OPTION) - 1}: ")

        if not check_option(len(GENERATE_REPORT_OPTION), user_option):
            print("Wrong option")
            pause()
            continue

        option = int(user_option)

        if option == 0:                  # BACK TO HOME
            break

        elif option == 1:                # TRANSCRIPT REPORT
            clear_screen()
            student_id = input("  Enter Student ID: ").strip()
            student = dm.get_student(student_id)
            if not student:
                print(f"  No student found with ID: {student_id}")
            else:
                report = TranscriptReport(student)
                report.generate_report()
                print(report.content_report())
                if input("\n  Save to file? (y/n): ").strip().lower() == "y":
                    report.save_to_file()

        elif option == 2:                # CLASS REPORT
            clear_screen()
            class_id = input("  Enter Class ID: ").strip()
            classroom = dm.get_classroom(class_id)
            if not classroom:
                print(f"  No classroom found with ID: {class_id}")
            else:
                report = ClassReport(classroom)
                report.generate_report()
                print(report.content_report())
                if input("\n  Save to file? (y/n): ").strip().lower() == "y":
                    report.save_to_file()

        elif option == 3:                # ANNUAL REPORT
            clear_screen()
            classrooms = dm.load_classroom()
            if not classrooms:
                print("  No classroom data found.")
            else:
                report = Annual(classrooms)
                report.generate_report()
                print(report.content_report())
                if input("\n  Save to file? (y/n): ").strip().lower() == "y":
                    report.save_to_file()

        pause()

# ─────────────────────────────────────────────
# Generate Graph sub-menu
# ─────────────────────────────────────────────

def handle_generate_graph():
    while True:
        clear_screen()
        display_option(GENERATE_GRAPH_OPTION, "GENERATE GRAPH")
        user_option = input(f"Choose option 0-{len(GENERATE_GRAPH_OPTION) - 1}: ")

        if not check_option(len(GENERATE_GRAPH_OPTION), user_option):
            print("Wrong option")
            pause()
            continue

        option = int(user_option)

        if option == 0:                  # BACK TO HOME
            break

        elif option == 1:                # GRAPH TRANSCRIPT REPORT
            clear_screen()
            print("[ GRAPH TRANSCRIPT REPORT ] — Feature coming soon...")

        elif option == 2:                # GRAPH CLASS REPORT
            clear_screen()
            class_id = input("  Enter Class ID: ").strip()
            print(f"  Generating graph for class {class_id}...")
            dm.generate_class_report_plot(class_id)

        elif option == 3:                # GRAPH ANNUAL REPORT
            clear_screen()
            print("[ GRAPH ANNUAL REPORT ] — Feature coming soon...")

        pause()

# ─────────────────────────────────────────────
# Home menu
# ─────────────────────────────────────────────

def main():
    while True:
        clear_screen()
        display_option(HOME_OPTION, "MAIN MENU")
        user_option = input(f"Choose option 0-{len(HOME_OPTION) - 1}: ")

        if not check_option(len(HOME_OPTION), user_option):
            print("Wrong option")
            pause()
            continue

        option = int(user_option)

        if option == 0:                  # EXIT
            clear_screen()
            print("Goodbye!")
            break

        elif option == 1:                # CRUD STUDENT OPERATION
            handle_crud_student()

        elif option == 2:                # VIEW CLASSROOM
            clear_screen()
            print("[ VIEW CLASSROOM ]")
            classrooms = dm.load_classroom()
            for c in classrooms:
                print(f"  {c.class_id} | Level: {c.class_level} | Room: {c.room} | Students: {c.len}")
            pause()

        elif option == 3:                # VIEW TEACHER
            clear_screen()
            print("[ VIEW TEACHER ]")
            teachers = dm.load_teacher()
            for t in teachers:
                print(f"  {t.teacher_id} | {t.name} | {t.subject} | Salary: {t.salary}")
            pause()

        elif option == 4:                # GENERATE REPORT
            handle_generate_report()

        elif option == 5:                # GENERATE GRAPH
            handle_generate_graph()

if __name__ == "__main__":
    main()