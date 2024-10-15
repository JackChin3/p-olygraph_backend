from supabase_api.infrastructure.user_impl import SupabaseUserRepository
from supabase_api.application.user_service_repository import UserRepository

class UserServiceImpl(UserRepository):
    def __init__(self, user_repository: SupabaseUserRepository):
        self.user_repository = user_repository

    async def create_user(self, data):
        return await self.user_repository.create_user(data)

    async def get_user(self, user_id):
        return await self.user_repository.get_user(user_id)

    async def update_user(self, user_id, data):
        return await self.user_repository.update_user(user_id, data)

    async def delete_user(self, user_id) -> bool:
        return await self.user_repository.delete_user(user_id)

# Factory function to get the user service with the repository implementation
async def get_user_service() -> UserRepository:
    user_repository = SupabaseUserRepository()
    return UserServiceImpl(user_repository)
