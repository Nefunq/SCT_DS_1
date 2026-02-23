import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the main population data
# The CSV has 3 header rows to skip before the actual column names
pop_df = pd.read_csv(
    'API_SP.POP.TOTL_DS2_en_csv_v2_40826.csv',
    skiprows=3,
    encoding='utf-8'
)

# Load the country metadata
meta_df = pd.read_csv(
    'Metadata_Country_API_SP.POP.TOTL_DS2_en_csv_v2_40826.csv',
    encoding='utf-8'
)

# Merge on Country Code
merged = pd.merge(pop_df, meta_df, on='Country Code', how='inner')

# Keep only rows with a defined Region (i.e., actual countries, not aggregates)
merged = merged[merged['Region'].notna()]

# Select the year 2024 and convert to numeric
merged['2024'] = pd.to_numeric(merged['2024'], errors='coerce')
merged = merged.dropna(subset=['2024'])

# Aggregate population by region
region_pop = merged.groupby('Region', as_index=False)['2024'].sum()
region_pop = region_pop.sort_values('2024', ascending=False)

# Create the bar chart
plt.figure(figsize=(12, 6))
plt.bar(region_pop['Region'], region_pop['2024'] / 1e9)  # convert to billions
plt.xlabel('Region')
plt.ylabel('Total Population (billions)')
plt.title('World Population Distribution by Region (2024)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('ds_task1.1.png')
plt.show()

# Histogram of country populations
plt.figure(figsize=(10, 6))

# plt.hist(merged['2024'] , bins=bins, edgecolor='black')
# plt.xlabel('Population (raw count)')

# Logarithmic x-axis to better show the wide range
bins = np.logspace(np.log10(merged['2024'].min()), 
                   np.log10(merged['2024'].max()), 30)
plt.hist(merged['2024'] , bins=bins, edgecolor='black')
plt.xscale('log')
plt.xlabel('Population (raw count, log scale)')
plt.ylabel('Number of countries')
plt.title('Distribution of Country Populations in 2024')
plt.tight_layout()
plt.savefig('ds_task1.2.png')
plt.show()
