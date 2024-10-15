from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, data):
        pass

    @abstractmethod
    async def get_user(self, user_id):
        pass

    @abstractmethod
    async def update_user(self, user_id, data):
        pass

    @abstractmethod
    async def delete_user(self, user_id) -> bool:
        pass
