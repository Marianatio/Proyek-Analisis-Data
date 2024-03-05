# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

# Set seaborn style
sns.set(style='dark')

# Function to create rents over time data frame
def create_rents_over_time(df):
    df['dteday'] = pd.to_datetime(df['dteday'])
    monthly_df = df.resample('M', on='dteday').sum()
    return monthly_df

# Function to aggregate bike rentals by hour data frame
def by_hour(df):
    hourly_agg = df.groupby("hours").agg({
        "instant_y": "nunique",
        "count_cr_y": ["max", "min"]
    })
    return hourly_agg


# Load csv files
days_hours_df = pd.read_csv("days_hours.csv")
datetime_columns = ["dteday"]
days_hours_df.sort_values(by="dteday", inplace=True)
days_hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_hours_df[column] = pd.to_datetime(days_hours_df[column])

# Streamlit Sidebar
with st.sidebar:
    # Add Header
    st.header("Proyek Analisis Data")
    st.header("Dashboard Bike-Rental")

# Create Dataframes
rents_over_time_df = create_rents_over_time(days_hours_df)
byhour_df = by_hour(days_hours_df)

# Bike Rentals Over Time (Aggregated by Month) Visualization
st.subheader("Bike Rentals Over Time")
plt.figure(figsize=(10, 5))
plt.plot(rents_over_time_df.index, rents_over_time_df['count_cr_x'], marker='o', linewidth=2, color="#72BCD4")
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Penyewaan Sepeda Berdasarkan Bulan', loc="center", fontsize=18)
plt.xticks(rotation=45,  fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()
st.pyplot(plt)

# Bike Rentals by Hour Visualization
st.subheader("Bike Rentals by Hour")
plt.figure(figsize=(10, 5))
x = byhour_df.index
y_max = byhour_df[('count_cr_y', 'max')]
y_min = byhour_df[('count_cr_y', 'min')]
plt.bar(x, y_max, label='Penyewaan Paling Banyak', color='green')
plt.bar(x, y_min, label='Penyewaan Paling Sedikit', color='red')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan Sepeda')
plt.title('Jumlah Penyewaan Sepeda Paling Banyak dan Paling Sedikit Pada Jam Tertentu')
hour_labels = [str(i) for i in x]
plt.xticks(x, hour_labels)
plt.legend()

for i, (max_val, min_val) in enumerate(zip(y_max, y_min)):
    plt.text(i, max_val, str(max_val), ha='center', va='bottom', fontweight='bold')
    plt.text(i, min_val, str(min_val), ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
st.pyplot(plt)