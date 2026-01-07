import csv

class TestCase:    
    def __init__(self, test_id, test_name, module, status="Not Executed"):
        self.test_id = test_id
        self.test_name = test_name
        self.module = module
        self.status = status
    
    def execute_test(self, result):
        if result.lower() in ["pass", "fail"]:
            self.status = result.capitalize()
        else:
            print(f"Invalid result '{result}'. Status remains unchanged.")
    
    def display_test_case(self):
        print("-" * 50)
        print(f"Test ID     : {self.test_id}")
        print(f"Test Name   : {self.test_name}")
        print(f"Module      : {self.module}")
        print(f"Status      : {self.status}")
        print("-" * 50)
    
    def to_csv_row(self):
        return [self.test_id, self.test_name, self.module, self.status, "NA"]

class AutomatedTestCase(TestCase):
    
    def __init__(self, test_id, test_name, module, automation_tool, status="Not Executed"):
        super().__init__(test_id, test_name, module, status)
        self.automation_tool = automation_tool
    
    def display_test_case(self):
        print("-" * 50)
        print(f"Test ID         : {self.test_id}")
        print(f"Test Name       : {self.test_name}")
        print(f"Module          : {self.module}")
        print(f"Status          : {self.status}")
        print(f"Automation Tool : {self.automation_tool}")
        print("-" * 50)
    
    def to_csv_row(self):
        return [self.test_id, self.test_name, self.module, self.status, self.automation_tool]

class TestSuite:
    def __init__(self, suite_name):
        self.suite_name = suite_name
        self.test_cases = [] 
    
    def add_test(self, test_case):
        self.test_cases.append(test_case)
        print(f" Added test '{test_case.test_name}' to suite '{self.suite_name}'")
    
    def run_all_tests(self):
        print("\n" + "=" * 60)
        print(f"  EXECUTING TEST SUITE: {self.suite_name}")
        print("=" * 60)
        
        for test in self.test_cases:
            print(f"\nTest: [{test.test_id}] {test.test_name}")
            print(f"Module: {test.module}")
            
            # Check if it's an automated test
            if isinstance(test, AutomatedTestCase):
                print(f"Type: Automated ({test.automation_tool})")
            else:
                print("Type: Manual")
            
            # Get result from user
            while True:
                result = input("Enter result (Pass/Fail): ").strip()
                if result.lower() in ["pass", "fail"]:
                    test.execute_test(result)
                    print(f"Status updated to: {test.status}")
                    break
                else:
                    print("Invalid input. Please enter 'Pass' or 'Fail'.")
        
        print("\n" + "=" * 60)
        print("  ALL TESTS EXECUTED!")
        print("=" * 60)
    
    def save_results_to_csv(self, file_name):
        headers = ["Test ID", "Test Name", "Module", "Status", "Automation Tool"]
        
        with open(file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            
            for test in self.test_cases:
                writer.writerow(test.to_csv_row())
        
        print(f"\nResults saved to '{file_name}'")
    
    def summary_report(self):
        total = len(self.test_cases)
        passed = sum(1 for t in self.test_cases if t.status.lower() == "pass")
        failed = sum(1 for t in self.test_cases if t.status.lower() == "fail")
        not_executed = sum(1 for t in self.test_cases if t.status.lower() == "not executed")
        
        print("\n" + "=" * 60)
        print(f"  TEST EXECUTION SUMMARY: {self.suite_name}")
        print("=" * 60)
        print(f"  Total Tests      : {total}")
        print(f"  Passed           : {passed}")
        print(f"  Failed           : {failed}")
        print(f"  Not Executed     : {not_executed}")
        print("=" * 60)
        
        if total > 0 and (passed + failed) > 0:
            pass_rate = (passed / (passed + failed)) * 100
            print(f"  Pass Rate        : {pass_rate:.1f}%")
            print("=" * 60)

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("     MINI TEST MANAGEMENT TOOL")
    print("=" * 60)
    
    # Create 2 Manual Test Cases
    manual_test_1 = TestCase(
        test_id="TC001",
        test_name="Verify Login with Valid Credentials",
        module="Authentication"
    )
    
    manual_test_2 = TestCase(
        test_id="TC002",
        test_name="Verify Password Reset Flow",
        module="Authentication"
    )
    
    # Create 2 Automated Test Cases
    automated_test_1 = AutomatedTestCase(
        test_id="TC003",
        test_name="Verify Homepage Load Time",
        module="Performance",
        automation_tool="Selenium"
    )
    
    automated_test_2 = AutomatedTestCase(
        test_id="TC004",
        test_name="Verify API Response Status",
        module="API Testing",
        automation_tool="Playwright"
    )
    
    # Create a Test Suite
    print("\nCreating Test Suite...")
    suite = TestSuite(suite_name="Sprint 24 Regression Suite")
    
    # Add all test cases to the suite
    print("\nAdding Test Cases to Suite:")
    suite.add_test(manual_test_1)
    suite.add_test(manual_test_2)
    suite.add_test(automated_test_1)
    suite.add_test(automated_test_2)
    
    # Display all test cases before execution
    print("\nTest Cases in Suite:")
    for test in suite.test_cases:
        test.display_test_case()
    
    # Execute all tests
    suite.run_all_tests()
    
    # Save results to CSV
    suite.save_results_to_csv("test_results.csv")
    
    # Print execution summary
    suite.summary_report()
    
    print("\nTest Management Tool execution completed!")
    print("\nCheck 'test_results.csv' for the execution report.")