#!/bin/bash

# 啟動 FastAPI 服務
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
