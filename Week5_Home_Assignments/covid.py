import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

class DataSet:
    def __init__(self,filename):
       self.filename = filename

    def loadCSV(self):
        try:
            self.df = pd.read_csv(self.filename)
            return self.df
        except FileNotFoundError:
            print(f"{self.filename} not found")
            return None

class CovidAnalysis(DataSet):
    def __init__(self, filename):
        super().__init__(filename)
        print(f"FileName is {self.filename}")
        self.loadCSV()

    #Summarize Case Counts by Region 
    # - Display total confirmed, death, and recovered cases for each region
    def Summarize_Case_Counts_By_Region(self):
        print("Summarization of Case Counts by Region:\n")
        print(self.df.groupby('WHO Region').agg({'Confirmed': 'sum', 'Deaths': 'sum', 'Recovered' : 'sum'}).reset_index())

    #Filter Low Case Records 
    # - Exclude entries where confirmed cases are < 10.
    def Filter_Low_Case_Records(self):
        print("Low Case Records\n")
        print(self.df[self.df["Confirmed"]>10])

    #Identify Region with Highest Confirmed Cases 
    def Region_With_Highest_Case_Count(self):
        max_id = self.df.groupby("WHO Region")["Confirmed"].idxmax()
        print("Region with High Case Count\n")
        filter_df = self.df.loc[max_id,['Country/Region','WHO Region','Confirmed']]
        print(filter_df.sort_values(by='Confirmed', ascending = False))

    #Sort Data by Confirmed Cases 
    # - Save sorted dataset into a new CSV file.
    def sort_by_Confirmed_Case(self, filename_to_export):
        Sorted_DataSet = self.df.sort_values(by='Confirmed') 
        print(Sorted_DataSet[["Country/Region","Confirmed"]])
        Sorted_DataSet.to_csv("filename_to_export",index=False)
        print("Sorted datset is exported to csv")

    # Top 5 Countries by Case Count
    def Top_5_Countries_ByCase_Count(self):
        Decending_Data_Set = self.df.sort_values(by="Confirmed",ascending=False)
        print(" Top 5 Countries by Case Count\n")
        print(Decending_Data_Set.head()[["Country/Region","Confirmed"]])

    # Region with Lowest Death Count
    def Region_With_Lowest_Death_Count(self):
        print("Region with Lowest Death Count\n")
        print(self.df.loc[self.df["Confirmed"].idxmin(),["Country/Region"]])

    # Loweest WHO Region Lowest Death Count
    def Lowest_WHO_Region_With_Low_Death_Count(self):
        print("Loweest WHO Region by Lowest Death Count")
        print(self.df.groupby("WHO Region")["Confirmed"].idxmin().idxmin())

    # India’s Case Summary (as of April 29, 2020) 
    def print_India_Summary(self):
        print("India's Case Summary")
        print(self.df[self.df["Country/Region"]=="India"])

    # Calculate Mortality Rate by Region 
    # - Death-to-confirmed case ratio. 
    def calculate_mortality_rate_by_region(self):
        Confirmed_Total_RegionWise = self.df.groupby("WHO Region")["Confirmed"].sum()
        Death_Total_RegionWise = self.df.groupby("WHO Region")["Deaths"].sum()
        print("Mortality rate by Region\n")
        mortality_rate = ( Death_Total_RegionWise / Confirmed_Total_RegionWise ) *100
        print(mortality_rate.to_frame(name="Mortality Rate (%)"))

    # Compare Recovery Rates Across Regions
    def compare_Recovery_rate_regiion(self):
        Confirmed_Total_RegionWise = self.df.groupby("WHO Region")["Confirmed"].sum()
        Recovered_Total_RegionWise = self.df.groupby("WHO Region")["Recovered"].sum()
        print(( Recovered_Total_RegionWise / Confirmed_Total_RegionWise ) *100)

    #  Detect Outliers in Case Counts 
    # - Use mean ± 2*std deviation. 
    def Detect_Outliers_Case_Count(self):
       mean_confirmed = self.df["Confirmed"].mean()
       std_dv_confirmed = self.df["Confirmed"].std()

       # Define the lower and upper bounds for outliers
       Upper_Bound_Val = mean_confirmed + 2 * std_dv_confirmed
       Lower_Bound_Val = mean_confirmed - 2 * std_dv_confirmed

       print("Outliers in case count\n")
       # Outliers Calculation
       print(self.df[(self.df['Confirmed'] < Upper_Bound_Val) | (self.df['Confirmed'] > Lower_Bound_Val)])

    # Identify Regions with Zero Recovered Cases 
    def Region_With_Zero_Recoevred_Cases(self):
        print("Region with Zero Recovered Case\n")
        print(self.df[self.df["Recovered"] == 0])

    #Group Data by Country and Region
    def group_WHO_Region(self):
        print("Data group by WHO Region\n")
        print(self.df.groupby("WHO Region").size().to_frame(name="Record Count").reset_index())

class CovidVisualization(CovidAnalysis):
    def __init__(self, file_path):
        super().__init__(file_path)

    #Bar Chart of Top 10 Countries by Confirmed Cases
    def Bar_Chart_of_Top_N_Countries_by_Confirmed_Cases(self,N):
        self.df.sort_values(by="Confirmed",ascending=False)
        top_10_confirmed_countries = self.df.head(N).loc[ : , ["Country/Region","Confirmed"]]
        plt.bar(top_10_confirmed_countries["Country/Region"],top_10_confirmed_countries["Confirmed"])
        # Rotate y-axis tick labels by 90 degrees
        plt.xticks(rotation=90)
        plt.title("Bar Chart of Top 10 Countries by Confirmed Cases")
        plt.xlabel("Country")
        plt.ylabel("Confirmed Case Count")
        plt.xticks(rotation=45)
        plt.yticks(rotation=45)
        GraphName = f"Bar_Chart_of_Top_N_Countries_by_Confirmed_Cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(f"D:\AI Engineer Training\Python_Coding\Week4and5_Home_Assignments\Output_Graph\{GraphName}")

    #Pie Chart of Global Death Distribution by Region
    def Pie_Chart_of_Global_Death_Distribution_by_Region(self):
        Death_Distribution_By_Region = self.df.groupby("WHO Region")["Deaths"].sum()
        Death_Distribution_By_Region.values
        plt.figure(figsize=(8, 8))  # Increase figure size
        plt.pie(Death_Distribution_By_Region.values,autopct='%1.2f%%',labels=Death_Distribution_By_Region.index)
        #Adding legend to pie chart and display on top left
        plt.legend(loc='upper left',bbox_to_anchor=(1, 1))
        plt.tight_layout() # Adjust layout to prevent overlap
        plt.xticks(rotation=45)
        plt.yticks(rotation=45)
        GraphName = f"Pie_Chart_of_Global_Death_Distribution_by_Region{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(f"D:\AI Engineer Training\Python_Coding\Week4and5_Home_Assignments\Output_Graph\{GraphName}")

    #Line Chart comparing Confirmed and Deaths for Top 5 Countries
    def Line_Chart_comparing_Confirmed_and_Deaths_for_Top_N_Countries(self,N):
        Top_N_Countries = self.df.nlargest(N, 'Confirmed')[["Country/Region", "Confirmed", "Deaths"]]
        plt.figure(figsize=(14, 6))
        x_positions = range(len(Top_N_Countries["Country/Region"]))
        plt.plot(x_positions, Top_N_Countries["Confirmed"], marker='*', linestyle='-' , label='Confirmed Cases')
        plt.plot(x_positions, Top_N_Countries["Deaths"], marker='^', linestyle='-' , label='Deaths')

        plt.title(f"Confirmed Cases vs Deaths for Top {N} Countries")
        plt.xlabel("Country")
        plt.ylabel("Count")
        plt.xticks(x_positions, Top_N_Countries["Country/Region"], rotation=45)

        # Format y-axis ticks to show actual numbers
        plt.ticklabel_format(style='plain', axis='y')
        plt.yticks(rotation=45)
        plt.grid(True,alpha=0.7)
        plt.legend()
        GraphName = f"Line_Chart_comparing_Confirmed_and_Deaths_for_Top_N_Countries{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(f"D:\AI Engineer Training\Python_Coding\Week4and5_Home_Assignments\Output_Graph\{GraphName}")

    #Scatter Plot of Confirmed Cases vs Recovered Cases
    def Scatter_Plot_of_Confirmed_Cases_vs_Recovered_Cases(self):
        plt.figure(figsize=(40, 6))
        plt.scatter(self.df["Country/Region"],self.df["Confirmed"],alpha=0.5,cmap='rainbow',edgecolors='black',s=500)
        plt.scatter(self.df["Country/Region"],self.df["Recovered"],alpha=0.5,cmap='plasma',edgecolors='black',s=500)
        plt.title("Scatter Plot of Confirmed Cases vs Recovered Cases")
        plt.xticks(rotation=45)
        plt.ticklabel_format(style='plain', axis='y')
        plt.yticks(rotation=45)
        plt.legend(['Confirmed Cases','Recovered Cases'])
        GraphName = f"Scatter_Plot_of_Confirmed_Cases_vs_Recovered_Cases{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(f"D:\AI Engineer Training\Python_Coding\Week4and5_Home_Assignments\Output_Graph\{GraphName}")

    #Histogram of Death Counts across all Regions
    def Histogram_of_Death_Counts_across_all_Regions(self):
        WHO_Region_Deaths = self.df.groupby("WHO Region")["Deaths"].sum()
        WHO_Region_Deaths
        plt.figure(figsize=(10, 6))
        plt.hist(self.df.groupby("WHO Region")["Deaths"].sum(), bins=5, color='skyblue', edgecolor='black', alpha=0.7)
        plt.title("Histogram of Death Counts across all Regions")
        plt.xlabel("Number of Deaths")
        plt.ylabel("Frequency")   
        GraphName = f"Histogram_of_Death_Counts_across_all_Regions{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(f"D:\AI Engineer Training\Python_Coding\Week4and5_Home_Assignments\Output_Graph\{GraphName}")

    #Stacked Bar Chart of Confirmed, Deaths, and Recovered for 5 Selected Countries
    def Stacked_Bar_Chart_of_Confirmed_Deaths_and_Recovered_for_5_Selected_Countries(self,No_Of_Countries):
        selected_countries = self.df[self.df["Country/Region"].isin(No_Of_Countries)]
        selected_countries.set_index("Country/Region",inplace=True)
        selected_countries[["Confirmed","Deaths","Recovered"]].plot(kind='bar',stacked=True,figsize=(10,6))
        plt.title("Stacked Bar Chart of Confirmed, Deaths, and Recovered for Selected Countries")
        plt.ylabel("Case Count")
        plt.ticklabel_format(style='plain', axis='y')
        plt.xticks(rotation=45)
        plt.yticks(rotation=45)
        GraphName = f"Stacked_Bar_Chart_of_Confirmed_Deaths_and_Recovered_for_Selected_Countries{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(f"D:\AI Engineer Training\Python_Coding\Week4and5_Home_Assignments\Output_Graph\{GraphName}")

    #Box Plot of Confirmed Cases across Regions
    def Box_Plot_of_Confirmed_Cases_across_Regions(self):
        plt.figure(figsize=(10, 6))
        self.df.groupby("WHO Region")["Confirmed"].sum().plot(kind='box',figsize=(10,6))
        plt.title("Box Plot of Confirmed Cases across Regions") 
        plt.ticklabel_format(style='plain', axis='y')
        GraphName = f"Box_Plot_of_Confirmed_Cases_across_Regions{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(f"D:\AI Engineer Training\Python_Coding\Week4and5_Home_Assignments\Output_Graph\{GraphName}")

    # Trend Line: Plot Confirmed cases for India vs another chosen country (side by side comparison)
    def Trend_Line_India_vs_Another_Country(self,country_name):
    
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        # India
        india_data = self.df[self.df["Country/Region"] == "India"]
        ax[0].plot(["Last Week", "Current"], [india_data["Confirmed last week"].values[0], india_data["Confirmed"].values[0]], marker='o')
        ax[0].set_title("India Confirmed Cases Trend")
        ax[0].set_ylabel("Confirmed Cases")
        ax[0].set_xticks([0, 1])
        ax[0].set_xticklabels(["Last Week", "Current"])
        ax[0].legend(['India'], loc='upper left')
        ax[0].ticklabel_format(style='plain', axis='y')
        for label in ax[0].get_yticklabels():
            label.set_rotation(45)
        # Second Country
        Second_COuntry_Data = self.df[self.df["Country/Region"] == country_name]
        ax[1].plot(["Last Week", "Current"], [Second_COuntry_Data["Confirmed last week"].values[0], Second_COuntry_Data["Confirmed"].values[0]], marker='o', color='orange')
        ax[1].set_title(f"{country_name} Confirmed Cases Trend")
        ax[1].set_ylabel("Confirmed Cases")
        ax[1].set_xticks([0, 1])
        ax[1].set_xticklabels(["Last Week", "Current"])
        ax[1].legend(['Brazil'], loc='upper left')
        ax[1].ticklabel_format(style='plain', axis='y')
        for label in ax[1].get_yticklabels():
            label.set_rotation(45)
        plt.tight_layout()
        GraphName = f"Trend_Line_India_vs_Another_Country{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(f"D:\AI Engineer Training\Python_Coding\Week4and5_Home_Assignments\Output_Graph\{GraphName}")


if __name__ == "__main__":
    Covid_Data = CovidVisualization("D:\AI Engineer Training\Python_Coding\Week4and5_Home_Assignments\country_wise_latest_1.csv")
    Covid_Data.Bar_Chart_of_Top_N_Countries_by_Confirmed_Cases(15)
    Covid_Data.Pie_Chart_of_Global_Death_Distribution_by_Region()
    Covid_Data.Line_Chart_comparing_Confirmed_and_Deaths_for_Top_N_Countries(6)
    Covid_Data.Scatter_Plot_of_Confirmed_Cases_vs_Recovered_Cases()
    Covid_Data.Histogram_of_Death_Counts_across_all_Regions()
    Covid_Data.Stacked_Bar_Chart_of_Confirmed_Deaths_and_Recovered_for_5_Selected_Countries(["US", "India", "Brazil", "Russia", "United Kingdom"])
    Covid_Data.Box_Plot_of_Confirmed_Cases_across_Regions()
    Covid_Data.Trend_Line_India_vs_Another_Country("US")

# if __name__ == "__main__":
#     Covid_Data = CovidAnalysis("D:\AI Engineer Training\Python_Coding\Week4and5_Home_Assignments\country_wise_latest_1.csv")
#     Covid_Data.Summarize_Case_Counts_By_Region()
# #     print("*" *100)
# #     Covid_Data.Filter_Low_Case_Records()
#     print("*" *100)
#     Covid_Data.Region_With_Highest_Case_Count()
#     print("*" *100)
#     Covid_Data.sort_by_Confirmed_Case("Sorted_data.csv")
#     print("*" *100)
#     Covid_Data.Top_5_Countries_ByCase_Count()
#     print("*" *100)
#     Covid_Data.Region_With_Lowest_Death_Count()
#     print("*" *100)
#     Covid_Data.Lowest_WHO_Region_With_Low_Death_Count()
#     print("*" *100)
#     Covid_Data.print_India_Summary()
#     print("*" *100)
#     Covid_Data.calculate_mortality_rate_by_region()
#     print("*" *100)
#     Covid_Data.Detect_Outliers_Case_Count()
#     print("*" *100)
#     Covid_Data.Region_With_Zero_Recoevred_Cases()
#     print("*" *100)
#     Covid_Data.group_WHO_Region()



    
