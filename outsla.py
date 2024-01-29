import streamlit as st
import pandas as pd
import pyperclip  # To interact with the clipboard
from datetime import datetime  # For getting the current date and time

def load_data(file_path):
    try:
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path, engine='openpyxl')
        return df
    except Exception as e:
        st.error(f"Error loading the file: {e}")
        return None

def display_sections(df, current_date, current_time):
    unique_operators = df['Operator'].unique()

    for operator in unique_operators:
        st.header(f"TT OUT SLA OPERATOR {operator} TANGGAL {current_date} {current_time}")

        operator_data = df[df['Operator'] == operator]
        all_rows_text = ""

        for i, (_, row) in enumerate(operator_data.iterrows(), start=1):
            all_rows_text += (
                f"**{i}. ❌ -Nomer TT:** {row['TT Operator']}\n"
                f"**-Segmen:** {row['List Site']}\n"
                f"**-Operator:** {row['Operator']}\n"
                f"**-Mitra:** {row['Mitra']}\n"
                f"**-Regional:** {row['Regional']}\n"
                f"**-Durasi:** {row['Durasi with SC']}\n"
                f"**Last Update:** {row['Update Progress']}\n"
                "===================\n"
            )

        # Display numbers for each item
        numbered_list = "\n".join([f"**{i}.**" for i in range(1, len(operator_data) + 1)])

        # Generate a unique key based on the operator name
        button_key = f"copy_button_{operator.replace(' ', '_')}"

        # Copy to Clipboard button outside the loop with a unique key
        if st.button("Copy to Clipboard", key=button_key):
            # Concatenate title, numbered list, and all rows text
            clipboard_text = (
                f"TT OUT SLA OPERATOR {operator} TANGGAL {current_date} {current_time}\n\n"
                #f"{numbered_list}\n\n"
                f"{all_rows_text}\n"
                #"===================\n"
            )

            # Copy to clipboard
            pyperclip.copy(clipboard_text)
            st.success("Text copied to clipboard!")



def main():
    st.title("LIST OUT SLA")

    # Upload Excel file
    file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])
    
    if file is not None:
        # Load data from Excel
        df = load_data(file)

        if df is not None:
            
            # Assuming you have the current time in the format "HH:mm:ss"
            current_time = datetime.now().strftime("%H:%M:%S")
            # Get the current date
            current_date = datetime.now().strftime("%d/%m/%Y")

            # Display sections in the specified format
            display_sections(df, current_date, current_time)
            
            # Display all rows in the specified format
            # Commented out for now as it's not defined in your provided code
            # display_all_rows(df)

if __name__ == "__main__":
    main()
