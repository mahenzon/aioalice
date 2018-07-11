import logging

log = logging.getLogger(__name__)


class BaseStorage:
    """
    You are able to save current user's state
    and data for all steps in states storage
    """

    async def close(self):
        """
        You have to override this method and use when application shutdowns.
        Perhaps you would like to save data and etc.

        :return:
        """
        raise NotImplementedError

    async def wait_closed(self):
        """
        You have to override this method for all asynchronous storages (e.g., Redis).

        :return:
        """
        raise NotImplementedError

    async def get_state(self, user_id, default):
        """
        Get current state of user. Return `default` if no record found.

        :param user_id:
        :param default:
        :return:
        """
        raise NotImplementedError

    async def get_data(self, user_id, default):
        """
        Get state data for user. Return `default` if no data is provided in storage.

        :param user_id:
        :param default:
        :return:
        """
        raise NotImplementedError

    async def set_state(self, user_id, state):
        """
        Set new state for user

        :param user_id:
        :param state:
        """
        raise NotImplementedError

    async def set_data(self, user_id, data):
        """
        Set data for user

        :param user_id:
        :param data:
        """
        raise NotImplementedError

    async def update_data(self, user_id, data=None, **kwargs):
        """
        Update data for user

        You can use data parameter or|and kwargs.

        :param data:
        :param user_id:
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    async def reset_data(self, user_id):
        """
        Reset data for user.

        :param user_id:
        :return:
        """
        await self.set_data(user_id, data={})

    async def reset_state(self, user_id, with_data=False):
        """
        Reset state for user.
        You may desire to use this method when finishing conversations.

        :param user_id:
        :param with_data:
        :return:
        """
        await self.set_state(user_id, state=None)
        if with_data:
            await self.reset_data(user_id)

    async def finish(self, user_id):
        """
        Finish conversation with user.

        :param user_id:
        :return:
        """
        await self.reset_state(user_id, with_data=True)


class DisabledStorage(BaseStorage):
    """
    Empty storage. Use it if you don't want to use Finite-State Machine
    """

    async def close(self):
        pass

    async def wait_closed(self):
        pass

    async def get_state(self, user_id, default):
        return None

    async def get_data(self, user_id, default):
        self._warn()
        return {}

    async def set_state(self, user_id, state):
        self._warn()

    async def set_data(self, user_id, data):
        self._warn()

    async def update_data(self, user_id, data=None, **kwargs):
        self._warn()

    @staticmethod
    def _warn():
        log.warning("You haven’t set any storage yet so no states and no data will be saved.\n"
                    "You can connect MemoryStorage for debug purposes or non-essential data.")
