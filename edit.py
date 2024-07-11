import pandas as pd

# Load the original dataset
csv_file = 'ModifiedCrimeData.csv'
df = pd.read_csv(csv_file)

# Select and rename columns for the new dataset
new_df = df[['Vict_Age', 'Vict_Sex', 'INCIDENT_AREA']].copy()
new_df.rename(columns={
    'Vict_Age': 'Victim_Age',
    'Vict_Sex': 'Victim_Sex',
    'INCIDENT_AREA': 'INCIDENT_AREA'
}, inplace=True)

# Save to new CSV file
new_df.to_csv('new_dataset.csv', index=False)

print("new_dataset.csv created successfully.")
