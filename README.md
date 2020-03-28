# Mail to Github Issue
### Collect your issues via mail.
## How to? (docker)
1. `docker create  -v /root/mailtoissue:/mailtoissue/accounts --name mail2issue -d strifel/mailtoissue`
2. `cd /root/mailtoissue`
3. `echo '{"username":  "test@example.com", "password":  "me123", "server":  "example.com", "delete":  1, "ssl":  true, "gh_repo": "strifel/mailToIssue", "gh_token": "1234"}' > account.json`
4. Edit account.json (you can rename the file as you wish)
5. Run `docker start mail2issue` regularly
## How to? (old and a bit buggy)
1. Fill `config.json` with a `password`, your github oauth `client_id` and `client_secret`
2. Create folder `accounts`
3. Start webServer.py and browse to shown address, authorize with github, enter IMAP details and register it with your set password.
4. Create cron to run checkMail.py regularly
