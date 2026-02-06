#!/bin/bash


cd /face

# Run with uv to ensure the virtual environment is used
uv run python -m app.main &
uv run python -m script.main &

# Wait for both processes
wait