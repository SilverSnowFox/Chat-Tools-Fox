# Chat Tools Fox
 Discord.py bot about chat and message tools.

## Commands
For commands, `<>` mean required and `[]` are optional.

### Utilities

- `Invites [@user]` - Sends a list of the top 25 invites or a list of the user's invites.
- `Botinfo` - Sends an embed with my information.
- `Invite` - Sends an embed with buttons to invite me to your servers.
- `@me` - If you mention me, I'll reply with the server's prefix.
- `Serverinfo` - Sends an embed with the server's information.
- `Voting` - You can support me by voting too!
- `Userinfo [@user]` - Sends an embed with the user's information. If you don't mention a user, it sends one with your information.
- `Poll <question$option 1$option 2$...>` - A poll command that allows between 2 and 10 options separated by '$'. A user can only have one vote.

### Admin

- `Prefix <prefix>` - Changes the bot prefix to an argument between 1 and 10 characters.
- `Lang` - To change the bot language.
- `Settings` - Displays the server's module settings and allows to disable or enable the moderation modules.
- `Purge <number> [@user]` - Deletes the 'number' of messages. If a user is mentioned, it deletes 'number' messages of that user.
- `Set <category> <channel>` - Set the channel for suggestions, reports or Improved Pins.
- `Remove <category>` - Removes the channel for suggestions, reports or Improved Pins.
- `Log <type> <channel>` - Sets up the log channel for the type. use `Log types` for the list of log types.
- `Show-logs` - Shows the channels the logs are set-up to.

## Modules

Explanation on the modules. Use `settings` to check the server's settings.

### Improved Pins
When a user pins a message, I will send the message to the set pins channel as an embed, together with the files, and unpin it to avoid reaching the pin limit.

![Improved Pins image](https://github.com/SilverSnowFox/Chat-Tools-Fox/blob/main/ReadMeFiles/Pins.PNG?raw=true)

### Message Links
When a user sends the link to a message I can access, I will display the contents of the message and its author.

![Message links image](https://github.com/SilverSnowFox/Chat-Tools-Fox/blob/main/ReadMeFiles/msgLink.PNG?raw=true)

### Anti-Scam
If a user sends a link to a scam registered in my database, I will delete that message.

![Anti-scams image](https://github.com/SilverSnowFox/Chat-Tools-Fox/blob/main/ReadMeFiles/Scams.PNG?raw=true)

### Anti-Ghost Ping
Ever wanted to know who was it that mentioned you and deleted the message? If they do, I will send a message with who was mentioned.

![Anti-ghost pings image](https://github.com/SilverSnowFox/Chat-Tools-Fox/blob/main/ReadMeFiles/Ghost.PNG?raw=true)