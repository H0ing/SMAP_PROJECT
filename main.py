from core.report import greeting
from core.person import greet
from model.student import Student
from model.classroom import Classroom
from model.teacher import Teacher
from report.annual import Annual
from report.class_report import ClassReport
from report.transcript_report import TranscriptReport
import os, sys, json, csv, math, logging
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List, Optional
# ─── Setup logging ────────────────────────────────────────────────────────────
os.makedirs("logs",    exist_ok=True)
os.makedirs("data",    exist_ok=True)
os.makedirs("reports", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ─── ANSI colours ─────────────────────────────────────────────────────────────
R="\033[91m"; G="\033[92m"; Y="\033[93m"; B="\033[94m"
C="\033[96m"; W="\033[97m"; DIM="\033[2m"; BOLD="\033[1m"; RST="\033[0m"

def clr(t,c): return f"{c}{t}{RST}"
def bold(t):  return f"{BOLD}{t}{RST}"
def clear(): os.system("cls" if os.name=="nt" else "clear")



