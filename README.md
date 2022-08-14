# **Gatekeeper V2**

Welcome to the efforts of countless hours of learning and failed attempts at writing code that culminated into this project known as Gatekeeper! Originally this started out as a bot to bring CubeCoders AMP to Discord with support for only Minecraft, but has evolved into this encompasing project of providing support for any type of server AMP can run along with providing as many of AMPs core features inside of Discord.

Need Support or have questions? Please visit my Discord and post in the respective channels.
Come Join my Discord - **[Kat's Paradise](https://discord.gg/s5FnnsbJ)**


## **Features**
___
-
-
-
### **Requirements**
_________
- Python 3.1 or greater
- Pip 2.1 or greater
- Discord.py 2.0 or greater 
    - *Please visit: https://github.com/Rapptz/discord.py to install discord.py development version!*
- Cube Coders AMP License
    - *https://cubecoders.com/AMP*


## **Installation Methods**
___
### **Manual Instructions**
1. Open your command line: run `sudo apt-get install -y python3 pip && git clone https://github.com/Rapptz/discord.py && cd discord.py && python3 -m pip install -U .[voice]`
2. Create an AMP user for the Bot with `Super Admins` role.
3. Follow the instructions in `tokenstemplate.py` file -> [tokenstemplate.py](/tokenstemplate.py)
4. From Command Line run script `start.py` *(eg. `../Discord Bot/start.py`)*
    - Run the bot, it will finish installing the rest of the requirements.
5. See **[Interacting with the Bot~](#interacting-with-the-bot)**

### **AMP Instance Instructions**
1. Create an AMP user for the Bot with `Super Admins` role.
2. Create a new instance of GatekeeperV2 in a container. *(The container option can be found under `Configuration -> New Instance Defaults`)*
3. Configure the settings in the GatekeeperV2 Instance under the `Configuration -> Bot Settings`, click `Update`, then start the bot.
4. See **[Interacting with the Bot~](#interacting-with-the-bot)**
___

## **Interacting with the Bot**
*Parameters such as `role` and `channel` support IDs and names*
- See **[Commands](/COMMANDS.md#commands-list)** for a full list of all Bot Commands and how to use them.

### **Setting up a NON-Adminstrator Role for the Bot**
- Use `/bot moderator (role)` and the bot will add that role as the minimum required role to interact with the bot.
    - **TIP** - Use this if you want NON-Discord Admins to have the ability to interact with the bot
    - It does honor the role heirarchy set via `Discord -> Server Settings -> Roles`.
    - Want more control? See **[Setting up Custom Permissions](/PERMISSIONS.md#permissions).**

### **Setting your AMP Console Channels**
- Use `/server console channel (channel)` and the bot will begin sending AMP Console messages to that channel. 
    - **TIP**: You can also send AMP Console commands through that Discord Channel to the Dedicated Server.

### **Setting your AMP Chat Channels**
- Use `/server chat channel (channel)` and the bot will begin sending AMP Chat messages to that channel. 
    - **TIP**: You can also send Chat messages through that Discord Channel to the Dedicated Server.
    
## **Setting your Whitelist Channel and Auto Whitelist Settings**
- Use `/bot whitelist channel (channel)` to set a channel for the bot to check whitelist requests.
    - **ATTENTION**: The Bot will not do anything with those requests unless you turn on `auto-whitelist`
- Use `/bot whitelist auto true` to allow the bot to handle whitelist requests in your whitelist channel!
    - **ATTENTION**: The Bot has a **default wait time of 5 minutes**, after the wait time is up they are whitelisted.
- Use `/bot whitelist waittime (time)` to adjust the Bot's wait time after a whitelist request.
    - **TIP**: You can set this value to `None` or `0` to allow the bot to instantly whitelist the user.

______
## **Launch Args**
- `-token` - Bypasse tokens validation check. *(Mandatory for AMP Template Installations/Operations)*
- `-command` - Enable slash command print statements for user traceback.
- `-dev` - Enable development print statments. *(used for development)*
- `-debug` - Enables *DEBUGGING* level for logging. *(used for development)*
- `-discord` - Disables Discord Intigration *(used for testing)*
- `-super` - This leaves AMP Super Admin role intact, use at your own risk.    
___
### **Credits**
"**Thank You**" to everyone at CubeCoders Discord Server, especially *IceofWrath, Mike, Greelan* and everyone else in their discord.

"**Thank You**" to everyone over at Discord.py Discord Server, especially *SolsticeShard and sgtlaggy* for all the silly questions I kept asking about embed's and Hybrid messages!

___
### **Want to Support?**
*Visit my [Patreon](https://www.patreon.com/Gatekeeperv2)*