import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler


class EDA:
    def __init__(self,dataset_filepath):
        self.dataset_filepath = dataset_filepath
        
    def load_csv(self):
        try:
            df = pd.read_csv(self.dataset_filepath)
            return df
        except FileNotFoundError:
            print("No file found")
            return None
        
    def compute_statistical_measures(self, df: pd.DataFrame):
        print("Mean \n",df.mean())
        print("Median \n",df.median())
        print("Standard Deviation \n",df.std())
        print(df.corr())

    def detect_outlier_return_cleaned_data(self, df: pd.DataFrame):
        """
        IQR = Q3 - Q1
        Lower Bound = Q1 - 1.5*IQR
        Upper Bound = Q3 + 1.5*IQR
        """
        df = df.select_dtypes(include="number") # remove any non-numeric column
        Q1 = df.quantile(0.25)
        Q3 = df.quantile(0.75)
        IQR = Q3-Q1
        Lower_Bound = Q1 - 1.5*IQR
        Upper_Bound = Q3 + 1.5*IQR
        print("Datatype of UpperBound is ",type(Upper_Bound))
        print("Q1 - ",Q1)
        print("Q3 - ",Q3)
        print("IQR - ",IQR)
        print("Lower Bound - ", Lower_Bound)
        print("Upper Bound - ",Upper_Bound)

        # Removing the outliers and return cleaned dataset
        cleaned_df = df[((df>=Lower_Bound) & (df<=Upper_Bound)).all(axis=1)] #.all(axis=1) ensures every numeric column in that row is within bounds.
        return cleaned_df
    
    def scale_df(self, original_df):
        scalar = StandardScaler()
        scaled_data = scalar.fit_transform(original_df)
        columns_from_df = original_df.columns
        scaled_df = pd.DataFrame(scaled_data,columns=columns_from_df)
        return scaled_df
    
    def plot_histograms(self,df, title_prefix):
        
        n_cols = len(df.columns)
        n_rows = (n_cols + 1) // 2  # Calculate number of rows needed (2 plots per row)
        
        plt.figure(figsize=(12, 4 * n_rows))
        
        for idx, col in enumerate(df.columns, 1):
            plt.subplot(n_rows, 2, idx)
            sns.histplot(data=df[col], kde=True)
            plt.title(f'{title_prefix} Distribution of {col}')
            plt.xlabel(col)
            plt.ylabel('Count')
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    print("Started")
    Covid_EDA = EDA(r"D:\AI Engineer Training\Python_Coding\Week6_Home_Assignments\country_wise_latest_1.csv")
    covid_df = Covid_EDA.load_csv()
   
    print(covid_df.head())
    covid_df_confirmed_newcases = covid_df.set_index('Country/Region').loc[:,['Confirmed', 'New cases']]
    covid_df_confirmed = covid_df.set_index('Country/Region').loc[:,['Confirmed']]
    print(covid_df_confirmed_newcases)
    Covid_EDA.compute_statistical_measures(covid_df_confirmed_newcases)
    cleaned_df = Covid_EDA.detect_outlier_return_cleaned_data(covid_df_confirmed_newcases)
    print("Cleaned DataSet \n",cleaned_df)
    cleaned_df.to_csv("Cleaned_DataSet_New11.csv")

    print("Skewness before scaling:/n",cleaned_df.skew())

    # Histogram before Normalization
    Covid_EDA.plot_histograms(cleaned_df,"Before Scaling")

    #scaling data
    scaled_df = Covid_EDA.scale_df(cleaned_df)
    print("Scaled Data:/n",scaled_df)

    # skewness after scaling
    print("Skewness after scaling:/n",scaled_df.skew())

    # Histogram after Normalization
    Covid_EDA.plot_histograms(scaled_df,"Before Scaling")


  