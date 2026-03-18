import os
from database.data_manager import DataManager
from model.student import Student

dm = DataManager("./data")

def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def pause(text = "\nPress enter key ...."):
    input(text)

HOME_OPTION = [
    "CRUD STUDENT OPERATION",
    "VIEW CLASSROOM",
    "VIEW TEACHER",
    "GENERATE REPORT",
    "GENERATE GRAPH",
    "EXIT"
]
GENERATE_REPORT_OPTION = [
    "TRANSCRIPT REPORT",
    "CLASS REPORT",
    "ANNUAL REPORT",
    "BACK TO HOME"
]
GENERATE_GRAPH_OPTION = [
    "GRAPH TRANSCRIPT REPORT",
    "GRAPH CLASS REPORT",
    "GRAPH ANNUAL REPORT",
    "BACK TO HOME"
]
CRUD_OPTION_STUDENT = [
    "VIEW STUDENT",
    "UPDATE STUDENT",
    "ADD STUDENT",
    "DELETE STUDENT",
    "BACK TO HOME"
]

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

UPDATE_FIELDS = {
    "1": ("student_name", "Full Name"),
    "2": ("class_id",     "Class ID"),
    "3": ("sex",          "Sex (M/F)"),
    "4": ("dob",          "Date of Birth (YYYY-MM-DD)"),
    "5": ("email",        "Email"),
    "6": ("attendance",   "Attendance %"),
}

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

    confirm = input(f"\n  Are you sure you want to delete '{student.student_name}'? (y/n): ").strip().lower()

    if confirm == "y":
        success = dm.delete_student(student_id)
        if success:
            print(f"  Student '{student.student_name}' deleted successfully!")
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
        user_option = input(f"Choose option 0-{len(CRUD_OPTION_STUDENT) - 1} (0 = back): ")

        if not check_option(len(CRUD_OPTION_STUDENT), user_option):
            print("Wrong option")
            pause()
            continue

        option = int(user_option)

        if option == 0:
            break
        elif option == 1:
            view_student()
        elif option == 2:
            update_student()
        elif option == 3:
            add_student()
        elif option == 4:
            delete_student()

        pause()

# ─────────────────────────────────────────────
# Generate Report sub-menu
# ─────────────────────────────────────────────

def handle_generate_report():
    while True:
        clear_screen()
        display_option(GENERATE_REPORT_OPTION, "GENERATE REPORT")
        user_option = input(f"Choose option 0-{len(GENERATE_REPORT_OPTION) - 1} (0 = back): ")

        if not check_option(len(GENERATE_REPORT_OPTION), user_option):
            print("Wrong option")
            pause()
            continue

        option = int(user_option)

        if option == 0:
            break
        elif option == 1:
            clear_screen()
            print("[ TRANSCRIPT REPORT ] — Feature coming soon...")
        elif option == 2:
            clear_screen()
            class_id = input("  Enter Class ID: ").strip()
            report = dm.generate_report(class_id)
            if report:
                print(f"\n  Class       : {report['class_id']}")
                print(f"  Level       : {report['class_level']}")
                print(f"  Students    : {report['student_count']}")
                print(f"  Average     : {report['class_average']:.2f}")
                print(f"  Pass Rate   : {report['pass_rate']:.2f}%")
                print(f"  Failing     : {report['failing_count']}")
                print(f"\n  Subject Averages:")
                for subj, avg in report['subject_averages'].items():
                    print(f"    {subj}: {avg:.2f}")
                print(f"\n  Top 5 Students:")
                for s in report['top_students']:
                    print(f"    {s['name']} — {s['average']:.2f}")
            else:
                print(f"  No data found for class: {class_id}")
        elif option == 3:
            clear_screen()
            print("[ ANNUAL REPORT ] — Feature coming soon...")

        pause()

# ─────────────────────────────────────────────
# Generate Graph sub-menu
# ─────────────────────────────────────────────

def handle_generate_graph():
    while True:
        clear_screen()
        display_option(GENERATE_GRAPH_OPTION, "GENERATE GRAPH")
        user_option = input(f"Choose option 0-{len(GENERATE_GRAPH_OPTION) - 1} (0 = back): ")

        if not check_option(len(GENERATE_GRAPH_OPTION), user_option):
            print("Wrong option")
            pause()
            continue

        option = int(user_option)

        if option == 0:
            break
        elif option == 1:
            clear_screen()
            print("[ GRAPH TRANSCRIPT REPORT ] — Feature coming soon...")
        elif option == 2:
            clear_screen()
            class_id = input("  Enter Class ID: ").strip()
            print(f"  Generating graph for class {class_id}...")
            dm.generate_class_report_plot(class_id)
        elif option == 3:
            clear_screen()
            print("[ GRAPH ANNUAL REPORT ] -> Feature coming soon...")

        pause()

# ─────────────────────────────────────────────
# Home menu
# ─────────────────────────────────────────────

def main():
    while True:
        clear_screen()
        display_option(HOME_OPTION, "MAIN MENU")
        user_option = input(f"Choose option 0-{len(HOME_OPTION) - 1} (0 = exit): ")

        if not check_option(len(HOME_OPTION), user_option):
            print("Wrong option")
            pause()
            continue

        option = int(user_option)

        if option == 0:
            clear_screen()
            print("Goodbye!")
            break
        elif option == 1:
            handle_crud_student()
        elif option == 2:
            clear_screen()
            print("[ VIEW CLASSROOM ]")
            classrooms = dm.load_classroom()
            for c in classrooms:
                print(f"  {c.class_id} | Level: {c.class_level} | Room: {c.room} | Students: {c.len}")
            pause()
        elif option == 3:
            clear_screen()
            print("[ VIEW TEACHER ]")
            teachers = dm.load_teacher()
            for t in teachers:
                print(f"  {t.teacher_id} | {t.name} | {t.subject} | Salary: {t.salary}")
            pause()
        elif option == 4:
            handle_generate_report()
        elif option == 5:
            handle_generate_graph()

if __name__ == "__main__":
    main()