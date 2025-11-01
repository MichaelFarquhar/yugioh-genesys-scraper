The following is a spec for an AI assistant to create a new project.

Given the stack below, create a new python project using UV as the virtual environment. Python and uv are already installed on this pc.

## Stack

-   Python
-   UV
-   requests package
-   beautifulsoup package

## Project Spec

Code the following:

When this python script is ran, it will make a request to https://www.yugioh-card.com/en/genesys/, use beautifulsoup to scrap the data from the <table> on this site. The table has two colums, Card Name and Points. After this, it will create a genesys.json file in base directory with the scraped table data, where its an array of objects and each object is the corresponding table rows, with the properties of "card_name" and "points" in json respectively. Points should be an integer while card_name is string.

## Standards

-   Use Python best standards and practices
-   Use naming conventions best standards and practices and python
-   Ignore git I will do that myself
-   Use comments sparingly -- only when required to explain processes that need explaining.
-   use context7 MCP when help is needed
-   Ask any clarifying questions

### README

Create a README.md file with:

-   Title
-   Shields.io badge for python under the title and before the description
-   a brief description
-   instructions to install and test locally
-   license section
-   Disclaimer that this is not malicious scraping. Will be scraped about once a month whenever genesys points values are updated

### LICENSE

Add a MIT License file with my name Michael Farquhar
