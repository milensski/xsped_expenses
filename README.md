# Xsped Expenses Reader

This application, built with Streamlit, aims to simplify the process of reading and analyzing expense data from XML and Excel files. It offers functionalities to process uploaded XML and Excel files containing expense information, perform data manipulation and filtering, and present the results in an organized manner.

## Features

- **File Upload**: Users can upload XML and Excel files containing expense data.
- **Data Processing**: The uploaded files are processed to extract relevant information.
- **Expense Analysis**: The application performs data manipulation and analysis, including merging datasets, filtering expenses, and aggregating data based on project and personnel.
- **Currency Selection**: Users can select the desired currency for displaying monetary values.

>[!WARNING]
>This application assumes a specific structure and format for the input files. Ensure that the XML and Excel files adhere to the expected schema for accurate processing and analysis.

## Dependencies

This application requires the following Python libraries:

- `xml.etree.ElementTree`
- `pandas`
- `streamlit`
