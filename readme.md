# demoHelper bot

stores a queue of people waiting for something to happen.

## usage/development

in discord devlopers site, create new app, swap to bot tab, add bot, here you with find token for the .env file, keep it secret, swap to auth0 tab and select bot and set permissons (currently only send messages needed), copy the link created and add to the server you want to run the bot on.  

create a .env file with `DISCORD_TOKEN=<yourtoken-here>`

```
pipenv install
pipenv run python3 -m demobot
```

![help](https://raw.githubusercontent.com/IdrisTheDragon/demoHelperBot/master/help.png)

