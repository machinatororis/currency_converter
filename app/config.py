import os
import sys

from dotenv import load_dotenv


def get_base_path():
    """
    Returns the application base path.

    If the app is running as a PyInstaller executable,
    the base path is the folder where the .exe file is located.
    Otherwise, it is the project root folder.
    """
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


BASE_PATH = get_base_path()
ENV_PATH = os.path.join(BASE_PATH, ".env")

load_dotenv(ENV_PATH)

API_KEY = os.getenv("API_KEY")