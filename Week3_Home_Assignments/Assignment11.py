import numpy as np

class TestReport:
    def __init__(self, test_execution_time):
        self.test_execution_time = test_execution_time

    def average_time(self):
        return np.mean(self.test_execution_time)
    
    def max_time(self):
        return np.max(self.test_execution_time)
    
class Regression_Report(TestReport):
    def __init__(self, test_execution_time):
        super().__init__(test_execution_time)

    def slow_tests(self, threshold):
        mask = self.test_execution_time > threshold
        return self.test_execution_time[mask]
    
R1 = Regression_Report(np.array([10, 15, 20, 25, 30, 35, 40, 45, 50]))  

print("Average Test Execution Time: ", R1.average_time())
print("Maximum Test Execution Time: ", R1.max_time())
print("Tests exceeding 30 seconds: ", R1.slow_tests(30))