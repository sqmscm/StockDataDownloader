# Stock Data Downloader for ECE 8903
![Update Stock Database](https://github.com/sqmscm/StockDataDownloader/workflows/Update%20Stock%20Database/badge.svg?branch=main&event=schedule)
## Setup
### 1. Prepare the database.
Create `stock` database in MS SQL Server and use the files in `sql` folder to initialize tables and data.
### 2. Add connection string and api key to secret.
Go to `Settings`-->`Secrets`-->`New secret`, create following secrets:

`CONNECTION_STRING`: SQL connection string

`API_KEY`: Alphavantage API key
### 3. Run workflow.
Go to `Actions`-->`Update Stock Database`-->`Run workflow`

The workflow will then be run at 05:00 UTC everyday.
