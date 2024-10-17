from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
URI_STRING = os.getenv("MONGODB_URI")
NUM_ITEMS = 10000
NUM_SAMPLING = 1000
DB_NAME = "demo"
COLLECTION_NAME = "employee"
