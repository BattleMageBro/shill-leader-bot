from core import postgres
from exceptions import UserError
from logg import log


class UserHandler():

    async def get(self, user_id):
        table_name = 'users'
        index_name = 'user_uuid'
        user = await postgres.select(table_name, index_name, user_id)
        if type(user) == list:
            user = user[0]
        else:
            user_message = str.format('Sorry user with your\'s id %s doesn\'t exist in our database.'
                                      'Please email to support.shill_leader@gmail.com we\'ll help you',
                                      user_id)
            dev_message = str.format('no user with id: %s', user_id)
            raise UserError(user_message=user_message, developer_message=dev_message)
        return user
    
    async def get_user_with_chat(self, user_uuid):
        user = await self.get(user_uuid)
        chat_id = user.get('current_chat')
        if not chat_id:
            user_message = str.format('You have no choosen chat to work with.' 
                                    'Please type /choose_chat if you already added chats to ShillLeaderBot or add new chat')
            dev_message = str.format('user with id %s has no current_chat', user_uuid)
            raise UserError(user_message=user_message, developer_message=dev_message)
        return user, chat_id

    async def patch(self, user_uuid, data):
        table_name = 'users'
        index_name = 'user_uuid'
        await postgres.update(table_name, index_name, user_uuid, data)

    async def post(self, data):
        table_name = 'users'
        await postgres.insert(table_name, data)


class ChatHandler():

    async def get(self, chat_uuid):
        table_name = 'chat'
        index_name = 'chat_uuid'
        chat = await postgres.select(table_name, index_name, chat_uuid)
        if type(chat) == list:
            chat = chat[0]
        else:
            chat = None
        log.debug(chat)
        return chat
    
    async def patch(self, chat_uuid, data):
        table_name = 'chat'
        index_name = 'chat_uuid'
        await postgres.update(table_name, index_name, chat_uuid, data)

    async def post(self, data):
        table_name = 'chat'
        await postgres.insert(table_name, data)


user_handler = UserHandler()
chat_handler = ChatHandler()