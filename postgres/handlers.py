from core import postgres
from exceptions import UserError
from logg import log


class UserHandler():
    def __init__(self):
        self.table_name = 'users'

    async def get(self, user_uuid):
        select_condintions = {'user_uuid': user_uuid}
        user = await postgres.select(self.table_name, select_condintions)
        if type(user) == list and len(user) != 0:
            user = user[0]
        else:
            user_message = ('Sorry user with your\'s id {} doesn\'t exist in our database.'
                            'Please email to support.shill_leader@gmail.com we\'ll help you').format(user_uuid)
            dev_message = 'no user with id: {}'.format(user_uuid)
            raise UserError(user_message=user_message, dev_message=dev_message)
        return user
    
    async def get_user_with_chat(self, user_uuid):
        user = await self.get(user_uuid)
        chat_id = user.get('current_chat')
        if not chat_id:
            user_message = ('You have no choosen chat to work with.' 
                            'Please type /choose_chat if you already added chats to ShillLeaderBot or add new chat')
            dev_message = 'User with id {} has no current_chat'.format(user_uuid)
            raise UserError(user_message=user_message, dev_message=dev_message)
        return user, chat_id

    async def patch(self, user_uuid, data):
        index_name = 'user_uuid'
        await postgres.update(self.table_name, index_name, user_uuid, data)

    async def post(self, data):
        await postgres.insert(self.table_name, data)


class ChatHandler():
    def __init__(self):
        self.table_name = 'chat'

    async def get(self, chat_uuid):
        select_condintions = {'chat_uuid': chat_uuid}
        chat = await postgres.select(self.table_name, select_condintions)
        if type(chat) == list and len(chat) != 0:
            chat = chat[0]
        else:
            chat = None
        log.debug(chat)
        return chat
    
    async def patch(self, chat_uuid, data):
        index_name = 'chat_uuid'
        await postgres.update(self.table_name, index_name, chat_uuid, data)

    async def post(self, data):
        await postgres.insert(self.table_name, data)


class UserChatHandler():
    def __init__(self):
        self.table_name = 'user_chat'

    async def get_chats_by_user(self, user_uuid):
        select_condintions = {'user_uuid': user_uuid}
        chats = await postgres.select(self.table_name, select_condintions)
        if type(chats) != list:
            chats = []
        return chats

    async def get_users_by_chat(self, chat_uuid):
        select_condintions = {'chat_uuid': chat_uuid}
        users = await postgres.select(self.table_name, select_condintions)
        if type(users) != list:
            users = []
        return users

    async def post(self, data):
        await postgres.insert(self.table_name, data)

    async def have_link(self, user_uuid, chat_uuid):
        select_conditions = {'chat_uuid': chat_uuid, 'user_uuid': user_uuid}
        links = await postgres.select(self.table_name, select_conditions)
        if links:
            return True
        return False


user_handler = UserHandler()
chat_handler = ChatHandler()
user_chat_handler = UserChatHandler()