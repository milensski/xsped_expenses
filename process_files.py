import xml.etree.ElementTree as ET

import pandas as pd

data = pd.read_excel('resources/persons.xlsx', sheet_name='Sheet')

df = pd.DataFrame(data, columns=['ID', 'First Name'])
df.reset_index()

database = {}

for index, row in df.iterrows():
    database[str(row['ID'])] = row['First Name']
    # print(f"{str(row['ID'])} : {row['First Name']}")
#
needed_info = ['LineSum', 'ProjectID', 'ProjectResponsiblePersonID']

tree = ET.parse('resources/20240018.xml')

with open('./resources/output.txt', 'a') as file:
    # file.write(f"Price Project Name\n")
    for elem in tree.iter():

        if elem.tag[56::] in needed_info:
            try:
                if elem.tag[56::] == 'ProjectResponsiblePersonID':
                    file.write(database[elem.text] + '\n')
                    print(database[elem.text])
                    print()

                elif elem.tag[56::] == 'LineSum':
                    file.write(f"{(float(elem.text)):.2f}")
                    print(f"{(float(elem.text)):.2f} ")

                else:
                    file.write(' ' + elem.text + ' ')
                    print(elem.text)
            except UnicodeError:
                print(f'skipping {elem.tag[56::]}')
                continue
            except KeyError:
                file.write('InvalidPerson' + '\n')
                print('InvalidPerson')
                print()

prices = []
projects = []
names = []
#
with open('./resources/output.txt', 'r+') as file:
    for line in file:
        try:
            price, project, *name = line.split()
            prices.append(price)
            projects.append(project)
            names.append(name[0])
        except ValueError:
            continue

print(prices)
print(projects)
print(names)

# Create a DataFrame with three columns
df2 = pd.DataFrame(
    {'Price': [f'{price}' for price in prices],
     'Project': [f'{project}' for project in projects],
     'Name': [f'{name}' for name in names]})

df2['Price'] = df2['Price'].astype(float)

grouped = df2.groupby(['Name', 'Project'])['Price'].sum().reset_index()

df2_sorted = grouped.sort_values('Name')

# Save the DataFrame to an Excel file
df2_sorted.to_excel('projects.xlsx', index=False)