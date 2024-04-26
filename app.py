import xml.etree.ElementTree as ET

import pandas as pd
import streamlit as st


def process_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    data = {'ID': [], 'LineSum': [], 'ProjectID': []}

    for line in root.iter():
        line_name = line.tag.split('}')[1]
        line_text = line.text
        if line_name == 'ProjectResponsiblePersonID':
            data['ID'].append(int(line_text))
        elif line_name == 'LineSum':
            data['LineSum'].append(line_text)
        elif line_name == 'ProjectID':
            data['ProjectID'].append(line_text)

    return data


def process_excel_file(persons_file):
    persons_data = pd.read_excel(persons_file, sheet_name='Sheet')
    persons_data['ID'] = persons_data['ID'].map(lambda x: int(x))

    return persons_data


def main():
    st.title("Xsped Expenses Reader")

    # File upload widgets for persons data and XML file
    persons_file = st.file_uploader("Upload Persons Data (Excel)", type=["xlsx"])
    xml_file = st.file_uploader("Upload XML File", type=["xml"])
    currency = st.selectbox('Select Currency', ("SEK", "EUR", "NOK", "DKK"))

    if st.button("Process Files"):
        with st.status("Processing Files", expanded=True):
            if persons_file and xml_file:
                # Read persons data from Excel file

                persons_data = process_excel_file(persons_file)

                data = process_xml(xml_file)

                df = pd.DataFrame(data)

                merged_df = pd.merge(df, persons_data, on='ID', how='inner')

                merged_df['LineSum'] = merged_df['LineSum'].astype(float)

                grouped = merged_df.groupby(['First Name', 'ProjectID']).sum().reset_index()

                df_sorted = grouped.sort_values('First Name')

                df_sorted['LineSum'] = df_sorted['LineSum'].map(lambda x: f'{x:.2f} {currency}')

                st.dataframe(df_sorted.loc[:, df_sorted.columns != 'ID'], width=700, height=700, hide_index=True)  #


if __name__ == "__main__":
    main()
