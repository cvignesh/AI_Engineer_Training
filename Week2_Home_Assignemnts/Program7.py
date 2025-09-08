class student:
    def __init__(self, name, grade, department):
        self.name = name
        self.grade = grade
        self.department = department

    def print_info(self):
        print(f"Student Name: {self.name}, Grade is {self.grade}, departme is {self.department}")
    
    def upgrade_grade(self, new_grade):
        self.grade = new_grade
    
if(__name__ == "__main__"):
    student1 = student("Ram", "A", "Managemnet")
    student2 = student("Raj", "B", "Maths")
    student3 = student("Raghu", "A", "Biology")

    student1.print_info()
    student2.print_info()
    student3.print_info()

    student1.upgrade_grade("B")
    print("After upgrading Grade for Studnet 1")
    student1.print_info()

