import pandas as pd

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

if __name__ == "__main__":
    Covid_Data = CovidAnalysis("D:\AI Engineer Training\Python_Coding\Week4_Home_Assignments\country_wise_latest_1.csv")
    Covid_Data.Summarize_Case_Counts_By_Region()
    print("*" *100)
    Covid_Data.Filter_Low_Case_Records()
    print("*" *100)
    Covid_Data.Region_With_Highest_Case_Count()
    print("*" *100)
    Covid_Data.sort_by_Confirmed_Case("Sorted_data.csv")
    print("*" *100)
    Covid_Data.Top_5_Countries_ByCase_Count()
    print("*" *100)
    Covid_Data.Region_With_Lowest_Death_Count()
    print("*" *100)
    Covid_Data.Lowest_WHO_Region_With_Low_Death_Count()
    print("*" *100)
    Covid_Data.print_India_Summary()
    print("*" *100)
    Covid_Data.calculate_mortality_rate_by_region()
    print("*" *100)
    Covid_Data.Detect_Outliers_Case_Count()
    print("*" *100)
    Covid_Data.Region_With_Zero_Recoevred_Cases()
    print("*" *100)
    Covid_Data.group_WHO_Region()



    
