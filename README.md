# Yahoo_Auctions_Scrapper
Yahoo_Auctions_Scrapper is a tool that allows for the scraping of all yahoo auction pages of a given search term. Also has a variety of stored procedures, functions, and querries to manage the database. All quarries are written in Postgre syntax. 

Code for the Scrapy/SqlAlchemy to postgres pipeline is located in the "Yahoo_to_SQL/card_scraper" folder.
 - To connect to local database, must configure variables located in the models.py file in a .env file to create connection string
 - To begin scraping, only need to run the Yahoo_to_SQL.py file. Configre start url to scrape from here.
 - Unfinished folder contains a spider for use with a proxy that is not yet finished.

The Models folder contains sql quarries that have been refactored to function with dbt and Snowflake. Still a work in progress

Loose sql files in main folder are SQL quarries that have not yet been refactored for dbt, and only are for use in a local Postgres db. 

Priorities for the project:
- Refactor all code to work with dbt and Snowflake
- Include airflow DAGs to schedule when the pipeline runs, and prep the staging table to insert into the production table. 
- Dockerize code so that it can easily be set up. 
