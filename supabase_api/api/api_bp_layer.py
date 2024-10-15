from flask import Blueprint, jsonify, request
from supabase_api.application.user_service_impl import get_user_service

user_api = Blueprint('user_api', __name__)

# Create a user
@user_api.route('/users', methods=['POST'])
async def create_user():
    data = request.json  # The data to create a user (no logic needed here)
    user_service = await get_user_service()  # Get the service dynamically
    user = await user_service.create_user(data)
    return jsonify(user), 201

# Read a user by ID
@user_api.route('/users/<int:user_id>', methods=['GET'])
async def get_user(user_id):
    user_service = await get_user_service()
    user = await user_service.get_user(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

# Update a user
@user_api.route('/users/<int:user_id>', methods=['PUT'])
async def update_user(user_id):
    data = request.json  # Update data comes from the request
    user_service = await get_user_service()
    user = await user_service.update_user(user_id, data)
    if user:
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

# Delete a user
@user_api.route('/users/<int:user_id>', methods=['DELETE'])
async def delete_user(user_id):
    user_service = await get_user_service()
    success = await user_service.delete_user(user_id)
    if success:
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'error': 'User not found'}), 404
