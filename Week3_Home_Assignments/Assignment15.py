class EMployee:
    def __init__(self, name, employee_id, department):
        self.name = name
        self.employee_id = employee_id
        self.department = department

    def display_info(self):
        print(f"Name: {self.name}, Employee ID: {self.employee_id}, Department: {self.department}")

class manager(EMployee):
    def __init__(self, name, employee_id, department, team_size):
        super().__init__(name, employee_id, department)
        self.team_size = team_size

    def display_info(self):
        super().display_info()
        print(f"Team Size: {self.team_size}")   

class developer(EMployee):
    def __init__(self, name, employee_id, department, programming_language):
        super().__init__(name, employee_id, department)
        self.programming_language = programming_language

    def display_info(self):
        super().display_info()
        print(f"Programming Language: {self.programming_language}") 

if __name__ == "__main__":
    m1 = manager("Name1", "EMP01", "Engg", 10)
    d1 = developer("Name2", "EMP02", "Engg", "Java")

    m1.display_info()
    d1.display_info()