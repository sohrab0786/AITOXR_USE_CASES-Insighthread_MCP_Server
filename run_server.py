# run_server.py
import os
import sys
import uvicorn

# Add the root directory to sys.path
sys.path.append(os.path.dirname(__file__))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)