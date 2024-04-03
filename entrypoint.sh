#!/bin/bash

# Run the migrations
alembic -c /app/app/core/db/migrations/alembic.ini upgrade head

# Run the API
uvicorn app.main:app --host 0.0.0.0 --port 8000