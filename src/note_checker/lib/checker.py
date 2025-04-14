
import os
from pathlib import Path
import re
from loguru import logger
from note_checker.lib.prompts import GRAMMAR_INSTRUCTION, AUDIT_INSTRUCTION
from openai import OpenAI
from tqdm import tqdm

IGNORE_PATTERNS = [r'.*\.excalidraw\.md$']

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
            model="o1",
            instructions=AUDIT_INSTRUCTION,
            input=file_content,
        ).output_text

        file.write_text(modified_content)



    def process(self):
        files = list(self.notes_root.rglob("*.md"))
        pbar = tqdm(files, desc="Starting", unit="file")
        i = 0

        for file in pbar:
            # Skip files that match ignore patterns
            if any(re.compile(pat).fullmatch(str(file)) for pat in IGNORE_PATTERNS):
                continue

            # Update progress bar description with the current file name
            pbar.set_description(f"Processing: {file.name}")
            self.proofread_file(file)
            self.audit_file(file)

            i += 1
            if i > 10:
                break