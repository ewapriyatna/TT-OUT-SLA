import streamlit as st
import pandas as pd
import pyperclip
import streamlit.components.v1 as components
from datetime import datetime

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
        # Get unique regionals for the current operator
        unique_regionals = df[df['Operator'] == operator]['Regional'].unique()

        for regional in unique_regionals:
            # Filter data for the current operator and regional
            filtered_data = df[(df['Operator'] == operator) & (df['Regional'] == regional)]

            st.header(f"*TT OUT SLA OPERATOR {operator} - {regional} TANGGAL {current_date} {current_time}*")

            all_rows_text = ""

            for i, (_, row) in enumerate(filtered_data.iterrows(), start=1):
                all_rows_text += (
                    f"*{i}. ❌ -Nomer TT:* {row['TT Operator']}\n"
                    f"*-Titel:* {row['List Site']}\n"
                    f"*-Operator:* {row['Operator']}\n"
                    f"*-Mitra:* {row['Mitra']}\n"
                    f"*-Regional:* {row['Regional']}\n"
                    f"*-Durasi:* {row['Durasi with SC']}\n"
                    f"*Last Update:* {row['Update Progress']}\n"
                    "===================\n"
                )

            # Display numbers for each item
            numbered_list = "\n".join([f"**{i}.**" for i in range(1, len(filtered_data) + 1)])

            # Generate a unique key based on the operator and regional names
            button_key = f"copy_button_{operator.replace(' ', '_')}_{regional.replace(' ', '_')}"

            # Copy to Clipboard button outside the loop with a unique key
            if st.button("Copy to Clipboard", key=button_key):
                # Concatenate title, numbered list, and all rows text
                clipboard_text = (
                    f"TT OUT SLA OPERATOR {operator} - {regional} TANGGAL {current_date} {current_time}\n\n"
                    f"{all_rows_text}\n"
                )

                # Copy to clipboard
                pyperclip.copy(clipboard_text)
                st.success("Text copied to clipboard!")

def main():
    st.title("TT OUT SLA BASED ON OPERATOR & REGIONAL")

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
