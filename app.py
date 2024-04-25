import xml.etree.ElementTree as ET

import pandas as pd
import streamlit as st


def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    return root


def main():
    st.title("Xsped Expenses Reader")

    # File upload widgets for persons data and XML file
    persons_file = st.file_uploader("Upload Persons Data (Excel)", type=["xlsx"])
    xml_file = st.file_uploader("Upload XML File", type=["xml"])

    if st.button("Process Files"):
        if persons_file and xml_file:
            # Read persons data from Excel file
            persons_data = pd.read_excel(persons_file, sheet_name='Sheet')
            persons_data['ID'] = persons_data['ID'].map('{}'.format)
            # Create a dictionary from persons data

            root = parse_xml(xml_file)

            data = {'ID': [], 'LineSum': [], 'ProjectID': []}

            for line in root.iter():
                line_name = line.tag.split('}')[1]
                line_text = line.text
                if line_name == 'ProjectResponsiblePersonID':
                    data['ID'].append(line_text)
                elif line_name == 'LineSum':
                    data['LineSum'].append(line_text)
                elif line_name == 'ProjectID':
                    data['ProjectID'].append(line_text)

            df = pd.DataFrame(data)

            merged_df = pd.merge(df, persons_data, on='ID', how='inner')

            merged_df['LineSum'] = merged_df['LineSum'].astype(float)
            grouped = merged_df.groupby(['First Name', 'ProjectID']).sum().reset_index()

            df_sorted = grouped.sort_values('First Name')

            st.dataframe(df_sorted.loc[:, df_sorted.columns != 'ID'], width=700)


if __name__ == "__main__":
    main()
