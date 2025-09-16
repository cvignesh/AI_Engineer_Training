import numpy as np

class ManualTester:
    def analyse(self, data):
        print(f"First 5 test execution times: {data[:5]}")

class AutomationTester:
    def analyse(self, data):
        print(f"Fastes Execution time : {data.min()}") 

class PerformanceTester:
    def analyse(self, data):
        print(f"95th percentile execution time : {np.percentile(data, 95)}")

def show_analysis(tester, data):
    tester.analyse(data)



if __name__ == "__main__":
    execution_time = np.array([29,4,19,65,34,29,12,13,45,10,45,38])

    manual_tester = ManualTester()
    AutomationTester_tester = AutomationTester()
    performance_tester = PerformanceTester()

    show_analysis(manual_tester, execution_time)
    show_analysis(AutomationTester_tester, execution_time)
    show_analysis(performance_tester, execution_time)   
