from flask import Flask
from supabase_api.api.api_bp_layer import user_api

app = Flask(__name__)

# Register the blueprint
app.register_blueprint(user_api)

if __name__ == '__main__':
    app.run(debug=True)
