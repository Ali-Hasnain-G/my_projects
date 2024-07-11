import os
import shutil
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to organize files

def organize_files(source_dir, target_dir):
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        if os.path.isfile(source_path):
            file_type = filename.split('.')[-1]
            target_folder = os.path.join(target_dir, file_type.upper())
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            shutil.move(source_path, os.path.join(target_folder, filename))
    print('File organization completed.')

# Function to send email

def send_email(subject, body, to_email):
    from_email = 'aliahc@gmail.com'  # Replace with your email address
    password = '112233'  # Replace with your email password

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Replace with your SMTP server details
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print('Email sent successfully.')
    except Exception as e:
        print(f'Failed to send email. Error: {str(e)}')

# Function to process CSV file

def process_csv(csv_file_path):
    try:
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f'File not found: {csv_file_path}')

        # Check if the file is empty or does not contain any data

        if os.path.getsize(csv_file_path) == 0:
            raise ValueError(f'CSV file is empty: {csv_file_path}')

        df = pd.read_csv(csv_file_path)

        # Check if the DataFrame is empty after reading

        if df.empty:
            raise ValueError(f'No data to parse from file: {csv_file_path}')

        # Process the CSV data as needed

        print('CSV file processed successfully.')
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as value_error:
        print(value_error)
    except pd.errors.EmptyDataError:
        print(f'No columns to parse from file: {csv_file_path}')
    except Exception as e:
        print(f'Failed to process CSV file. Error: {str(e)}')

# Main execution block

if __name__ == '__main__':

    # Example usage: replace these paths with actual paths in your environment

    csv_file_path = r"C:\Users\GM Computer\OneDrive\Documents\A.csv.csv"
    recipient_email = 'abc@gmail.com'

    # Process CSV file

    process_csv(csv_file_path)

    # Send email

    subject = 'CSV Processing Report'
    body = 'The CSV file processing task has completed.'
    send_email(subject, body, recipient_email)

    print('Task automation completed.')

# Function to process CSV data

def process_csv(csv_file):
    df = pd.read_csv(csv_file)

    # Example processing: multiply a column by 2

    df['Processed_Column'] = df['Original_Column'] * 2

    # Save processed data back to CSV

    df.to_csv('processed_data.csv', index=False)
    print('CSV data processed and saved.')

# Example usage

if __name__ == '__main__':

    # Replace with actual paths on your system

    source_directory = "C:\\data"
    target_directory = "C:\\data"


    # Perform file organization

    organize_files(source_directory, target_directory)

    # Perform email automation

    subject = 'Automated Email'
    body = 'Hello, this is an automated email.'
    recipient_email = 'abc@gmail.com'
    send_email(subject, body, recipient_email)

    # Perform data entry automation

    csv_file_path = r"C:\Users\GM Computer\OneDrive\Documents\A.csv.csv"

    process_csv(csv_file_path)

    print('All automation tasks completed.')
