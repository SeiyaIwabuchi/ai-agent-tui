import os
from os.path import join, dirname
import sys
from dotenv import load_dotenv

load_dotenv(verbose=True)

extDataDir = os.getcwd()
if getattr(sys, 'frozen', False):
    extDataDir = sys._MEIPASS
load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

host = os.environ.get("host")