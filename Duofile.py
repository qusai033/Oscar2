import pandas as pd

def load_and_clean_data(file_path):
    """
    Load and clean data from a CSV file.
    Extract the relevant section between 'Edited BP Data Record Count' and 'Edited Awake BP Data Record Count'.
    """
    # Read the CSV file
    data = pd.read_csv(file_path, header=None)

    # Locate the start and end of the relevant sections in the file
    start_index = data[data.iloc[:, 0].str.contains("Edited BP Data Record Count", na=False)].index[0] + 2
    end_index = data[data.iloc[:, 0].str.contains("Edited Awake BP Data Record Count", na=False)].index[0]

    # Extract the relevant data
    relevant_data = data.iloc[start_index:end_index].reset_index(drop=True)

    # Assign the first row as the header
    relevant_data.columns = relevant_data.iloc[0]
    relevant_data = relevant_data[1:]

    return relevant_data, data

def create_date_column(data):
    """
    Create a 'Date' column by combining 'Year', 'Month', 'Day', 'Hour', and 'Minute' columns.
    """
    data['Date'] = pd.to_datetime(data['Year'].astype(str) + '-' +
                                  data['Month'].astype(str) + '-' +
                                  data['Day'].astype(str) + ' ' +
                                  data['Hour'].astype(str) + ':' +
                                  data['Minute'].astype(str), errors='coerce')
    return data

def extract_patient_info(full_data, name_identifier, id_identifier):
    """
    Extract the 'Patient Name' and 'Patient ID' from the full dataset.
    """
    patient_name, patient_id = None, None

    # Iterate over the full dataset to find the patient information
    for index, row in full_data.iterrows():
        if row.str.contains(name_identifier, na=False).any():
            patient_name = name_identifier
        if row.str.contains(id_identifier, na=False).any():
            patient_id = id_identifier

    return patient_name, patient_id

def assign_patient_info(data, patient_name, patient_id):
    """
    Assign the 'Patient Name' and 'Patient ID' to each row in the data.
    """
    data['Patient Name'] = patient_name
    data['Patient ID'] = patient_id
    return data

def merge_and_sort_data(duo_data, qbp_data):
    """
    Merge Duo_BP and Q_BP data and sort by 'Date'.
    """
    # Concatenate the two datasets
    merged_data = pd.concat([duo_data, qbp_data], ignore_index=True)

    # Sort by the 'Date' column
    merged_data_sorted = merged_data.sort_values(by='Date')

    # Reset index
    merged_data_sorted = merged_data_sorted.reset_index(drop=True)

    return merged_data_sorted

def main():
    # Load and clean Duo_BP and Q_BP data using absolute paths
    duo_data_cleaned, duo_full_data = load_and_clean_data(r'C:\Users\duobao\Desktop\Sensorlab\oscar2 data\oscar data\Duo_BP.csv')
    qbp_data_cleaned, qbp_full_data = load_and_clean_data(r'C:\Users\duobao\Desktop\Sensorlab\oscar2 data\oscar data\Q_BP.csv')

    # Add 'Date' column to both datasets
    duo_data_cleaned = create_date_column(duo_data_cleaned)
    qbp_data_cleaned = create_date_column(qbp_data_cleaned)

    # Extract 'Patient Name' and 'Patient ID' from both datasets
    duo_name, duo_id = extract_patient_info(duo_full_data, 'Bao Duo', '168769')
    qbp_name, qbp_id = extract_patient_info(qbp_full_data, 'Almustafa Qusai', '168743')

    # Assign Patient Name and ID to the respective datasets
    duo_data_cleaned = assign_patient_info(duo_data_cleaned, duo_name, duo_id)
    qbp_data_cleaned = assign_patient_info(qbp_data_cleaned, qbp_name, qbp_id)

    # Merge and sort the data by the new 'Date' column
    merged_sorted_data = merge_and_sort_data(duo_data_cleaned, qbp_data_cleaned)

    # Remove the unnecessary columns ('Date', 'User Info Duo', 'User Info QBP')
    merged_sorted_data = merged_sorted_data.drop(columns=['Date', 'User Info Duo', 'User Info QBP'], errors='ignore')

    # Save the result to a new CSV file
    merged_sorted_data.to_csv(r'C:\Users\duobao\Desktop\Sensorlab\oscar2 data\oscar data\Merged_BP_Data.csv', index=False)
    print("Merged and sorted data saved to 'Merged_BP_Data.csv'.")

if __name__ == "__main__":
    main()
