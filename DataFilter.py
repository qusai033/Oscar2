import pandas as pd

file_path = 'C:/Users/q1n/Documents/Oscar 2/DuoResults.asc'
# Reading the .asc file
with open(file_path, 'r') as file:
    lines = file.readlines()
# Extracting data
data = []
header = []
for line in lines:
    if line.startswith('Index'):
        header = line.strip().split('\t')
    elif line.strip() and line[0].isdigit():
        data.append(line.strip().split('\t'))
# Creating a DataFrame
df = pd.DataFrame(data, columns=header)
# Reorder columns to match the CSV
columns_order = [
    'Index', 'Reason', 'Sys', 'Dia', 'HR', 'Mean', 'cSys', 'cDia', 'cHR',
    'cPP', 'cAP', 'cAIx', 'cAIx@75', 'cMAP', 'Hour', 'Minute', 'Month',
    'Day', 'Year', 'EC', 'cEC', 'cQC', 'Tag', 'Comments'
]
df = df.reindex(columns=columns_order)
df.fillna('', inplace=True)
# Saving to CSV
df.to_csv('C:/Users/q1n/Documents/processed_data1.csv', index=False)