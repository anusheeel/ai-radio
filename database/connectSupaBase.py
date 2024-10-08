from dotenv import load_dotenv, find_dotenv
import os
from supabase import create_client, Client
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR2aG95YWVtY2Jhemx3aGRzZHd0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgxNzUxNDEsImV4cCI6MjA0Mzc1MTE0MX0.7FmHSiXQ3oUIN_UwFJCZLmaenAhfNyWyyVSwLbLqY0I"#os.getenv("SUPABASE_API_KEY")
SUPABASE_PROJECT_URL= "https://tvhoyaemcbazlwhdsdwt.supabase.co"#os.getenv("SUPABASE_PROJECT_URL")


# Initialize the Supabase client
supabase = create_client(SUPABASE_PROJECT_URL, SUPABASE_API_KEY)

# Make sure this client can be imported by other modules
def get_supabase_client():
    return supabase






