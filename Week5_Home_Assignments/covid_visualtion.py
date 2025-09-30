import Week4and5_Home_Assignments.covid_analysis as ca
import matplotlib.pyplot as plt


class CovidVisualization(ca.CovidAnalysis):
    def __init__(self, file_path):
        super().__init__(file_path)

    #Bar Chart of Top 10 Countries by Confirmed Cases
    def bar_chart_top_10_countries_by_confirmed_cases(self):
        top_10 = self.df.nlargest(10, 'Confirmed')
        plt.figure(figsize=(10, 6))
        plt.bar(top_10['Country/Region'], top_10['Confirmed'], color='skyblue')
        plt.xlabel('Country/Region')
        plt.ylabel('Confirmed Cases')
        plt.title('Top 10 Countries by Confirmed COVID-19 Cases')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    covid_vis = CovidVisualization("D:\AI Engineer Training\Python_Coding\Week4_Home_Assignments\country_wise_latest_1.csv")
    covid_vis.bar_chart_top_10_countries_by_confirmed_cases()
