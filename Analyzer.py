import csv
import os
import argparse
import re
import pandas as pd
import shutil

def create_new_csv(input_file, output_file):
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header row

        # Find the index of "ac_tap_triage_complete" column
        stop_index = headers.index("ac_tap_triage_complete")

        # Create the output file if it does not exist
        if not os.path.exists(output_file):
            open(output_file, 'w').close()

        # Write the data to the output file
        with open(output_file, 'w', newline='') as output:
            writer = csv.writer(output)
            writer.writerow(headers[:stop_index+1])

            # Write the rows up until the stop column
            for row in reader:
                writer.writerow(row[:stop_index+1])

    print(f"New CSV file '{output_file}' created successfully.")

def create_new_csv_with_range(input_file, output_file, start_column, end_column):
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header row

        # Find the indices of the start and end columns
        start_index = headers.index(start_column)
        end_index = headers.index(end_column)

        # Create the output file if it does not exist
        if not os.path.exists(output_file):
            open(output_file, 'w').close()

        # Write the data to the output file
        with open(output_file, 'w', newline='') as output:
            writer = csv.writer(output)

            # Write the selected column headers
            selected_headers = headers[start_index:end_index+1]
            writer.writerow(selected_headers)

            # Write the rows with selected column values
            for row in reader:
                selected_values = row[start_index:end_index+1]
                writer.writerow(selected_values)

    print(f"New CSV file '{output_file}' created successfully.")

def extract_first_column(input_file, output_file):
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header row

        # Extract the first column values
        first_column_values = [row[0] for row in reader]

    # Create the output file if it does not exist
    if not os.path.exists(output_file):
        open(output_file, 'w').close()

    # Write the first column values to the output file
    with open(output_file, 'w', newline='') as output:
        writer = csv.writer(output)
        writer.writerow([headers[0]])  # Write the first column header
        writer.writerows(zip(first_column_values))

    print(f"New CSV file '{output_file}' created successfully.")

def merge_csv_by_columns(file1, file2, output_file):
    with open(file1, 'r') as file1_obj, open(file2, 'r') as file2_obj:
        reader1 = csv.reader(file1_obj)
        reader2 = csv.reader(file2_obj)

        # Read the header rows from both files
        headers1 = next(reader1)
        headers2 = next(reader2)

        # Combine the headers from both files
        merged_headers = headers1 + headers2

        # Read the data rows from both files
        data1 = list(reader1)
        data2 = list(reader2)

        # Check if the number of rows is the same in both files
        if len(data1) != len(data2):
            print("Error: The number of rows in the files does not match.")
            return

    # Create the output file if it does not exist
    if not os.path.exists(output_file):
        open(output_file, 'w').close()

    # Merge the data by columns and write to the output file
    with open(output_file, 'w', newline='') as output:
        writer = csv.writer(output)
        
        # Write the merged headers
        writer.writerow(merged_headers)

        # Write the merged data row by row
        for row1, row2 in zip(data1, data2):
            merged_row = row1 + row2
            writer.writerow(merged_row)

    print(f"CSV files '{file1}' and '{file2}' merged successfully into '{output_file}'.")

    # Delete the input files
    os.remove(file1)
    os.remove(file2)

def extract_first_two_columns(input_file, output_file):
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header row

        # Extract the first two columns' values
        first_two_columns_values = [[row[0], row[1]] for row in reader]

    # Create the output file if it does not exist
    if not os.path.exists(output_file):
        open(output_file, 'w').close()

    # Write the first two columns' values to the output file
    with open(output_file, 'w', newline='') as output:
        writer = csv.writer(output)
        writer.writerow(headers[:2])  # Write the first two column headers
        writer.writerows(first_two_columns_values)

    print(f"New CSV file '{output_file}' created successfully.")

def move_csv_to_folder(csv_file_path, destination_folder):
    try:
        # Create the destination folder if it doesn't exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Extract the filename from the original path
        file_name = os.path.basename(csv_file_path)

        # Build the new destination path
        new_path = os.path.join(destination_folder, file_name)

        # Move the CSV file to the destination folder
        shutil.move(csv_file_path, new_path)

        print(f"CSV file '{file_name}' has been moved to '{destination_folder}'.")
    except FileNotFoundError:
        print(f"CSV file '{csv_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'csv_file_path' with the actual path of the CSV file you want to move.


# Replace 'destination_folder' with the actual path of the folder you want to move the CSV file into.


parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
parser.add_argument('filename')     
args = parser.parse_args()
csv_file_path = "Demographic_Final.csv"
destination_folder = "Final_Folder"
create_new_csv(args.filename, "Triage.csv")
create_new_csv_with_range(args.filename, "Patient.csv", "pt_mrn", "patient_demographics_complete")
extract_first_column(args.filename, "Record.csv")
merge_csv_by_columns("Record.csv","Patient.csv","Demographic_Final.csv")
create_new_csv_with_range(args.filename, "Patient.csv", "start_time", "ac_tap_form_5_complete")
extract_first_two_columns(args.filename, "Record.csv")
merge_csv_by_columns("Record.csv","Patient.csv","ACTaps.csv")
move_csv_to_folder(csv_file_path, destination_folder)

#######################################################################
# This part creates 6 different CSV files of the different tap values #
#######################################################################

def create_files(csv_file_path, header_name):
    filepaths = []  # Initialize a list to hold the filepaths of the created files
    with open(csv_file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames

        # Find the index of the desired header
        header_index = None
        for i, header in enumerate(headers):
            if header.lower() == header_name.lower():
                header_index = i
                break

        if header_index is None:
            print(f"Header '{header_name}' not found in the CSV file.")
            return

        # Create a folder to store the new files
        folder_name = os.path.splitext(csv_file_path)[0]
        os.makedirs(folder_name, exist_ok=True)

        # Initialize a dictionary to hold file writers
        file_writers = {}
        file_names = {}

        # Iterate through each row and append to the respective files
        for row in reader:
            value = row[headers[header_index]]

            # Skip rows that don't have a valid number
            if not value.isdigit() or int(value) < 0 or int(value) > 5:
                continue

            # Create new file if it doesn't exist in the dictionary
            if value not in file_writers:
                base_name = os.path.splitext(os.path.basename(csv_file_path))[0]
                filename = f"{base_name}_{value}.csv"
                file_path = os.path.join(folder_name, filename)
                file_writers[value] = open(file_path, 'a', newline='')

                # Write the headers to the new file
                writer = csv.writer(file_writers[value])
                writer.writerow(headers)

            # Append the row to the respective file
            writer = csv.writer(file_writers[value])
            writer.writerow(row.values())

        # Close all file writers and collect filepaths
        for value, writer in file_writers.items():
            writer.close()
            filepaths.append(os.path.join(folder_name, f"{base_name}_{value}.csv"))

    print(f"New files created in folder '{folder_name}'.")
    return filepaths

#########################################################
# Reformats the taps into a much shorter data structure #
#########################################################

def get_list_from_basename(filepath):
    # Extract the basename without extension
    basename = os.path.splitext(os.path.basename(filepath))[0]

    # Use regular expression to find the first number in the basename
    match = re.search(r'\d+', basename)

    if match:
        number = int(match.group())  # Convert the matched number to an integer
        if number > 0:
            upper_limit = min(number, 4)  # Set the upper limit to 5 or number + 2, whichever is smaller
            return list(range(2, upper_limit + 2))  # Return the list from 2 to the upper limit (inclusive)
        else:
            print("The extracted number is not greater than 0.")
            return []
    else:
        print("No number found in the basename.")
        return None
    

def reformat(filename, numlist):
    # Print the file name for which the CSV file will be read
    print(f"Reading the CSV file: {filename}")

    # Read the CSV file to be modified using pandas
    original_data = pd.read_csv(filename)

    # Define the column suffixes provided in the 'numlist'
    column_suffixes = numlist

    # Check if numlist is empty
    if not column_suffixes:
        print("Empty 'numlist'. Renaming the original file.")
        
        # Get the base file name without the extension
        base_filename, file_extension = os.path.splitext(filename)

        # Define the output CSV file name with "_reformat" added before the file extension
        output_file = f'{base_filename}_reformat{file_extension}'
        
        # Rename the original file to the output file name
        os.rename(filename, output_file)
        
        print(f"Original file renamed to: {output_file}")
        return output_file
    else:
        # Create an empty list to store the modified data frames
        merged_data_list = []
        
        # Append the original data to the list
        merged_data_list.append(original_data)

        # Iterate over the column suffixes
        for suffix in column_suffixes:
            # Print the current column suffix being processed
            print(f"\nProcessing column suffix {suffix}...")

            # Check if the required columns exist for the current suffix
            if f'ac_tap_form_{suffix}_complete' in original_data.columns and f'start_time_v{suffix}' in original_data.columns:
                # Create a copy of the original data for modification
                data = original_data.copy()

                # Find the index positions of the relevant headers
                start_time_index = data.columns.get_loc('start_time')
                ac_tap_form_1_complete_index = data.columns.get_loc('ac_tap_form_1_complete')
                start_time_v_index = data.columns.get_loc(f'start_time_v{suffix}')
                ac_tap_form_complete_index = data.columns.get_loc(f'ac_tap_form_{suffix}_complete')
                record_id_index = data.columns.get_loc('record_id')

                # Select the rows up to and including 'ac_tap_form_1_complete'
                data.iloc[:, start_time_index:ac_tap_form_1_complete_index + 1] = data.iloc[:, start_time_v_index:ac_tap_form_complete_index + 1].values

                # Replace values under 'record_id' by appending the suffix
                data['record_id'] = data['record_id'].astype(str) + f' (v{suffix})'

                # Append the modified data frame to the list
                merged_data_list.append(data)
            else:
                print(f"Required columns not found for suffix {suffix}. Skipping modifications.")

        if merged_data_list:
            # Concatenate the modified data frames into a single data frame
            merged_data = pd.concat(merged_data_list, ignore_index=True)

            # Remove headers and columns after 'ac_tap_form_1_complete'
            merged_data = merged_data.iloc[:, :ac_tap_form_1_complete_index + 1]

            # Get the base file name without the extension
            base_filename, file_extension = os.path.splitext(filename)

            # Define the output CSV file name with "_reformat" added before the file extension
            output_file = f'{base_filename}_reformat{file_extension}'

            # Write the merged data to the output file in CSV format, without index
            merged_data.to_csv(output_file, index=False)

            print("Merging, modifications, and column removal completed successfully.")

            # Delete the input file if 'numlist' is not empty
            os.remove(filename)
            print(f"Input file '{filename}' has been deleted.")
            
            return output_file
        else:
            print("No modifications were performed due to missing required columns.")
            return None

#######################################
# Merges all data structures together #
#######################################

def merge(file_paths):
    # List to store data frames
    dfs = []

    # Iterate through the file paths
    for file_path in file_paths:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            dfs.append(df)
            # Optionally, you can print the file name before deleting
            # print("Merging file:", file_path)
            os.remove(file_path)

    # Merge data frames
    merged_df = pd.concat(dfs, ignore_index=True)

    # Create the folder if it doesn't exist
    folder_path = "Final_Folder"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Write merged data frame to a new CSV file in the ACTaps folder
    merged_file_path = os.path.join(folder_path, 'ACTaps_FINAL.csv')
    merged_df.to_csv(merged_file_path, index=False)

    print("CSV files merged successfully, and input files moved to the ACTaps folder!")

def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents have been deleted.")
    except FileNotFoundError:
        print(f"Folder '{folder_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

#######################################################
# Initiates all the functions to process all the data #
#######################################################

#Usage:
csv_file_path = "ACTaps.csv"
header_name = 'act_totalnum'

# Initialize an empty list
results_list = []

filepaths = create_files(csv_file_path, header_name)
for i in filepaths:
    result = reformat(i, get_list_from_basename(i))
    results_list.append(result)
merge(results_list)
delete_folder("ACTaps")
delete_file("ACTaps.csv")

##############################################
# Reformats Data to be processed more easily #
##############################################

def move_column_after_header(csv_file, column_name, target_header):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Check if the target header exists in the DataFrame
    if target_header not in df.columns:
        print(f"Target header '{target_header}' not found in the CSV file.")
        return

    # Get the index of the target header
    target_index = df.columns.get_loc(target_header)

    # Check if the column to move exists in the DataFrame
    if column_name not in df.columns:
        print(f"Column '{column_name}' not found in the CSV file.")
        return

    # Get the index of the column to move
    column_index = df.columns.get_loc(column_name)

    # If the column to move is already after the target header, no need to do anything
    if column_index == target_index + 1:
        print(f"Column '{column_name}' is already after '{target_header}'.")
        return

    # Remove the column to move from the DataFrame
    column_to_move = df.pop(column_name)

    # Insert the column right after the target header
    df.insert(target_index + 1, column_name, column_to_move)

    # Save the modified DataFrame back to the CSV file
    df.to_csv(csv_file, index=False)
    print(f"Column '{column_name}' moved after '{target_header}' successfully.")

#######################################################################
# This part creates 6 different CSV files of the different tap values #
#######################################################################

def create_files(csv_file_path, header_name):
    filepaths = []  # Initialize a list to hold the filepaths of the created files
    with open(csv_file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames

        # Find the index of the desired header
        header_index = None
        for i, header in enumerate(headers):
            if header.lower() == header_name.lower():
                header_index = i
                break

        if header_index is None:
            print(f"Header '{header_name}' not found in the CSV file.")
            return

        # Create a folder to store the new files
        folder_name = os.path.splitext(csv_file_path)[0]
        os.makedirs(folder_name, exist_ok=True)

        # Initialize a dictionary to hold file writers
        file_writers = {}
        file_names = {}

        # Iterate through each row and append to the respective files
        for row in reader:
            value = row[headers[header_index]]

            # Skip rows that don't have a valid number
            if not value.isdigit() or int(value) < 0 or int(value) > 5:
                continue

            # Create new file if it doesn't exist in the dictionary
            if value not in file_writers:
                base_name = os.path.splitext(os.path.basename(csv_file_path))[0]
                filename = f"{base_name}_{value}.csv"
                file_path = os.path.join(folder_name, filename)
                file_writers[value] = open(file_path, 'a', newline='')

                # Write the headers to the new file
                writer = csv.writer(file_writers[value])
                writer.writerow(headers)

            # Append the row to the respective file
            writer = csv.writer(file_writers[value])
            writer.writerow(row.values())

        # Close all file writers and collect filepaths
        for value, writer in file_writers.items():
            writer.close()
            filepaths.append(os.path.join(folder_name, f"{base_name}_{value}.csv"))

    print(f"New files created in folder '{folder_name}'.")
    return filepaths

#########################################################
# Reformats the taps into a much shorter data structure #
#########################################################

def get_list_from_basename(filepath):
    # Extract the basename without extension
    basename = os.path.splitext(os.path.basename(filepath))[0]

    # Use regular expression to find the first number in the basename
    match = re.search(r'\d+', basename)

    if match:
        number = int(match.group())  # Convert the matched number to an integer
        if number > 0:
            upper_limit = min(number, 4)  # Set the upper limit to 5 or number + 2, whichever is smaller
            return list(range(2, upper_limit + 2))  # Return the list from 2 to the upper limit (inclusive)
        else:
            print("The extracted number is not greater than 0.")
            return []
    else:
        print("No number found in the basename.")
        return None
    

def reformat(filename, numlist):
    # Print the file name for which the CSV file will be read
    print(f"Reading the CSV file: {filename}")

    # Read the CSV file to be modified using pandas
    original_data = pd.read_csv(filename)

    # Define the column suffixes provided in the 'numlist'
    column_suffixes = numlist

    # Check if numlist is empty
    if not column_suffixes:
        print("Empty 'numlist'. Renaming the original file.")
        
        # Get the base file name without the extension
        base_filename, file_extension = os.path.splitext(filename)

        # Define the output CSV file name with "_reformat" added before the file extension
        output_file = f'{base_filename}_reformat{file_extension}'
        
        # Rename the original file to the output file name
        os.rename(filename, output_file)
        
        print(f"Original file renamed to: {output_file}")
        return output_file
    else:
        # Create an empty list to store the modified data frames
        merged_data_list = []
        
        # Append the original data to the list
        merged_data_list.append(original_data)

        # Iterate over the column suffixes
        for suffix in column_suffixes:
            # Print the current column suffix being processed
            print(f"\nProcessing column suffix {suffix}...")
        
            # Check if the required columns exist for the current suffix
            if f'actfu_datediff_{suffix}' in original_data.columns and f'actdate_yn_{suffix}' in original_data.columns:
                # Create a copy of the original data for modification
                data = original_data.copy()

                # Find the index positions of the relevant headers
                start_time_index = data.columns.get_loc('actdate_yn_1')
                ac_tap_form_1_complete_index = data.columns.get_loc('actfu_datediff_1')
                start_time_v_index = data.columns.get_loc(f'actdate_yn_{suffix}')
                ac_tap_form_complete_index = data.columns.get_loc(f'actfu_datediff_{suffix}')
                record_id_index = data.columns.get_loc('record_id')

                # Select the rows up to and including 'ac_tap_form_1_complete'
                data.iloc[:, start_time_index:ac_tap_form_1_complete_index + 1] = data.iloc[:, start_time_v_index:ac_tap_form_complete_index + 1].values

                # Replace values under 'record_id' by appending the suffix
                data['record_id'] = data['record_id'].astype(str) + f' (v{suffix})'

                # Append the modified data frame to the list
                merged_data_list.append(data)
            else:
                print(f"Required columns not found for suffix {suffix}. Skipping modifications.")

        if merged_data_list:
            # Concatenate the modified data frames into a single data frame
            merged_data = pd.concat(merged_data_list, ignore_index=True)

            # Remove headers and columns after 'ac_tap_form_1_complete'
            merged_data = merged_data.iloc[:, :ac_tap_form_1_complete_index + 1]

            # Get the base file name without the extension
            base_filename, file_extension = os.path.splitext(filename)

            # Define the output CSV file name with "_reformat" added before the file extension
            output_file = f'{base_filename}_reformat{file_extension}'

            # Write the merged data to the output file in CSV format, without index
            merged_data.to_csv(output_file, index=False)

            print("Merging, modifications, and column removal completed successfully.")

            # Delete the input file if 'numlist' is not empty
            os.remove(filename)
            print(f"Input file '{filename}' has been deleted.")
            
            return output_file
        else:
            print("No modifications were performed due to missing required columns.")
            return None

#######################################
# Merges all data structures together #
#######################################

def merge(file_paths):
    # List to store data frames
    dfs = []

    # Iterate through the file paths
    for file_path in file_paths:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            dfs.append(df)
            # Optionally, you can print the file name before deleting
            # print("Merging file:", file_path)
            os.remove(file_path)

    # Merge data frames
    merged_df = pd.concat(dfs, ignore_index=True)

    # Create the folder if it doesn't exist
    folder_path = "Final_Folder"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Write merged data frame to a new CSV file in the ACTaps folder
    merged_file_path = os.path.join(folder_path, 'Triage_FINAL.csv')
    merged_df.to_csv(merged_file_path, index=False)

    print("CSV files merged successfully, and input files moved to the ACTaps folder!")

def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents have been deleted.")
    except FileNotFoundError:
        print(f"Folder '{folder_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

#######################################################
# Initiates all the functions to process all the data #
#######################################################

#Usage:
csv_file_path = "Triage.csv"
header_name = 'act_totalnum'

# Lists of values for column_to_move and target_header
columns_to_move = ["actfu_datediff_1", "actfu_datediff_2", "actfu_datediff_3", "actfu_datediff_4", "actfu_datediff_5"]
target_headers = ["fu_date_1_yn", "fu_date_2_yn", "fu_date_3_yn", "fu_date_4_yn", "fu_date_5_yn"]

for column_to_move, target_header in zip(columns_to_move, target_headers):
    move_column_after_header(csv_file_path, column_to_move, target_header)

# Initialize an empty list
results_list = []

filepaths = create_files(csv_file_path, header_name)
for i in filepaths:
    result = reformat(i, get_list_from_basename(i))
    results_list.append(result)
merge(results_list)
delete_folder("Triage")
delete_file("Triage.csv")
