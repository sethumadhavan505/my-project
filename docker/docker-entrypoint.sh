#!/bin/bash
set -e

# Validate hosted Supabase credentials before starting the API.
# This application uses the Supabase HTTP API, not a local PostgreSQL host.
echo "Checking Supabase configuration..."
python -c "from database import supabase; print('Supabase client configured successfully.')"

# Ensure the embedding model is cached before the API starts.
echo "Checking embedding model cache..."
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2'); print('Embedding model is ready.')"

echo "Starting IEEE Paper Generator Backend..."
exec "$@"
