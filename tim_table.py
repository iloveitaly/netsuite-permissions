from lxml import etree
import requests
import pandas as pd
import json

url = "https://timdietrich.me/blog/netsuite-suiteql-tables-permissions-reference/"
html_content = requests.get(url).content
parser = etree.HTMLParser()
tree = etree.fromstring(html_content, parser)

# Extracting the table using XPath
xpath_query = '//*[@id="permissionsTable"]'
table_element = tree.xpath(xpath_query)[0]

# Converting the HTML table element to a string
table_html = etree.tostring(table_element, method="html").decode()

# Parsing the table HTML to a DataFrame
df = pd.read_html(table_html, flavor="bs4")[0]

# Convert the DataFrame to a JSON structure and print it
json_struct = json.loads(df.to_json(orient="records"))
print(json.dumps(json_struct, indent=2))

# Save the DataFrame to a CSV file
csv_filename = "./permissions_table.csv"
df.to_csv(csv_filename, index=False)

# Output the path to the saved CSV file
csv_filename
