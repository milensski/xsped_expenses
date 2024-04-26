import io
import xml.etree.ElementTree as ET

import pandas as pd
import streamlit as st


def process_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    data = {'ID': [], 'LineSum': [], 'Project ID': []}

    for line in root.iter():
        line_name = line.tag.split('}')[1]
        line_text = line.text
        if line_name == 'ProjectResponsiblePersonID':
            data['ID'].append(int(line_text))
        elif line_name == 'LineSum':
            data['LineSum'].append(line_text)
        elif line_name == 'ProjectID':
            data['Project ID'].append(int(line_text))

    return data


def process_excel_file(excel_file):
    excel_data = pd.read_excel(excel_file, sheet_name='Sheet')

    if 'ID' in excel_data.columns:
        excel_data['ID'] = excel_data['ID'].map(lambda x: int(x))

    elif 'Project ID' in excel_data.columns:
        excel_data['Project ID'] = excel_data['Project ID'].map(lambda x: int(x))
        return excel_data[['Project ID', 'Difference']]

    return excel_data


def filter_estimated_project(df: pd.DataFrame):
    df['Project ID'] = df['Project ID'].astype(str)
    filtered_df = df[df['Difference'] > 200].copy()
    filtered_df['Difference'] = filtered_df['Difference'].map(lambda x: f'{x:.2f} SEK')

    return filtered_df.loc[:, filtered_df.columns != 'ID']


def main():
    st.title("Xsped Expenses Reader")

    buffer = io.BytesIO

    # File upload widgets for persons data and XML file
    persons_file = st.file_uploader("Upload Persons Data (Excel)", type=["xlsx"])
    xml_file = st.file_uploader("Upload XML File", type=["xml"])
    estimations_file = st.file_uploader("Upload Estimations File", type=["xlsx"])
    currency = st.selectbox('Select Currency', ("SEK", "EUR", "NOK", "DKK"))

    if st.button("Process Files"):
        with st.status("Processing Files", expanded=True):
            if persons_file and xml_file:
                # Read persons data from Excel file

                persons_data = process_excel_file(persons_file)
                data = process_xml(xml_file)
                estimations = process_excel_file(estimations_file)

                df = pd.DataFrame(data)

                merged_df = pd.merge(df, persons_data, on='ID', how='inner')

                merged_df['LineSum'] = merged_df['LineSum'].astype(float)

                grouped = merged_df.groupby(['First Name', 'Project ID']).sum().reset_index()

                df_sorted = grouped.sort_values('First Name')

                df_sorted['LineSum'] = df_sorted['LineSum'].map(lambda x: f'{x:.2f} {currency}')

                merge_est = pd.merge(df_sorted, estimations, on='Project ID', how='inner')

                filtered_est = filter_estimated_project(merge_est)

                st.dataframe(filtered_est, width=700, height=700, hide_index=True)

                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    # Write each dataframe to a different worksheet.
                    filtered_est.to_excel(writer, sheet_name=f'Sheet 1')
                    writer.close()
                    st.download_button(
                        label="Download Excel worksheets",
                        data=buffer,
                        file_name="not_estimated.xlsx",
                        mime="application/vnd.ms-excel"
                    )


if __name__ == "__main__":
    main()
