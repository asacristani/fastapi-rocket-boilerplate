#!/bin/bash

# Run the migrations
alembic upgrade head

# Run the API
uvicorn app.main:app --host 0.0.0.0 --port 8000