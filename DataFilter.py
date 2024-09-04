import pandas as pd

columns_to_extract = ['Patient Name', 'Patient ID', 'Index', 'Reason', 'Sys', 'Dia', 'HR', 'Mean', 'Hour', 'Minute', 'Month', 'Day', 'Year', 'Tag', 'Comments']

def extract_patient_info_from_footer(asc_data):
    patient_name = None
    patient_id = None

    # Looking for the line containing "Patient Name" and "Patient ID"
    for i, line in enumerate(asc_data):
        if "Patient Name" in line and "Patient ID" in line:
            # The next line contains the actual patient data
            patient_info_line = asc_data[i + 1].split()  # Split by whitespace or tabs
            patient_name = patient_info_line[0] + " " + patient_info_line[1]  # Extracting Patient Name (First + Last)
            patient_id = patient_info_line[2]  # Extracting Patient ID
            break
    return patient_name, patient_id

def process_asc_file_with_all_indices(asc_data):
    processed_data = []
    headers_found = False
    seen_indices = set()
    last_index = 0  

    patient_name, patient_id = extract_patient_info_from_footer(asc_data)
    for line in asc_data:
        if headers_found:
            line_data = line.strip().split('\t')
            if len(line_data) >= 23 and line_data[0].isdigit():  # Ensure the index is numeric
                index = int(line_data[0])
                # Fill missing indices between the last index and the current one
                for missing_index in range(last_index + 1, index):
                    processed_data.append({
                        'Index': str(missing_index),
                        'Reason': '--',
                        'Sys': '--',
                        'Dia': '--',
                        'HR': '--',
                        'Mean': '--',
                        'Hour': '--',
                        'Minute': '--',
                        'Month': '--',
                        'Day': '--',
                        'Year': '--',
                        'Tag': '--',
                        'Comments': '--',
                        'Patient Name': patient_name,
                        'Patient ID': patient_id
                    })
                seen_indices.add(index)
                processed_data.append({
                    'Patient Name': patient_name,
                    'Patient ID': patient_id,
                    'Index': line_data[0],
                    'Reason': line_data[1],
                    'Sys': line_data[2],
                    'Dia': line_data[3],
                    'HR': line_data[4],
                    'Mean': line_data[5],
                    'Hour': line_data[14],
                    'Minute': line_data[15],
                    'Month': line_data[16],
                    'Day': line_data[17],
                    'Year': line_data[18],
                    'Tag': line_data[22],
                    'Comments': line_data[23] if len(line_data) > 23 else ''
                })
                last_index = index
        elif line.startswith('Index'):
            headers_found = True
    return pd.DataFrame(processed_data, columns=columns_to_extract)

asc_file_path = 'DuoResults2.asc'
with open(asc_file_path, 'r') as file:
    asc_data = file.readlines()

processed_data = process_asc_file_with_all_indices(asc_data)
# Select rows 0 to 30 and columns 0 to 15 
selected_data = processed_data.iloc[0:30, :]

selected_data.to_csv('processed_duo_results_with_patient_info5.csv', index=False)
print(selected_data)





