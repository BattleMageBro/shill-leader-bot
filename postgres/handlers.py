from core import postgres
from exceptions import UserError
from logg import log
from messages import ERRORS


class UserHandler():
    def __init__(self):
        self.table_name = 'users'

    async def get(self, user_uuid):
        select_condintions = {'user_uuid': user_uuid}
        user = await postgres.select(self.table_name, select_condintions)
        if type(user) == list and len(user) != 0:
            user = user[0]
        else:
            user_message = (ERRORS['no_user']).format(user_uuid)
            dev_message = 'no user with id: {}'.format(user_uuid)
            raise UserError(user_message=user_message, dev_message=dev_message)
        log.info(f'GET {self.table_name} with id {user_uuid}')
        return user
    
    async def get_user_with_chat(self, user_uuid):
        user = await self.get(user_uuid)
        chat_uuid = user.get('current_chat')
        if not chat_uuid:
            user_message = (ERRORS['no_current_chat'])
            dev_message = 'User with id {} has no current_chat'.format(user_uuid)
            raise UserError(user_message=user_message, dev_message=dev_message)
        log.info(f'GET_WITH_CHAT {self.table_name} with id {user_uuid} current_chat {chat_uuid}')
        return user, chat_uuid

    async def patch(self, user_uuid, data):
        index_name = 'user_uuid'
        await postgres.update(self.table_name, index_name, user_uuid, data)
        log.info(f'PATCH {self.table_name} id {user_uuid} with data {data}')

    async def post(self, data):
        await postgres.insert(self.table_name, data)
        log.info(f'POST to {self.table_name} with data {data}')


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
        log.info(f'GET {self.table_name} with id {chat_uuid}')
        return chat
    
    async def patch(self, chat_uuid, data):
        index_name = 'chat_uuid'
        log.debug(data)
        await postgres.update(self.table_name, index_name, chat_uuid, data)
        log.info(f'PATCH {self.table_name} id {chat_uuid} with data {data}')

    async def post(self, data):
        await postgres.insert(self.table_name, data)
        log.info(f'POST to {self.table_name} with data {data}')


class UserChatHandler():
    def __init__(self):
        self.table_name = 'user_chat'

    async def get_chats_by_user(self, user_uuid):
        select_condintions = {'user_uuid': user_uuid}
        chats = await postgres.select(self.table_name, select_condintions)
        if type(chats) != list:
            chats = []
        log.info(f'GET_BY_USER {self.table_name} with id {user_uuid} chats are {chats}')
        return chats

    async def get_users_by_chat(self, chat_uuid):
        select_condintions = {'chat_uuid': chat_uuid}
        users = await postgres.select(self.table_name, select_condintions)
        if type(users) != list:
            users = []
        log.info(f'GET_BY_CHAT {self.table_name} with id {chat_uuid} users are {users}')
        return users

    async def post(self, data):
        await postgres.insert(self.table_name, data)
        log.info(f'POST to {self.table_name} with data {data}')

    async def have_link(self, user_uuid, chat_uuid):
        select_conditions = {'chat_uuid': chat_uuid, 'user_uuid': user_uuid}
        links = await postgres.select(self.table_name, select_conditions)
        if links:
            log.info(f'Found link by user {user_uuid} with chat {chat_uuid}')
            return True
        log.info(f'Not Found link by user {user_uuid} with chat {chat_uuid}')
        return False
    
    async def get_chats_with_names(self, user_uuid):
        search_condintions = {'user_chat.user_uuid': user_uuid}
        select_conditions = 'user_chat.chat_uuid,user_chat.user_uuid,chat.chat_name'
        join_conditions = {'table': 'chat', 'cond': 'user_chat.chat_uuid=chat.chat_uuid'}
        chats = await postgres.select_join(select_conditions, self.table_name, search_condintions, join_conditions)
        if type(chats) != list:
            chats = []
        log.info(f'GET_BY_USER_WITH_NAMES {self.table_name} with id {user_uuid} chats are {chats}')
        return chats


class PacksHandler():
    def __init__(self):
        self.table_name = 'packs'

    async def get(self, pack_uuid):
        select_condintions = {'pack_uuid': pack_uuid}
        pack = await postgres.select(self.table_name, select_condintions)
        if type(pack) == list and len(pack) != 0:
            pack = pack[0]
        else:
            pack = None
        log.info(f'GET {self.table_name} with id {pack_uuid}')
        return pack
    
    async def get_all(self):
        packs = await postgres.select(self.table_name, {})
        log.info(f'GET_ALL {self.table_name}')
        return packs

    async def patch(self, pack_uuid, data):
        index_name = 'pack_uuid'
        await postgres.update(self.table_name, index_name, pack_uuid, data)
        log.info(f'PATCH {self.table_name} id {pack_uuid} with data {data}')

    async def post(self, data):
        await postgres.insert(self.table_name, data)
        log.info(f'POST to {self.table_name} with data {data}')


user_handler = UserHandler()
chat_handler = ChatHandler()
user_chat_handler = UserChatHandler()
packs_handler = PacksHandler()