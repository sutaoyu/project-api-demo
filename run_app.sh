#!/bin/bash
gunicorn -D -c gunicorn.py app.main:app -n NPC_Backend
