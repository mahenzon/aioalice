from ..dispatcher import BaseStorage


class MemoryStorage(BaseStorage):
    """In-memory states storage"""

    def __init__(self):
        self.data = {}

    async def close(self):
        self.data.clear()

    async def wait_closed(self):
        pass

    def _get_user_data(self, user_id):
        if user_id not in self.data:
            self.data[user_id] = {'state': None, 'data': {}}
        return self.data[user_id]

    async def get_state(self, user_id, default):
        user = self._get_user_data(user_id)
        return user['state']

    async def get_data(self, user_id, default):
        user = self._get_user_data(user_id)
        return user['data']

    async def set_state(self, user_id, state):
        user = self._get_user_data(user_id)
        user['state'] = state

    async def set_data(self, user_id, data):
        user = self._get_user_data(user_id)
        user['data'] = data

    async def update_data(self, user_id, data=None, **kwargs):
        user = self._get_user_data(user_id)
        if data is None:
            data = {}
        user['data'].update(data, **kwargs)
