#!/bin/sh
# Activate Python virtual environment
echo ==================================
echo Starting Flask Application
echo ==================================
. .env/bin/activate
# Run main.py
python main.py
