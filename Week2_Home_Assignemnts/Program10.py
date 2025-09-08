# bugs = {"BUG1" : {"severity":"High","priority":"medium","descr":"Not able to login"}}
# for key, value in bugs.items():
#     print(value)
#     print("Printing inner map")
#     for key1, value1 in value.items():
#         print(f"{key1} : {value1}")

class BugTracker:
    bugs = {}

    def add_bug(self, bug_id, description, severity):
        BugTracker.bugs[bug_id] = {'Description':description, 'Severity':severity,'status': 'Open'}
    
    def update_status(self, bug_id, new_status):
        if bug_id in BugTracker.bugs:
            BugTracker.bugs[bug_id]['status'] = new_status
        else:
            print(f"{bug_id} is not avaible")

    def list_all_bugs(self):
        for key,value in BugTracker.bugs.items():
            print("Bug Id : ",key)
            print("----------------------")
            for attr,attr_val in value.items():
                print(f"attr : {attr_val}")
            print("----------------------")

if(__name__ == "__main__"):
    Bug_obj = BugTracker()
    Bug_obj.add_bug("BUG-1","Login not working", "High")
    Bug_obj.add_bug("BUG-2","Tooltip missing", "Medium")
    Bug_obj.list_all_bugs()
    print("Updating the status of BUG-1")
    Bug_obj.update_status("BUG-1","In-Progress")
    Bug_obj.list_all_bugs()