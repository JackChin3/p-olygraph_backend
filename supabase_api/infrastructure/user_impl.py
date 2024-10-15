import os
import supabase
from supabase_api.domain.user_repository import UserRepository

class SupabaseUserRepository(UserRepository):
    def __init__(self):
        # Fetch the Supabase credentials from environment variables
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_key = os.getenv('SUPABASE_KEY')
        
        # Check if the environment variables are properly set
        if not supabase_url or not supabase_key:
            raise ValueError("Supabase URL or Key not set in environment variables")

        # Set up Supabase client
        self.client = supabase.create_client(supabase_url, supabase_key)

    async def create_user(self, data):
        response = self.client.table('users').insert(data).execute()
        return response.data[0] if response.data else None

    async def get_user(self, user_id):
        response = self.client.table('users').select('*').eq('id', user_id).execute()
        return response.data[0] if response.data else None

    async def update_user(self, user_id, data):
        response = self.client.table('users').update(data).eq('id', user_id).execute()
        return response.data[0] if response.data else None

    async def delete_user(self, user_id) -> bool:
        response = self.client.table('users').delete().eq('id', user_id).execute()
        
        if response.error: # type: ignore
            # Log or print the error if needed
            print(f"Error deleting user: {response.error}") # type: ignore
            return False

        return True  # Return True if delete was successful
