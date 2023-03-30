#!/bin/bash
set -e
uvicorn main:app --host 0.0.0.0 --port 9102 --log-level debug --reload