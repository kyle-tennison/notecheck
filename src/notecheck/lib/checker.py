from pathlib import Path
import re
from dotenv import load_dotenv
from loguru import logger
from notecheck.lib.prompts import GRAMMAR_INSTRUCTION, AUDIT_INSTRUCTION
from openai import OpenAI, RateLimitError
from notecheck.lib.util import backoff_on_exception

IGNORE_PATTERNS = [r".*\.excalidraw\.md$"]
CACHE_FILE = Path(__file__).parent.parent.parent.parent / "cache.txt"
CACHE_FILE.touch()

load_dotenv()


class NoteChecker:
    """
    Utility for proofreading and auditing markdown notes using the OpenAI API.
    """

    def __init__(self, notes_root: Path):
        """
        Initialize the NoteChecker.

        Args:
            notes_root (Path): The root directory containing markdown note files.
        """
        self.notes_root = notes_root.expanduser().absolute()
        self.openai = OpenAI()

    def proofread_file(self, file: Path):
        """
        Send markdown content to OpenAI for grammar correction.

        Args:
            file (Path): The markdown file to process.
        """
        file_content = file.read_text()

        modified_content = self.openai.responses.create(
            model="o3-mini",
            instructions=GRAMMAR_INSTRUCTION,
            input=file_content,
        ).output_text

        file.write_text(modified_content)

    def audit_file(self, file: Path):
        """
        Send markdown content to OpenAI for clarity and style auditing.

        Args:
            file (Path): The markdown file to process.
        """
        file_content = file.read_text()

        modified_content = self.openai.responses.create(
            model="o3-mini",
            instructions=AUDIT_INSTRUCTION,
            input=file_content,
        ).output_text

        file.write_text(modified_content)

    def process(self):
        """
        Process all markdown files in the notes directory.

        Applies grammar correction and style auditing to each eligible file,
        skipping cached entries and using exponential backoff on rate limits.
        """

        @backoff_on_exception(RateLimitError)
        def task(file: Path):
            """
            Handle a single file with proofreading and auditing steps.

            Args:
                file (Path): The markdown file to process.
            """
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
            file
            for file in self.notes_root.rglob("*.md")
            if not any(re.compile(pat).fullmatch(str(file)) for pat in IGNORE_PATTERNS)
        ]

        for file in files:
            task(file)
