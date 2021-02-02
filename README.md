# Stock Data Downloader for ECE 8903
## Setup
### 1. Add SQL connection string to secret.
Go to `Settings`-->`Secrets`-->`New secret`, create a new secret named `CONNECTION_STRING` and paste the connection string in the value.
### 2. Run Workflow.
Go to `Actions`-->`Update Stock Database`-->`Run workflow`

The workflow will then be run at 05:00 UTC everyday.
