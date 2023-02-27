import os

from dotenv import load_dotenv

load_dotenv()

"""
This main file and we have to run this file and this application
runs on uvicorn server on 8000 port.
"""

if __name__ == "__main__":
    os.system("uvicorn server.main:app --reload --port 8000")
