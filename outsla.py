import streamlit as st
import pandas as pd
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

            st.header(f"TT OUT SLA OPERATOR {operator} - {regional} TANGGAL {current_date} {current_time}")

            all_rows_text = ""

            for i, (_, row) in enumerate(filtered_data.iterrows(), start=1):
                all_rows_text += (
                    f"**{i}. ❌ -Nomer TT:** {row['TT Operator']}\n"
                    f"**-Titel:** {row['List Site']}\n"
                    f"**-Operator:** {row['Operator']}\n"
                    f"**-Mitra:** {row['Mitra']}\n"
                    f"**-Regional:** {row['Regional']}\n"
                    f"**-Durasi:** {row['Durasi with SC']}\n"
                    f"**Last Update:** {row['Update Progress']}\n"
                    "===================\n"
                )

            # Display numbers for each item
            numbered_list = "\n".join([f"**{i}.**" for i in range(1, len(filtered_data) + 1)])

            # Display the content with a unique ID
            st.markdown(f'<div id="{operator}_{regional}">{all_rows_text}</div>', unsafe_allow_html=True)

            # Copy to Clipboard button
            copy_button_key = f"copy_button_{operator.replace(' ', '_')}_{regional.replace(' ', '_')}"
            if st.button("Copy to Clipboard", key=copy_button_key):
                # Get the content to copy using the unique ID
                content_to_copy = st.markdown(f'<div id="{operator}_{regional}">{all_rows_text}</div>', unsafe_allow_html=True)
                
                # Copy to clipboard
                st.session_state[copy_button_key] = content_to_copy.markdown
                st.success("Text copied to clipboard!")

def main():
    st.title("Excel Data Display")

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

            # Filter by regional
            selected_regional = st.selectbox("Select Regional:", ['All'] + df['Regional'].unique())
            if selected_regional != 'All':
                display_sections(df, current_date, current_time)
            else:
                # Display sections in the specified format
                display_sections(df, current_date, current_time)

if __name__ == "__main__":
    main()
