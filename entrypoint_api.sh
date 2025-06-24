#!/bin/bash
sleep 2s

echo "Applying migrations..."
alembic upgrade head

echo "Starting application..."
cd app && python main.py