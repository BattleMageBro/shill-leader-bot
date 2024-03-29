# toDo вынести в отдельный конфиг файл и запилить уи-шку для того чтобы на ходу подкладывать сообщения, понять структуру нужную
MESSAGES = {
    'stateReset': 'Argument not found',
    'invalidKey': 'Key is invalid {key}',
    'stateChange': 'Successfully change state',

    'help': """Possible commands are:
/choose_options - press to choose between shilling options 
/start_shilling - press to start shilling process after choosing options 
/stop_shilling - press to stop shilling process 
/choose_shill_message - press if you want to change your message to a new template 
/choose_chat - press to select between chats, if you added ShillLeaderBot to more than one group chat 
/choose_packs - press to get description of our shilling packs 
/choose_links - press to input group links to create your own shilling list 
/choose_timeout - press to choose time between shilling messages posted by bot 
/choose_shill_end - press to create a timer for stoping the shilling process
/get_chat_info - press to get current options for chat you are working with at this moment

You can choose different shilling options for different chats""",

    'success_start': """Hello and Welcome to ShillLeaderBot. Now you need to add Bot to your group chat and make a bot Admin. Make sure it is able to: Change group info, Delete messages, Ban users, Invite users via link, Pin messages, Manage video chats. Then use /add_shillbot command in your chat.

Type /help to show all possible commands.""",

    'startShilling': 'We start this shill motherffuckers\nChoose text that you want to shill\nhere ...',
    'shillEnds': 'We end with mthrfucker shilling',
    
    'choose_options': 'Please choose whether you want to use built-in shilling packs with listed shilling group links or you want to create your own custom shilling list',
    'choose_shill_message': 'Now you need to create a shilling template. This is a message that will be printed by bot and going to be used for copying. Please create it with accordance to shilling rules from different shilling packs. You can use it to input detailed instructions and latest rules for Implicit shilling.',
    'choose_shill_message_success': 'ShillMessage chosen and it is:\n\n{}',
    'choose_chat': 'Please choose chat from this list',
    'choose_chat_success': 'Successfully chosen chat, now press /choose_options',
    'choose_packs_start': 'Now you can choose your shilling pack',
    'choose_packs': """These are our current packs with short description. You can read more on our website "ShillLabs.com"
HARD SHILLING - Shilling groups where you can shill everything in it - Allows links, links to TG, and longer messages with emojis.
SOFT SHILLING - Shilling groups allowing short messages WITHOUT LINKS. You can tag the TG Name. Spell it out with no @ as well.
SUPER SOFT SHILLING - Shilling groups allowing ONLY Implicit Shilling. No spam and direct advertising.
VIP Channels - Shilling groups with huge whales in them. Respected owners and strong communities. MOSTLY Implicit shilling allowed. """,
    'choose_packs_success': 'Successfully chosen pack',
    'choose_links': 'Please insert links separated with ","',
    'choose_links_success': 'Links for shilling are successfully chosen',
    'choose_timeout': 'Please choose time between shilling cycle in seconds. How often do you want the bot to send next link. Default parameter is 60 seconds',
    'choose_timeout_success': 'Timeout successfully chosen. The value is {} seconds',
    'choose_shill_end': 'Please choose time before stopping shilling process. Choose time in hours. Default parameter is 1 hour',
    'choose_shill_end_success': """Shill End Time successfully chosen. The value is {} hours.
Now you can start shilling process by pressing /start_shilling. To stop the process press /stop_shilling """ ,

    'chat_added': 'Successfully added chat, now you can set up bot\'s preferences by opening chat with bot. Then use /choose_options to start. Good luck!',
}

ERRORS = {
    'no_chats': 'You have no added chats. Please add ShillBot to the group chat you are managing and make a bot - Admin. Then use /add_shillbot command and return to this chat.',
    'chat_not_exist': "Chat you want to choose doesn\'t exist. Please try command /add_shillbot in your group chat or contact us @shillleaderbotchat.",
    'wrong_opts_data': 'please contact support chat @shillleaderbotchat',
    'timeout_format': "Incorrect value for timeout. This must be integer or float. Please choose timeout again",
    'end_timeout_format': 'Incorrect value for end timeout. This must be integer or float. Please choose timeout again',
    'start_shilling': 'Please fill shilling options before starting shilling process. You can do it with command /choose_options ',
    'no_user': 'Sorry user with your id {} doesn\'t exist in our database. Please contact support chat @shillleaderbotchat ',
    'no_current_chat': 'You have no chosen chat to work with. Please type /choose_chat if you already added ShillLeaderBot to your group chat or add new chat',
    'already_shilling': 'You already shilling. End shill with /stop_shilling command, choose other chat and options if needed and start again',
    'bot_kicked': "Bot was kicked from group you want to shill or bot is no admin more. Please check groupAdmins and make bot Admin then make command /add_shillbot before start shill process. "
}