# Mail to Github Issue
### Collect your issues via mail.
## How to?
1. Fill `config.json` with a `password`, your github oauth `client_id` and `client_secret`
2. Create folder `accounts`
3. Start webServer.py and browse to shown address, authorize with github, enter IMAP details and register it with your set password.
4. Create cron to run checkMail.py regularly
