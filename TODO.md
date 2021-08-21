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
- [ ] Voting Command
- [ ] Invite Command
- [ ] Bot information
- [ ] Check bot permissions
- [ ] User information
- [ ] Server information
- [ ] Mention to get server prefix

### Moderation
- [ ] Anti-ghost ping
- [ ] Word whitelisting, delete message and send warn embed
- [ ] Change prefixes
- [ ] Change languages

### Chat creation and editing
- [ ] Channel creating
  - Create with name
  - Optional add people
- [ ] Channel member actions
  - Add people
  - Remove people
- [ ] Edit description
- [ ] Slow-mode
- [ ] Delete channel

### Thread 
- [ ] Create thread (name, time, users)
- [ ] Delete thread
- [ ] Archive thread?

### Report
- [ ] Set report channel
- [ ] Send report (Message and attachments, if any)
  - Button to reject
  - Admin reply to reject (accept)
  - DM user about report answer
  - Edit report embed with answer
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
- [ ] Set pinned message channel
- [ ] Option to enable improved pins, which sends embed with embed content to a channel and link to message
  - Need to set channel first
  - Option to send and then unpin

### Logging 
- [ ] Set edit log channel
- [ ] Set pinned/unpin log channel
- [ ] Set delete message channel
- [ ] Set kicked channel
- [ ] Set banned channel
- [ ] Set joined channel
- [ ] Set leave channel

### Message Link
- [ ] If a message is linked, webhook with user avatar, name and embed of the content in the message referenced

### Admin
- [ ] Create muted role or set it up
- [ ] Kick command with reason
  - Check if user has permissions
  - Check if can kick the person
- [ ] Ban command with reason
  - Check if user has permissions
  - Check if can kick the person
- [ ] Mute with reason and time (or none)
  - Need to check if muted role exists
  - Need valid time
  - Need to be able to give person role
  - Need to check if mute works
- [ ] Unban
  - Check if user exists or is banned
- [ ] Un-mute
  - Check is person has muted role
  - Remove muted role
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
  - Show
  - Clear
  - Create 
    - Temporary
    - Permanent


### Anonymous chat
Need to check if possible to make a channel where sends messages with random gen, or number with increasing index using webhook and generic avatar.

### Background
- [ ] Prefixes SQL
- [ ] Languages SQL
- [ ] Server channels SQL
- [ ] EN Embeds
  - [ ] Help
  - [ ] Commands
  - [ ] Errors
- [ ] ES Embeds
  - [ ] Help
  - [ ] Commands
  - [ ] Errors