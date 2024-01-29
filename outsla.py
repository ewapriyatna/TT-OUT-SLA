import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

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

            # Generate a unique key based on the operator and regional names
            button_key = f"copy_button_{operator.replace(' ', '_')}_{regional.replace(' ', '_')}"

            # Custom HTML button to copy to clipboard
            copy_button_html = f"""
                <button onclick="copyToClipboard('{button_key}')">Copy to Clipboard</button>
                <script>
                    function copyToClipboard(buttonKey) {{
                        var textToCopy = document.getElementById(buttonKey).innerText;
                        navigator.clipboard.writeText(textToCopy).then(function() {{
                            alert("Text copied to clipboard!");
                        }});
                    }}
                </script>
            """

            # Display the button
            components.html(copy_button_html)

            # Display the content with a unique ID
            st.markdown(f'<div id="{button_key}">{all_rows_text}</div>', unsafe_allow_html=True)

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
