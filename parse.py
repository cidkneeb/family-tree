from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from gedcom.parser import Parser
import json

# Path to your `.ged` file
file_path = 'Dursey-McClain.ged'

# Initialize the parser
gedcom_parser = Parser()

# Parse the GEDCOM file
gedcom_parser.parse_file(file_path)

# Extract individuals and their relationships
individuals = {}
root_child_elements = gedcom_parser.get_root_child_elements()

print("Available individuals:")
for element in root_child_elements:
    if isinstance(element, IndividualElement):
        pointer = element.get_pointer()
        name = " ".join(element.get_name())
        individuals[pointer] = {
            'name': name,
            'pointer': pointer,
            'children': []
        }

print("\nExtracting family relationships:")

for element in root_child_elements:
    if isinstance(element, FamilyElement):
        family_id = element.get_pointer()
        husband = None
        wife = None
        children = []

        for child in element.get_child_elements():
            tag = child.get_tag()
            if tag == "HUSB":
                husband = child.get_value()
            elif tag == "WIFE":
                wife = child.get_value()
            elif tag == "CHIL":
                children.append(child.get_value())
        
        # Add children to their parents
        if husband and husband in individuals:
            individuals[husband]['children'].extend(children)
        if wife and wife in individuals:
            individuals[wife]['children'].extend(children)

# Save the individuals data to a JSON file
with open('individuals_data.json', 'w') as f:
    json.dump(individuals, f, indent=4)
