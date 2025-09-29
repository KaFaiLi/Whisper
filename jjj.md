import camelot
import pandas as pd
import os
import sys

def extract_tables_to_excel(pdf_path, output_folder):
    """
    Extracts all tables from a given PDF file and saves each table as a separate Excel file.

    This function uses the 'lattice' flavor of Camelot, which is optimized for tables
    with clear, visible grid lines.

    Args:
        pdf_path (str): The full path to the source PDF file.
        output_folder (str): The path to the folder where Excel files will be saved.
    """
    print(f"--- Starting Table Extraction from: {os.path.basename(pdf_path)} ---")

    # --- 1. Input Validation and Setup ---
    # Check if the PDF file exists
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' was not found.")
        sys.exit(1) # Exit the script if the file doesn't exist

    # Check if the output folder exists, if not, create it
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Created output directory: {output_folder}")
    except OSError as e:
        print(f"Error creating directory {output_folder}. Reason: {e}")
        sys.exit(1)

    # --- 2. Core Table Extraction ---
    try:
        # Use flavor='lattice' for tables with defined lines.
        # For tables separated by whitespace, you might try flavor='stream'.
        print("Reading PDF... (This may take a moment for large files)")
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
        
    except Exception as e:
        print(f"An unexpected error occurred while reading the PDF: {e}")
        sys.exit(1)

    # --- 3. Processing and Saving Results ---
    if tables.n == 0:
        print("No tables were found in the PDF using the 'lattice' method.")
        return

    print(f"Success! Found {tables.n} table(s) in the document.")

    # Iterate through all the found tables and save them
    for i, table in enumerate(tables):
        # The table object has a pandas DataFrame representation
        df = table.df

        # Clean up column headers that might span multiple lines
        # This joins multiline headers with a space. E.g., "Service\nDescription" -> "Service Description"
        df.columns = [' '.join(col).strip() for col in df.columns.to_flat_index()]

        # Define the output filename
        excel_filename = f"page_{table.page}_table_{i + 1}.xlsx"
        output_path = os.path.join(output_folder, excel_filename)

        try:
            # Save the DataFrame to an Excel file, without the pandas index
            df.to_excel(output_path, index=False)
            print(f"-> Saved: '{excel_filename}' (Shape: {df.shape})")
            
            # You can also print a parsing report for debugging
            # print(table.parsing_report)

        except Exception as e:
            print(f"Error saving table to {output_path}. Reason: {e}")

    print(f"--- Extraction Complete. All files saved in '{output_folder}' ---")


if __name__ == "__main__":
    # --- Configuration ---
    # IMPORTANT: Replace this with the path to YOUR PDF file.
    # On Windows, your path might look like: r"C:\Users\YourUser\Documents\report.pdf"
    # On macOS/Linux: "/home/youruser/documents/report.pdf"
    input_pdf_path = "your_document.pdf" 
    
    # Define where the output Excel files will be stored.
    # This will create a folder named 'extracted_tables' in the same directory as the script.
    output_directory = "extracted_tables"

    # --- Run the extractor function ---
    extract_tables_to_excel(input_pdf_path, output_directory)

