import student as Student
class Classroom():
 def __init__(self,class_id,class_level,room,homeroom_teacher,capacity,year):
  self._class_id = class_id
  self._room = room
  self._class_level = class_level
  self._homeroom_teacher = homeroom_teacher
  self._students=[]  #list of student 
  self._capacity = capacity
  self._year = year 
 @property
 def getClassId(self):
  return self._class_id
 def setClassId(self,new_class_id):
  if(new_class_id):
   self._class_id=new_class_id
  raise ValueError ("Class ID should not empty")
 @property
 def students(self):
  return list(self.students)
 # add student 
 def addStudent(self, student):
        if not isinstance(student, Student):
            raise TypeError("Only Student instances allowed")
        if student in self._students:
            raise ValueError(f"Student {student.student_id} already in class")
        self._students.append(student) #otherwise append
 def removeStudent(self,student_id):
  sizestudents=len(self._students)
  self._students=[s for s in self._students if s.student_id!=student_id]
  return len(self._students)<sizestudents # true if remove student from the class succeed
 def getStudent(self,student_id):
  for s in self._students:
   if s.student_id==student_id:
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
 def iter(self):
     return iter(self._students)
 
 def len(self):
     return len(self._students)
 
 def getitem(self, index):
     return self._students[index]
 
 def contains(self, student):
     return student in self._students
 
        
  
 
