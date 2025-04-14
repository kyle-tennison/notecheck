
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import re
import time
from loguru import logger
from note_checker.lib.prompts import GRAMMAR_INSTRUCTION, AUDIT_INSTRUCTION
from openai import OpenAI, RateLimitError
from tqdm import tqdm
from note_checker.lib.util import backoff_on_exception

IGNORE_PATTERNS = [r'.*\.excalidraw\.md$']
CACHE_FILE = Path(__file__).parent.parent.parent.parent / "cache.txt"
CACHE_FILE.touch()

class NoteChecker:

    def __init__(self, notes_root: Path):
        self.notes_root = notes_root.expanduser().absolute()
        self.openai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def proofread_file(self, file: Path):
        file_content = file.read_text()

        modified_content = self.openai.responses.create(
            model="o3-mini",
            instructions=GRAMMAR_INSTRUCTION,
            input=file_content,
        ).output_text

        file.write_text(modified_content)

    def audit_file(self, file: Path):
        file_content = file.read_text()

        modified_content = self.openai.responses.create(
            model="o3-mini",
            instructions=AUDIT_INSTRUCTION,
            input=file_content,
        ).output_text

        file.write_text(modified_content)



    def process(self):

        @backoff_on_exception(RateLimitError)
        def task(file: Path):

            if not file.read_text().strip():
                return

            if str(file.resolve()) in CACHE_FILE.read_text().splitlines():
                logger.debug(f"File {file} was cached")
            else:
                logger.info(f"Processing {file}")
                self.proofread_file(file)
                self.audit_file(file)
                CACHE_FILE.write_text(CACHE_FILE.read_text() + f"\n{file.resolve()}")

        files = [
            file for file in self.notes_root.rglob("*.md")
            if not any(re.compile(pat).fullmatch(str(file)) for pat in IGNORE_PATTERNS)
        ]

        for file in files:
            task(file)

