import os

# In a real app, use environment variables. 
# For this challenge, we can default to a strict key or allow setting via ENV.
API_KEY_SECRET = os.getenv("API_KEY_SECRET", "sk_test_123456789")
