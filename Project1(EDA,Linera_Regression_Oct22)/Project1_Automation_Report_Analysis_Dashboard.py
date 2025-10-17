import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

st.set_page_config(page_title="Automation Test Analytics Dashboard", layout="wide")
st.title("Automation Test Analytics Dashboard")

# -----------------------------
# Upload Dataset
# -----------------------------
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Dataset loaded successfully!")
    st.dataframe(df)

    # Convert Execution Date to datetime
    df['Execution Date'] = pd.to_datetime(df['Execution Date'])

    # -----------------------------
    # Filters
    # -----------------------------
    st.sidebar.header("Filters")
    modules = df['Module'].unique().tolist()
    selected_modules = st.sidebar.multiselect("Select Module(s):", modules, default=modules)

    min_date = df['Execution Date'].min()
    max_date = df['Execution Date'].max()
    date_range = st.sidebar.date_input("Execution Date Range:", [min_date, max_date])

    # Apply filters
    df_filtered = df[(df['Module'].isin(selected_modules)) &
                     (df['Execution Date'] >= pd.to_datetime(date_range[0])) &
                     (df['Execution Date'] <= pd.to_datetime(date_range[1]))]

    # -----------------------------
    # Summary Metrics
    # -----------------------------
    st.header("📊 Summary Metrics")
    total_tests = len(df_filtered)
    passed_tests = len(df_filtered[df_filtered['Status']=='Passed'])
    failed_tests = len(df_filtered[df_filtered['Status']=='Failed'])
    skipped_tests = len(df_filtered[df_filtered['Status']=='Skipped'])
    avg_duration = round(df_filtered['Duration(seconds)'].mean(), 2)

    # Flaky Tests
    flaky_tests = df_filtered.groupby('Testcase Name')['Status'].nunique()
    flaky_tests_count = len(flaky_tests[flaky_tests > 1])

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Tests", total_tests)
    col2.metric("Passed Tests", passed_tests)
    col3.metric("Failed Tests", failed_tests)
    col4.metric("Skipped Tests", skipped_tests)
    col5.metric("Average Duration (sec)", avg_duration)
    col6.metric("Flaky Tests", flaky_tests_count)

    # -----------------------------
    # Test Coverage & Execution Insights
    # -----------------------------
    st.header("📈 Test Coverage & Execution Insights")
    pass_ratio = (passed_tests/total_tests)*100
    failed_ratio = (failed_tests/total_tests)*100
    skipped_ratio = (skipped_tests/total_tests)*100

    col1, col2, col3 = st.columns(3)
    col1.metric("Pass Ratio (%)", round(pass_ratio,2))
    col2.metric("Fail Pass Ratio (%)", round(pass_ratio,2))
    col3.metric("Skip Ratio (%)", round(skipped_ratio,2))

    ########################## Mdoule-wise status distribution#########################################

    module_status_pct = (
    df_filtered.groupby('Module')['Status']
    .value_counts(normalize=True)   # gives proportion per module
    .mul(100)                       # convert to %
    .rename('Percentage')           # THIS creates the 'Percentage' column
    .reset_index()
    )

    # Pivot for plotting
    module_status_pivot = module_status_pct.pivot(index='Module', columns='Status', values='Percentage')

    # Plot stacked bar chart
    fig_stck_bar, ax = plt.subplots(figsize=(20,6))
    module_status_pivot.plot(kind='bar', stacked=True, colormap='Set2', ax=ax)

    ax.set_ylabel('Percentage')
    ax.set_title('Module-wise Status Distribution (%)')
    ax.set_xticklabels(module_status_pivot.index, rotation=45)
    ax.legend(title='Status')
    plt.tight_layout()

    st.subheader("Module-wise Status Distribution (%)")
    st.pyplot(fig_stck_bar)

    # Count of each status
    status_counts = df['Status'].value_counts()
    st.subheader("Overall Test Status Distribution")

    # Plot pie chart
    fig, ax = plt.subplots(figsize=(4,4))
    ax.pie(
        status_counts,
        labels=status_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops={'edgecolor': 'white'}
    )
    ax.axis('equal')  # Equal aspect ratio for a perfect circle
    st.pyplot(fig)

    ################### Test Execution Frequency ##########################################

    # Slider to select number of top tests
    top_n = st.slider("Select number of top executed tests to display:", min_value=1, max_value=50, value=10, step=1)

    # Get top N executed test cases
    test_freq_top = df_filtered['Testcase Name'].value_counts().head(top_n)

    # Plot horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, max(4, top_n*0.3)))  # dynamically adjust height
    ax.barh(test_freq_top.index[::-1], test_freq_top.values[::-1], color='skyblue')  # reverse for descending order
    ax.set_xlabel("Execution Count")
    ax.set_ylabel("Testcase Name")
    ax.set_title(f"Top {top_n} Most Executed Test Cases")

    # Add count labels on bars
    for i, v in enumerate(test_freq_top.values[::-1]):
        ax.text(v + 0.5, i, str(v), color='blue', va='center')

    plt.tight_layout()
    st.pyplot(fig)

    ########################Avg Test Execution Duration Over time #####################################################

    # Convert dates safely
    df_filtered['Execution Date'] = pd.to_datetime(df_filtered['Execution Date'], errors='coerce')
    df_filtered = df_filtered.dropna(subset=['Execution Date'])

    st.subheader("Average Test Duration Over Time")

    # --- Date range filter ---
    min_date = df_filtered['Execution Date'].min()
    max_date = df_filtered['Execution Date'].max()

    start_date, end_date = st.date_input(
        "Select date range:",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Force datetime for consistency
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter data based on selected date range
    mask = (df_filtered['Execution Date'] >= start_date) & (df_filtered['Execution Date'] <= end_date)
    df_filtered_range = df_filtered.loc[mask]

    # Calculate average duration per day
    avg_duration_time = df_filtered_range.groupby('Execution Date')['Duration(seconds)'].mean().sort_index()

    # Plot
    fig2, ax2 = plt.subplots(figsize=(10,4))
    ax2.plot(avg_duration_time.index, avg_duration_time.values, marker='o', linestyle='-', color='skyblue')

    # Formatting
    ax2.set_ylabel("Avg Duration (sec)")
    ax2.set_xlabel("Execution Date")
    ax2.set_title("Average Test Duration Over Time")
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.xaxis.set_major_locator(mdates.DayLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig2)

    # -----------------------------
    # Bottlenecks & Performance Issues
    # -----------------------------

    ############################Long Running Tests############################################
    
    st.subheader("Top Long-running Tests")

    # Slider to choose Top N
    top_n = st.slider(
        "Show Top N Long-running Tests",
        min_value=5,
        max_value=50,
        value=10,
        step=1,
        key="top_n_slider"
    )

    # Compute average duration (used as reference)
    avg_duration = df_filtered['Duration(seconds)'].mean()

    # Filter long-running tests above average
    long_running = df_filtered[df_filtered['Duration(seconds)'] > avg_duration]

    # Sort by duration descending
    long_running_sorted = long_running.sort_values(by='Duration(seconds)', ascending=False)

    # Take Top N
    long_running_top = long_running_sorted.head(top_n)

    # Add comparison column (optional)
    long_running_top = long_running_top.assign(
        Above_Avg_Percent=((long_running_top['Duration(seconds)'] - avg_duration) / avg_duration * 100).round(1)
    )

    # Display DataFrame
    st.dataframe(long_running_top[['Testcase Name', 'Module', 'Duration(seconds)', 'Above_Avg_Percent', 'Execution Date']])

    # Bar chart
    fig, ax = plt.subplots(figsize=(8, 0.4 * len(long_running_top)))  # dynamic chart height
    ax.barh(long_running_top['Testcase Name'], long_running_top['Duration(seconds)'], color='orange')
    ax.set_xlabel("Duration (seconds)")
    ax.set_ylabel("Testcase Name")
    ax.set_title(f"Top {top_n} Long-running Testcases")
    ax.invert_yaxis()  # longest test on top
    st.pyplot(fig)

    #######################Long Running Tests Trend###############################################
    
    st.subheader("Long-running Tests (with Duration Trend)")

    # Ensure Execution Date is datetime
    df_filtered['Execution Date'] = pd.to_datetime(df_filtered['Execution Date'])

    # Sort by Testcase and Date for trend analysis
    df_sorted = df_filtered.sort_values(['Testcase Name', 'Execution Date'])

    # Compute previous duration per test
    df_sorted['Prev Duration'] = df_sorted.groupby('Testcase Name')['Duration(seconds)'].shift(1)

    # Compute duration change
    df_sorted['Change (%)'] = ((df_sorted['Duration(seconds)'] - df_sorted['Prev Duration']) / 
                            df_sorted['Prev Duration'] * 100).round(2)

    # Filter only long-running tests (above threshold)
    threshold_long = st.slider(
        "Show tests longer than this many seconds:",
        min_value=int(df_filtered['Duration(seconds)'].min()),
        max_value=int(df_filtered['Duration(seconds)'].max()),
        value=int(df_filtered['Duration(seconds)'].mean()),
        step=1,
        key="long_running_threshold" 
    )

    long_running = df_sorted[df_sorted['Duration(seconds)'] > threshold_long]

    # Display table
    st.dataframe(long_running[['Testcase Name', 'Module', 'Execution Date',
                            'Duration(seconds)', 'Prev Duration', 'Change (%)']])

    # Optional: Show top tests with highest increase in duration
    top_increase = long_running.nlargest(10, 'Change (%)').dropna(subset=['Change (%)'])

    if not top_increase.empty:
        st.subheader("📈 Top 10 Tests with Increased Duration")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(top_increase['Testcase Name'], top_increase['Change (%)'], color='tomato')
        ax.set_xlabel("Change in Duration (%)")
        ax.set_ylabel("Testcase Name")
        ax.set_title("Tests Getting Slower Over Time")
        st.pyplot(fig)

############################# Inidividual Test Case Execution duration Trend ##########################################

    st.subheader("Testcase Execution Duration Trend")

    # Ensure Execution Date is datetime
    df_filtered['Execution Date'] = pd.to_datetime(df_filtered['Execution Date'], errors='coerce')

    # Let user pick a testcase
    testcase_names = df_filtered['Testcase Name'].unique()
    test_selected = st.selectbox("Select a Testcase to view trend:", sorted(testcase_names))

    # Filter data for the selected testcase
    df_trend = df_filtered[df_filtered['Testcase Name'] == test_selected].sort_values('Execution Date')

    if not df_trend.empty:
        # Calculate average duration for reference
        avg_duration = df_trend['Duration(seconds)'].mean()

        # Create figure
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(
            df_trend['Execution Date'],
            df_trend['Duration(seconds)'],
            marker='o',
            linestyle='-',
            color='teal',
            label='Duration'
        )

        # Add average reference line
        ax.axhline(avg_duration, color='gray', linestyle='--', label=f'Avg Duration ({avg_duration:.1f}s)')

        # Formatting
        ax.set_title(f"Duration Trend for '{test_selected}'")
        ax.set_xlabel("Execution Date")
        ax.set_ylabel("Duration (seconds)")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show chart
        st.pyplot(fig)

        # Optionally show table for detail
        with st.expander("Show Execution History Data"):
            st.dataframe(df_trend[['Execution Date', 'Duration(seconds)', 'Module', 'Status']])
    else:
        st.warning("No execution data available for the selected testcase.")

  ########################## Execution Peaks #####################################################

    exec_peaks = df_filtered.groupby('Execution Date')['Testcase Name'].count()
    st.subheader("Execution Peaks (Tests per Day)")
    fig4, ax4 = plt.subplots(figsize=(10,4))
    ax4.plot(exec_peaks.index, exec_peaks.values, marker='o', color='green')
    ax4.set_ylabel("Number of Tests")
    ax4.set_xlabel("Execution Date")
    ax4.tick_params(axis='x', rotation=45)
    st.pyplot(fig4)

    # -----------------------------
    # Defect & Error Analysis
    # -----------------------------
    st.header("Defect & Error Analysis")
    top_errors = df_filtered['Error Message'].value_counts().head(10)
    st.subheader("Top Frequent Error Messages")
    fig5, ax5 = plt.subplots(figsize=(10,4))
    ax5.bar(top_errors.index, top_errors.values, color='red')
    ax5.set_ylabel("Count")
    ax5.set_xlabel("Error Message")
    ax5.tick_params(axis='x', rotation=45)
    st.pyplot(fig5)

    error_by_module = df_filtered[df_filtered['Status']=='Failed'].groupby('Module')['Error Message'].count()
    st.subheader("Error Count by Module")
    fig6, ax6 = plt.subplots(figsize=(8,4))
    ax6.bar(error_by_module.index, error_by_module.values, color='purple')
    ax6.set_ylabel("Failed Count")
    ax6.set_xlabel("Module")
    ax6.tick_params(axis='x', rotation=45)
    st.pyplot(fig6)

    error_trend = df_filtered[df_filtered['Status']=='Failed'].groupby('Execution Date')['Testcase Name'].count()
    st.subheader("Error Trend Over Time")
    fig7, ax7 = plt.subplots(figsize=(10,4))
    ax7.plot(error_trend.index, error_trend.values, marker='o', color='brown')
    ax7.set_ylabel("Failed Count")
    ax7.set_xlabel("Execution Date")
    ax7.tick_params(axis='x', rotation=45)
    st.pyplot(fig7)

    error_group_summary = df_filtered[df_filtered['Status']=='Failed'].groupby('Error Message').agg({'Module':'unique','Testcase Name':'unique'})
    st.subheader("Error Group Summary")
    st.dataframe(error_group_summary)  

    st.subheader("Error Distribution by Module")
    failed = df_filtered[df_filtered['Status'] == 'Failed']

    if not failed.empty:
        # Group by Module & Error Message
        error_by_module = (
            failed.groupby(['Module', 'Error Message'])
            .size()
            .reset_index(name='Count')
        )

        # Pivot to prepare for stacked bar
        pivot_data = error_by_module.pivot(index='Module', columns='Error Message', values='Count').fillna(0)

        # Plot stacked bar
        fig, ax = plt.subplots(figsize=(10, 5))
        pivot_data.plot(kind='bar', stacked=True, ax=ax, colormap='tab20')
        ax.set_ylabel("Failure Count")
        ax.set_xlabel("Module")
        ax.set_title("Error Distribution by Module")
        ax.legend(title="Error Message", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        st.pyplot(fig)
    else:
        st.info("No failed test cases found.")
      

       

    ####################### Flaky Tests Detection ###############################################
    st.header(" Flaky Tests Detection")

    # Identify flaky tests (having more than one unique status)
    flaky = df_filtered.groupby('Testcase Name')['Status'].nunique()
    flaky_tests_df = flaky[flaky > 1].reset_index().rename(columns={'Status': 'Unique Status Count'})

    if not flaky_tests_df.empty:
        st.metric("Total Flaky Tests", len(flaky_tests_df))

        st.subheader("Flaky Tests List")
        st.dataframe(flaky_tests_df)

        # Flaky tests by module
        flaky_module = (
            df_filtered[df_filtered['Testcase Name'].isin(flaky_tests_df['Testcase Name'])]
            .groupby('Module')['Testcase Name']
            .nunique()
            .sort_values(ascending=False)
        )

        st.subheader("Flaky Tests by Module")

        # Dynamic chart height
        fig8, ax8 = plt.subplots(figsize=(8, 0.5 * len(flaky_module)))
        ax8.barh(flaky_module.index, flaky_module.values, color='cyan')
        ax8.set_xlabel("Flaky Test Count")
        ax8.set_ylabel("Module")
        ax8.set_title("Modules with Flaky Tests")
        st.pyplot(fig8)

        # Optional: View trend for a selected flaky test
        st.subheader("🔍 View Flaky Test Execution Trend")
        flaky_test_selected = st.selectbox("Select a Flaky Testcase:", flaky_tests_df['Testcase Name'])

        flaky_trend = df_filtered[df_filtered['Testcase Name'] == flaky_test_selected].sort_values('Execution Date')
        if not flaky_trend.empty:
            fig9, ax9 = plt.subplots(figsize=(8, 4))
            ax9.plot(flaky_trend['Execution Date'], flaky_trend['Status'], marker='o', linestyle='-', color='orange')
            ax9.set_xlabel("Execution Date")
            ax9.set_ylabel("Status")
            ax9.set_title(f"Status History for '{flaky_test_selected}'")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig9)
    else:
        st.info("No flaky tests detected in the selected dataset.")

    ############ HeatMaps ##############################################

    st.header("Heatmaps for Visual QA Insights")

    # --- Filters ---
    modules = st.multiselect(
        "Select Modules:",
        options=df_filtered['Module'].unique(),
        default=df_filtered['Module'].unique()
    )

    min_date = df_filtered['Execution Date'].min()
    max_date = df_filtered['Execution Date'].max()
    date_range = st.date_input(
        "Select Date Range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Apply filters
    df_filtered_range = df_filtered[
        (df_filtered['Module'].isin(modules)) &
        (df_filtered['Execution Date'] >= pd.to_datetime(date_range[0])) &
        (df_filtered['Execution Date'] <= pd.to_datetime(date_range[1]))
    ]

    # --- Heatmap Type Selector ---
    heatmap_type = st.radio("Select Heatmap Type:",
                            ["Module vs Execution Date (Failure Rate %)",
                            "Module vs Execution Date (Avg Duration)",
                            "Flaky Tests per Module Heatmap",
                            "Module vs Error Messages"])

    ############################# Module vs Execution Date (Failure Rate %) ############################
    if heatmap_type == "Module vs Execution Date (Failure Rate %)":
        if not df_filtered_range.empty:
            failure_rate = df_filtered_range.pivot_table(
                index='Module',
                columns='Execution Date',
                values='Status',
                aggfunc=lambda x: (x=='Failed').sum() / len(x) * 100
            )
            failure_rate.columns = [d.strftime('%Y-%m-%d') for d in failure_rate.columns]

            fig, ax = plt.subplots(figsize=(min(30, max(12, 0.3*len(failure_rate.columns))),
                                            min(15, max(6, 0.5*len(failure_rate.index)))))
            sns.heatmap(failure_rate, cmap='Reds', annot=False, fmt=".1f", linewidths=0.5,
                        cbar_kws={'label': 'Failure Rate (%)'}, ax=ax)
            ax.set_title("Module vs Execution Date (Failure Rate %)")
            ax.set_xticklabels(failure_rate.columns, rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.info("No data available for selected filters.")

    ############################# Module vs Execution Date (Avg Duration) ############################
    elif heatmap_type == "Module vs Execution Date (Avg Duration)":
        if not df_filtered_range.empty:
            avg_duration = df_filtered_range.pivot_table(
                index='Module',
                columns='Execution Date',
                values='Duration(seconds)',
                aggfunc='mean'
            )
            avg_duration.columns = [d.strftime('%Y-%m-%d') for d in avg_duration.columns]

            fig, ax = plt.subplots(figsize=(min(30, max(12, 0.3*len(avg_duration.columns))),
                                            min(15, max(6, 0.5*len(avg_duration.index)))))
            sns.heatmap(avg_duration, cmap='YlOrBr', annot=False, fmt=".1f", linewidths=0.5,
                        cbar_kws={'label': 'Avg Duration (sec)'}, ax=ax)
            ax.set_title("Module vs Execution Date (Avg Duration)")
            ax.set_xticklabels(avg_duration.columns, rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.info("No data available for selected filters.")

    ########################### Flaky Tests per Module Heatmap ########################################
    elif heatmap_type == "Flaky Tests per Module Heatmap":
        st.subheader("Flaky Tests per Module Heatmap")

        # Identify flaky tests (multiple statuses)
        flaky_tests = df_filtered_range.groupby('Testcase Name')['Status'].nunique()
        flaky_tests = flaky_tests[flaky_tests > 1].reset_index(name='Unique Status Count')

        if not flaky_tests.empty:
            df_flaky = df_filtered_range[df_filtered_range['Testcase Name'].isin(flaky_tests['Testcase Name'])]
            flaky_count_by_module = df_flaky.groupby('Module')['Testcase Name'].nunique().reset_index()
            flaky_count_by_module = flaky_count_by_module.set_index('Module')
            heatmap_data = flaky_count_by_module.rename(columns={'Testcase Name':'Flaky Test Count'})

            fig, ax = plt.subplots(figsize=(6, max(4, 0.5*len(heatmap_data))))
            sns.heatmap(heatmap_data, annot=False, fmt="d", cmap="Oranges", linewidths=0.5,
                        cbar_kws={'label':'Number of Flaky Tests'}, ax=ax)
            ax.set_xlabel("")
            ax.set_ylabel("Module")
            ax.set_title("Number of Flaky Tests per Module")
            plt.yticks(rotation=0)
            st.pyplot(fig)
        else:
            st.info("No flaky tests detected for selected filters.")

    ########################### Module vs Error Messages ########################################
    elif heatmap_type == "Module vs Error Messages":
        failed = df_filtered_range[df_filtered_range['Status']=='Failed']
        if not failed.empty:
            error_matrix = failed.groupby(['Module', 'Error Message'])['Testcase Name'].nunique().unstack(fill_value=0)
            fig, ax = plt.subplots(figsize=(min(30, max(12, 0.3*len(error_matrix.columns))),
                                            min(15, max(6, 0.5*len(error_matrix.index)))))
            sns.heatmap(error_matrix, cmap='Oranges', annot=False, fmt='d', linewidths=0.5,
                        cbar_kws={'label': 'Number of Failed Tests'}, ax=ax)
            ax.set_title("Module vs Error Messages")
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
        else:
            st.info("No failed test cases found for selected filters.")