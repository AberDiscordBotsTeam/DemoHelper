# DemoHelper bot

stores a queue of people waiting for demonstrators to help them with their work or sign-off

## Install and use locally
1. Check python3, pip and pipenv are installed
2. Navigate to a terminal and `git clone  <repository url>` and cd into its directory
3. `pipenv install` to install dependencies
4. Navigate to the discord developers site, create a new application, go to the bot tab, add a bot and then copy the token from that tab
5. create a .env file with the token from the previous step using the format `DISCORD_TOKEN=<yourtoken-here>`
6. `pipenv run python3 -m demobot` to run the server
7. Navigate to the 0Auth2 tab and select bot from the scopes section, then scroll down and select the bot permissions: View channels and Send Messages. Copy the link from the scopes section and paste it into your web browser and select the servers you want to add the bot to
  
## Setting up as a service
1. Complete the steps from above apart from 6 and 7
2. create a file in `/etc/systemd/system/` called `demoBot.service` and add the following to the file:
```
[Unit]
Description=demoBot
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=<username>
WorkingDirectory=/home/<username>/demoHelperBot
ExecStart=/usr/bin/pipenv run python3 -m demobot

[Install]
WantedBy=multi-user.target
```
3. Once completed use the command `sudo systemctl daemon-reload` to reload the file

## The following commands are now used to manage the bot:
1. `sudo systemctl start demoBot` - start the service
2. `sudo systemctl status demoBot` - get the status of the service
3. `sudo systemctl stop demoBot` - stop the service
4. `systemctl restart demoBot` - restart the service
5. `sudo systemctl enable demoBot/sudo systemctl disable demoBot` - enable/disable the service on boot of server.
6. `journalctl -ru demobot.service` - view recent logs

## General maintenance
1. `pipenv update` to update dependencies
2. `git pull` to pull updates from the repository
3. `systemctl restart demoBot` to restart the service

## Preview of bot working
![help](https://raw.githubusercontent.com/IdrisTheDragon/demoHelperBot/master/help_2.png)

