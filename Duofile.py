import pandas as pd
import os

file_path = 'C:\\Users\\duobao\\Desktop\\DuoResults.asc'
with open(file_path, 'r') as file:
    lines = file.readlines()

tables = []
current_table = []
in_table_section = False
table_starts = [
    "Omitted BP Data Record Count",
    "Omitted Awake BP Data Record Count",
    "Omitted Asleep BP Data Record Count"
]

for line in lines:
    stripped_line = line.strip()
    if any(start in stripped_line for start in table_starts):
        if current_table:
            df_table = pd.DataFrame(current_table)
            tables.append(df_table)
            current_table = []
        in_table_section = True
        print(f"Detected start of a table: {stripped_line}")

    if in_table_section and stripped_line:
        current_table.append(stripped_line.split())

    if in_table_section and not stripped_line:
        in_table_section = False

if current_table:
    df_table = pd.DataFrame(current_table)
    tables.append(df_table)
    print(f"Extracted table with shape: {df_table.shape}")

if tables:
    spaced_tables = [tables[0]]  # 第一个表格不需要空行
    for table in tables[1:]:
        empty_space = pd.DataFrame([[''] * table.shape[1]] * 2)
        spaced_tables.append(empty_space)
        spaced_tables.append(table)


    merged_table = pd.concat(spaced_tables, ignore_index=True)
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    merged_csv_path = os.path.join(desktop_path, 't5.csv')
    merged_table.to_csv(merged_csv_path, index=False, header=False)
    print(f"The tables were successfully extracted and merged into one CSV file：{merged_csv_path}")
else:
    print("No tables were found in the file.")
