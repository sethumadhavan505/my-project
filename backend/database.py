"""Shared Supabase client used by API routes and background workers."""

from supabase import Client, create_client
from config import get_settings

settings = get_settings()


def get_supabase_client() -> Client:
    """Create the Supabase REST client from validated application settings."""
    return create_client(settings.supabase_url, settings.supabase_key)


supabase: Client = get_supabase_client()
