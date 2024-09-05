import pandas as pd
import xml.etree.ElementTree as ET

# Load the Excel file
file_path = './XML_test_flat.xlsx'

# Read the sheets
output_values_df = pd.read_excel(file_path, sheet_name='Output_Values')
output_xpath_df = pd.read_excel(file_path, sheet_name='Output_XML_Path')

# Function to add elements to XML tree based on XPath
def set_xml_value(root, xpath, value):
    path_parts = xpath.split('/')
    
    current = root
    for part in path_parts:
        if part.startswith('@'):  # If it's an attribute
            attr_name = part[1:]
            current.set(attr_name, str(value))  # Set attribute value
            return
        else:
            next_elem = current.find(part)
            if next_elem is None:
                next_elem = ET.SubElement(current, part)
            current = next_elem

    current.text = str(value)  # Set the element's text value

# Create the root element for the XML
root = ET.Element("Root")

# Loop through each row in the Output_Values DataFrame
for row_idx in range(len(output_values_df)):
    row_element = ET.SubElement(root, "Row", id=str(row_idx + 1))  # Create a new XML node for each row
    
    for col in output_values_df.columns:
        value = output_values_df[col][row_idx]
        xpath = output_xpath_df[col][row_idx]
        
        if pd.notna(xpath) and pd.notna(value):
            set_xml_value(row_element, xpath, value)

# Write the XML to a file
tree = ET.ElementTree(root)
output_file = 'Output.xml'
tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f'XML file {output_file} has been created.')
