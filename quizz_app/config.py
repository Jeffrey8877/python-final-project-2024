# Flask configuration settings

# Generated using: python -c 'import secrets; print(secrets.token_hex(16))'
SECRET_KEY = 'your-secret-key-here'  # TODO: You should generate your own secret key

# Database settings
DATABASE_PATH = 'database/quiz.db'

# Flask settings
DEBUG = True  # Should be False in production
SESSION_COOKIE_SECURE = False  # Should be True in production
TEMPLATES_AUTO_RELOAD = True