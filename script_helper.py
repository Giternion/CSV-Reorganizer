import csv
import os
import time

charlist = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
new_col = []
new_row = []
outfile = "output.csv"

def qwarn():  # Prints warning and notes to user
    print("WARNING: This script can only work from columns A-Z, it will be confused if you enter, for example, AA")
    time.sleep(1)
    print("WARNING: CSV should only contain products to be imported. Remove rows used only for organizational purposes, like a row named 'Laptops'")
    time.sleep(1)
    print("WARNING: The names of headers must remain, otherwise the whole column will be assumed unimportant and removed.")
    time.sleep(1)
    while True:
        tutorial = input("Do you know how to use this Script: Y/N?: ")
        if tutorial in ['n', 'N']:
            print("This script ought to be in a folder, with only two other files. These two files should be the .bat file (this is used to run on Windows devices) and the CSV you want to reorganize (This should be renamed input.csv)")
            time.sleep(5)
            print("You will need to also have the Excel version of the file open. Because this script will ask you in which column to find certain information")
            time.sleep(5)
            print("If you don't have info for a column, because it's empty for example, or you want to exclude data, just hit enter. That column will then be removed in the CSV")
            break
        elif tutorial in ['y', 'Y']:
            print("If you say so")
            break
        else: 
            print("Not an accepted response")
    time.sleep(1)
    print("Good Luck!")

# This will convert letters to their corresponding number value, because a human will likely be looking at a spreadsheet.
# It should: Ask for input > Check input is of a valid type > Return input as number if good.
# Drop the column if the user enters nothing
def ltrnumbr(column):
    while True:
        ltr = input(f"Where should the column '{column}' be moved to? (Enter a single capital letter or press Enter to drop): ")
        if ltr == "":
            return None  # Drop the column
        elif ltr in charlist:
            return charlist.index(ltr)
        else:
            print("This is not a valid character. Please enter a single capital letter.")

# This will create the new file, with the appropriate columns
# It should open the file > iterate through each row in the old file > create a new row, with the order of the elements coming from new_col > write the row to the new file 
def reorganizer():
    print("Reorganizing")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'input.csv')
    
    if not os.path.isfile(input_file):
        print(f"File 'input.csv' not found in the directory '{script_dir}'.")
        return

    with open(input_file, newline='', encoding='utf8', errors='ignore') as f:  # open file to use
        reader = csv.reader(f)
        headers = next(reader)  # read the header row
        filtered_headers = [header for header in headers if header.strip()]  # filter out empty headers
        print(f"Headers found: {filtered_headers}")
        
        # Ask user where each column should be reorganized to
        for header in headers:
            if header.strip():  # Only prompt if header is not empty
                new_col.append(ltrnumbr(header))
            else:
                new_col.append(None)  # Drop column if header is empty
        
        for row in reader:  # this will iterate through rows
            temp = []
            for i in new_col:  # this will take values from row, and write them to temp in the order specified by new_col
                if i is not None:
                    temp.append(row[i])
            new_row.append(temp)

    with open(outfile, 'w', newline='') as file:
        writer = csv.writer(file)
        # Filter headers to exclude dropped columns
        new_headers = [headers[i] for i in range(len(headers)) if new_col[i] is not None]
        writer.writerow(new_headers)  # write filtered headers to the new file
        writer.writerows(new_row)
    print("Reorganization complete.")

qwarn()
reorganizer()
print("DONE! Check output.csv")
time.sleep(40)
