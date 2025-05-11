# Mask Bloc Bot

To connect this bot to your Discord server with the necessary permissions, you'll have to have 
1. Created an application on Discord
2. Categorized it as a bot
3. Gone to this URL to authorize your bot on the server(s) you want it: `https://discord.com/oauth2/authorize?client_id=<BOT_CLIENT_ID>&permissions=<PERMISSIONS>&integration_type=0&scope=bot` where
   - BOT_CLIENT_ID is also referred to as a bot's Application ID by Discord
   - PERMISSIONS is an integer that can be determined at the bottom of this page https://discord.com/developers/applications/YOUR_APPLICATION_ID_HERE/bot
      - This bot needs the ability to manage roles, which is 268435456.
      - It also needs to be above any roles that it is going to manage in the discord Roles tab in order to do so.

## Requirements

## To Run With Docker Compose
Rename `.example.env.dev` and `.example.env.prod` to `.env.dev` and `.env.prod` respectively, and fill them each in with the respective environment's variables.

Run this command to start the bot as well as a process that checks if the image has been updated every 30 seconds for CI/CD: 

```
docker compose up
```
