import json
import subprocess
import argparse

#--------------------------------------------------------
# ListView Utility
# prepares a destructiveChanges.xml file for ListView metadata for the given query
# author: mohan chinnappan
#--------------------------------------------------------


# Set up command line argument parsing
parser = argparse.ArgumentParser(description='SOQL query tool to fetch ListView metadata.')
parser.add_argument(
    '-q', '--query', 
    type=str, 
    default='SELECT Name, SObjectType, DeveloperName FROM ListView WHERE SObjectType != null', 
    help='The SOQL query to execute. Default is "SELECT Name, SObjectType, DeveloperName FROM ListView WHERE SObjectType != null".'
)

args = parser.parse_args()

# Run the SOQL query using the query provided or the default query
cmd = f'sfdx force:data:soql:query -q "{args.query}" --json'
result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

# Parse JSON output
try:
    data = json.loads(result.stdout)
    records = data["result"]["records"]
    print(f"✅ Found {len(records)} ListViews.")
except (json.JSONDecodeError, KeyError):
    print("❌ Error: Failed to parse SOQL query output.")
    exit(1)

# Check if we have records
if not records:
    print("❌ No records found.")
    exit(1)

# Debugging: print the entire raw JSON result
print("Raw JSON Result:", json.dumps(data, indent=4))

# Construct XML content
xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>\n'''

# Check each record and print out the Name and SObjectType for debugging
for record in records:
    listview_name = record.get("Name")
    object_name = record.get("SobjectType")  # Use correct case for SObjectType
    developer_name = record.get("DeveloperName")
    
    # Debugging output to check what we're getting
    print(f"Processing ListView: {listview_name}, SObjectType: {object_name}")
    
    # Only process if both listview_name and object_name exist
    if listview_name and object_name:
        xml_content += f'        <members>{object_name}.{developer_name}</members>\n'

# Add the ListView name tag
xml_content += '''        <name>ListView</name>
    </types>
    <version>60.0</version>
</Package>'''

# Write to destructiveChanges.xml
with open("destructiveChanges.xml", "w") as f:
    f.write(xml_content)

print("✅ destructiveChanges.xml generated successfully!")