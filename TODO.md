#Chat Tools Fox
This is a Discord.py bot that focuses on chat functionality and moderation.

### Help
- [ ] Help
  - [ ] Create Main
    - Select menu with categories
  - [ ] Create the categories
    - Use select menu with hidden reply
  - [ ] Button with invite

### Utilities
- [x] Voting Command
- [x] Invite Command
- [x] Bot information
- [x] User information
- [x] Server information
- [x] Mention to get server prefix

### Moderation
- [x] Anti-ghost ping
- [ ] Word whitelisting, delete message and send warn embed
- [x] Change prefixes
- [x] Change languages
- [x] Anti-scam
- [ ] Mute with reason and time (or none)
  - Need to check if muted role exists
  - Need valid time
  - Need to be able to give person role
  - Need to check if mute works
- [ ] Un-mute
  - Check is person has muted role
  - Remove muted role
- [ ] Clear Chat 

### Chat creation and editing
- [ ] Channel member actions
  - Add people
  - Remove people
- [ ] Edit description
- [ ] Slow-mode
- [ ] Delete channel

### Report
- [ ] Set report channel
- [ ] Send report (Message and attachments, if any)
  - Button to reject
  - Admin reply to reject (accept)
  - DM user about report answer
  Edit report embed with answer
- [ ] Try adding anonymous report

### Suggestions
- [ ] Set suggestion channel
- [ ] Suggest
  - Add button to upvote or down-vote
  - Admin reply to suggestion, or to close it with reason
- [ ] Try adding anonymous suggestion

### Poll
- [ ] Create a poll with upvote and down-vote, timed (none, msg)
  - Admin and poll creator button to close poll

### Improved pins
- [x] Created functions
- [ ] Set pinned message channel
- [ ] Option to enable improved pins, which sends embed with embed content to a channel and link to message
  - Need to set channel first
  - Option to send and then unpin

### Logging
- [ ] Set pinned/unpin log channel
- [ ] Set delete message and edit log channel
- [ ] Set kicked and banned channel
- [ ] Set join and leave channel

### Message Link
- [x] If a message is linked, webhook with user avatar, name and embed of the content in the message referenced
- [ ] Add option to enable/disable

### Admin
- [ ] Create muted role or set it up
- [ ] Start up
  - Creates log category with only admin perm can view
    - Create channel for join/leave
    - Create channel for message edit, ghost ping
    - Create channel for channel tools (pin, unpin, edit, create, delete)
    - Create channel for reports
    - Create channel for thread tools
  - Create suggestion channel
    - Can't send text
  - Create muted role
  - Create pins channel
    - Can't send text
- [ ] Invites
  - [x] Show
  - [ ] Clear


### Anonymous chat
Need to check if possible to make a channel where sends messages with random gen, or number with increasing index using webhook and generic avatar.

### Background
- [x] Prefixes JSON
- [x] Languages JSON
- [ ] Server channels SQL
- [ ] EN Embeds
  - [ ] Help
  - [ ] Commands
  - [ ] Errors
- [ ] ES Embeds
  - [ ] Help
  - [ ] Commands
  - [ ] Errors
- [ ] Add custom emotes for commands
- [ ] Disallow DM