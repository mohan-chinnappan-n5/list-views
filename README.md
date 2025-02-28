# ListView Utility Script

## Description

The ListView Utility script is a Python tool that prepares a `destructiveChanges.xml` file for ListView metadata. It allows you to run a SOQL query to fetch metadata for ListViews and then generates an XML file to be used in Salesforce metadata deployments.

### Author: 
Mohan Chinnappan

---

## Features

- Run a customizable SOQL query to fetch `ListView` metadata from Salesforce.
- Generate a `destructiveChanges.xml` file for the queried `ListView` metadata.
- Default query filters ListViews where `SObjectType` is not null.
- Generates a properly structured XML file with relevant metadata information for Salesforce deployments.

---

## Installation

To run this script, you need:

- Python 3.x installed on your machine.
- Salesforce CLI (`sfdx`) installed and configured.
- Proper Salesforce authentication set up for your environment.

---

## Usage

The script accepts a command-line argument `--query` (or `-q`) that allows you to specify a custom SOQL query. If no query is provided, the script will default to the following query:

```sql
SELECT Name, SObjectType, DeveloperName FROM ListView WHERE SObjectType != null
```

## Command syntax
```bash
python3 listview_util.py --query "<YOUR_SOQL_QUERY>"
```

-q, --query (optional): The SOQL query to run. If not provided, the script uses the default query.

### Example
	1.	Default Query:
```bash
python3 listview_util.py
```
	2.	Custom Query:

```bash
python3 listview_util.py --query "SELECT Name, SObjectType, DeveloperName FROM ListView WHERE SObjectType = 'Campaign'"

```
This runs the custom query and generates the XML file for ListViews where the SObjectType is ‘Campaign’.

## Script Workflow
-	1.	Command Line Arguments:
The script accepts a --query argument that allows you to provide your custom SOQL query. The default query fetches ListView metadata where SObjectType is not null.
-	2.	Running the Query:
The script uses Salesforce CLI (sfdx) to run the SOQL query and fetch results in JSON format.
-	3.	Parsing the Results:
The script processes the JSON result from the query and extracts the relevant information (Name, SObjectType, and DeveloperName) for each ListView.
-	4.	Generating XML:
The script constructs the XML file (destructiveChanges.xml) based on the metadata. It includes the necessary <members> and <name> tags for Salesforce deployments.
-	5.	Saving the XML File:
The XML content is written to a file named destructiveChanges.xml.


## Example Output

- For a successful run, the following output is printed in the terminal:
```
✅ Found 5 ListViews.
Raw JSON Result:
{
    "result": {
        "records": [
            {
                "Name": "Created by Me",
                "SObjectType": "Report",
                "DeveloperName": "Created_by_Me"
            },
            ...
        ]
    }
}
✅ destructiveChanges.xml generated successfully!
```

- And the destructiveChanges.xml file will look like this:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>Report.Created_by_Me</members>
        <members>Report.Private_Reports</members>
        ...
        <name>ListView</name>
    </types>
    <version>60.0</version>
</Package>

```
