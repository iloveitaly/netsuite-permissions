# Debugging NetSuite Permissions

Figuring out which NetSuite permissions you should include on a role for record access can be tricky. This repo provides simplified tables generated from various sources to make it easy to determine which permissions are required for data access.

## Looking up Permissions

### 1. NetSuite Record Catalog

[Lookup the table in this CSV](output/netsuite_record_catalog.csv) to find any required permissions.

Not all tables will have permissions specified. For instance `transactionAddressBook` is not indicated.

### 2. Tim's Documentation

[Tim Dietrich has a great site](https://timdietrich.me/blog/netsuite-suiteql-tables-permissions-reference/) which lists out tables and their permissions.

[You can find a simplified CSV here](output/tim_table.csv) with identical column names as the previous CSV

This seems to be pulled from the record catalog JSON but has slightly different content, so it could be customized, which
is why you should check here after checking the NetSuite-provided catalog.

### 3. Community Documented Permissions

Check out this CSV for [community-documented permissions](output/community_permissions.csv) which are not found in the above sources.

### 4. NetSuite Documentation

Some NetSuite permissions aren't in the above sources and you need to [manually search the NetSuite documentation](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N128815.html#NetSuite-Documentation-Overview) to find specific permissions that are required.

If you find a permission that is missing from the Community Documented Permissions, [please add it to the CSV and submit a PR!](output/community_permissions.csv)

For instance, the "Transaction History" requires some additional permissions which are not found anywhere else [but in this document](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_N555081.html#Granting-User-Access-to-Transaction-History).


## NetSuite Record Catalog API

Here's how to get a dump of all tables in the account:

```shell
http -v GET https://$NETSUITE_ACCOUNT.app.netsuite.com/app/recordscatalog/rcendpoint.nl action==getRecordTypes data=='{"structureType":"FLAT"}' "Cookie: $NETSUITE_COOKIE"
```

And structure for a specific table:

```shell
https://$NETSUITE_ACCOUNT.app.netsuite.com/app/recordscatalog/rcendpoint.nl action==getRecordTypeDetail data=='{"scriptId":"workflowActionScript","path":""}' "Cookie: $NETSUITE_COOKIE"
```
