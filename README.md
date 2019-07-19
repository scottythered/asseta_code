# asseta_code

A repository of various code work during my time of employment at Asseta.com

## Contents

**manufacturer_API_example**: Manufacturer names from thousands of existing and archvied equipment listings were condensed into a thesaurus in Airtable. From this thesaurus, a local API was built with Flask_Restless and hosted on PythonAnywhere.com. This API is used during the cleaning of every new updated inventory list for all Asseta accounts, automatically catching known variant versions of manufacturer names and using fuzzy matching on unknown names. Aso includes a copy of the API script running on PythonAnywhere.com.

**thesaurus_update**: Library of functions related to updating the Manufacturer API. The library uses the Airtable API to convert the strucutred table containing the thesaurus into a large JSON object which the Manufacturer API uses for matching and searching.

**simplified_postgres**: Probably a misnomer, as it doesn't *really* simplify Postgres; in the process of updating account inventories, I found myself using a variation of 3 Postgres queries via the psycopg2 library for 75 percent of all of my database queries. simplified_postgres condenses these queries into a library that Ican call to save time.

**weekly_account_reminder**: An automated script that checks for accounts whose inventories haven't been updated in more than 90 days. If any unchecked accounts are found, the script sends an email via the Mailgun API.

**weekly_stats_chart**: Basic stats on the number of individual equipment listings added, removed, updated, or put on hold per week are tracked in a Google Docs spreadsheet. This script queries the Google Sheet and uses the Chartify library to present a bar graph representing the past 4 weeks of equipment listings.
