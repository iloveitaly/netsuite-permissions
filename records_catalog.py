import json
import os
import sys

import requests


def get_netsuite_detail(netsuite_table_id):
    """
    example record data structure:

       {'data': {'availabilityDetails': ['Available'],
             'children': [],
             'featureNames': ['ACCOUNTING'],
             'features': ['Accounting'],
             'fields': [{'availabilityDetails': ['Available'],
                         'children': [],
                         'dataType': 'STRING',
                         'featureNames': [],
                         'features': [],
                         'fieldType': 'TEXT',
                         'flags': [],
                         'id': 'descr',
                         'isAvailable': True,
                         'isColumn': True,
                         'label': 'Description',
                         'permissionCodes': [],
                         'permissions': [],
                         'removed': False,
                         'type': 'RECORD_FIELD'},
                        {'availabilityDetails': ['Available'],
                         'children': [],
                         'dataType': 'BOOLEAN',
                         'featureNames': [],
                         'features': [],
                         'fieldType': 'CHECKBOX',
                         'flags': [],
                         'id': 'isInactive',
                         'isAvailable': True,
                         'isColumn': True,
                         'label': 'Inactive',
                         'permissionCodes': [],
                         'permissions': [],
                         'removed': False,
                         'type': 'RECORD_FIELD'},
                        {'availabilityDetails': ['Available'],
                         'children': [],
                         'dataType': 'INTEGER',
                         'featureNames': [],
                         'features': [],
                         'fieldType': 'INTEGER',
                         'flags': [],
                         'id': 'id',
                         'isAvailable': True,
                         'isColumn': True,
                         'label': 'Internal ID',
                         'permissionCodes': [],
                         'permissions': [],
                         'removed': False,
                         'type': 'RECORD_FIELD'},
                        {'availabilityDetails': ['Available'],
                         'children': [],
                         'dataType': 'STRING',
                         'featureNames': [],
                         'features': [],
                         'fieldType': 'TEXT',
                         'flags': [],
                         'flh': '<p>Enter the name for this record. This name '
                                'appears in lists that include this '
                                'record.<br></p>',
                         'id': 'name',
                         'isAvailable': True,
                         'isColumn': True,
                         'label': 'Name',
                         'permissionCodes': [],
                         'permissions': [],
                         'removed': False,
                         'type': 'RECORD_FIELD'},
                        {'availabilityDetails': ['Available'],
                         'children': [],
                         'dataType': 'FLOAT',
                         'featureNames': [],
                         'features': [],
                         'fieldType': 'FLOAT',
                         'flags': [],
                         'flh': '<p>Amounts for this category are not reported on '
                                '1099-MISC forms until they exceed this amount '
                                'per vendor.</p>',
                         'id': 'threshold',
                         'isAvailable': True,
                         'isColumn': True,
                         'label': 'Threshold',
                         'permissionCodes': [],
                         'permissions': [],
                         'removed': False,
                         'type': 'RECORD_FIELD'}],
             'flags': [],
             'id': 'category1099misc',
             'isAvailable': True,
             'joins': [],
             'label': '1099-MISC Category',
             'permissionCodes': ['LIST_ACCOUNT'],
             'permissions': ['Accounts'],
             'recordClass': 'RECORD',
             'scriptIdPath': [{'recordType': 'category1099misc'}],
             'subrecords': [],
             'type': 'RECORD_TYPE'},
    'status': 'ok',
    'type': 'response'}
    """

    netsuite_account = os.environ["NETSUITE_ACCOUNT"]
    netsuite_cookie = os.environ["NETSUITE_COOKIE"]

    url = (
        f"https://{netsuite_account}.app.netsuite.com/app/recordscatalog/rcendpoint.nl"
    )
    params = {
        "action": "getRecordTypeDetail",
        "data": json.dumps({"scriptId": netsuite_table_id, "path": ""}),
        # "_": "1710452463368",
    }

    print(f"GET {netsuite_table_id}", file=sys.stderr)

    response = requests.get(url, params=params, headers={"Cookie": netsuite_cookie})
    response.raise_for_status()

    return response.json()["data"]


catalog_path = sys.argv[1]
with open(catalog_path, "r") as f:
    catalog_data = json.load(f)

result = []


for row in catalog_data:
    # ex row: {"id":"category1099misc","label":"1099-MISC Category"}

    id = row["id"]
    label = row["label"]
    detail = get_netsuite_detail(id)

    result.append(
        {
            "id": id,
            "label": label,
            "detail": detail,
        }
    )

print(json.dumps(result, indent=2))
