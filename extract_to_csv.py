import os
import json
import csv
import PyPDF2
from pathlib import Path
import pandas as pd

def extract_pdf_text(pdf_path):
    """Extract text content from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = []
            for page in pdf_reader.pages:
                text_content.append(page.extract_text())
            return '\n'.join(text_content)
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_json_content(json_path):
    """Extract content from JSON file"""
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Convert JSON to readable string format
            content = json.dumps(data, indent=2, ensure_ascii=False)
            return content
    except Exception as e:
        return f"Error reading JSON: {str(e)}"

def process_all_files():
    """Process all files in all folders and create CSV"""
    
    # Define the 7 ticket type folders
    folders = [
        "Hardware_Issue",
        "Software_Issue",
        "Network_Problem",
        "Password_Reset",
        "Access_Request",
        "System_Error",
        "Security_Incident"
    ]
    
    # Get base path (parent of the script, which contains the folders)
    base_path = Path(__file__).parent
    
    # Lists to store data
    x = []  # Content
    y = []  # Folder names
    file_types = []  # File type (JSON or PDF)
    file_names = []  # File names
    
    print("Processing files...")
    
    # Process each folder
    for folder in folders:
        folder_path = base_path / folder
        if not folder_path.exists():
            print(f"Warning: Folder {folder_path} not found, skipping...")
            continue
        
        print(f"\nProcessing folder: {folder}")
        
        # Get all files in the folder
        files = sorted(os.listdir(str(folder_path)))
        
        for file in files:
            file_path = folder_path / file
            
            if file.endswith('.json'):
                content = extract_json_content(str(file_path))
                file_type = "JSON"
            elif file.endswith('.pdf'):
                content = extract_pdf_text(str(file_path))
                file_type = "PDF"
            else:
                continue  # Skip non-JSON/PDF files
            
            # Store data
            y.append(folder)  # Folder name
            x.append(content)  # File content
            file_types.append(file_type)
            file_names.append(file)
            
            print(f"  Processed: {file} ({file_type})")
    
    # Create CSV file
    csv_filename = "it_tickets_dataset.csv"
    print(f"\n\nCreating CSV file: {csv_filename}")
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Folder_Name', 'File_Name', 'File_Type', 'Content'])
        
        # Write data rows
        for i in range(len(x)):
            writer.writerow([y[i], file_names[i], file_types[i], x[i]])
            
         # Adding a description column to the CSV
    df = pd.read_csv(csv_filename)
    def extract_description(content):
        try:
            return json.loads(content).get('description', '') if isinstance(content, str) and content.strip() else ''
        except json.JSONDecodeError:
            return ''
    df['Description'] = df['Content'].apply(extract_description)
    df.to_csv(csv_filename, index=False)

    
    print(f"\n{'='*60}")
    print(f"CSV file created successfully!")
    print(f"{'='*60}")
    print(f"\nSummary:")
    print(f"  Total files processed: {len(x)}")
    print(f"  Folders processed: {len(set(y))}")
    print(f"  JSON files: {file_types.count('JSON')}")
    print(f"  PDF files: {file_types.count('PDF')}")
    print(f"\nCSV saved as: {csv_filename}")
    
    return x, y

if __name__ == "__main__":
    x, y = process_all_files()
    print(f"\nVariables created:")
    print(f"  x (content): {len(x)} items")
    print(f"  y (folder names): {len(y)} items")