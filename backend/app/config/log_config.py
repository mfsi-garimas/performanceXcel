# app/config/log_config.py
import json
import logging
from datetime import datetime, timezone
from logging.handlers import TimedRotatingFileHandler
import os

from app.config.env_config import settings

# -------------------------------
# Environment & log level
# -------------------------------
ENV = settings.ENV
LOG_LEVEL = logging.DEBUG if ENV == "dev" else logging.INFO

# -------------------------------
# Log directory & file
# -------------------------------
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../logs"))
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "log.log")

BACKUP_COUNT = 3  # Keep last 3 days
# -------------------------------
# JSON Formatter
# -------------------------------
class JsonFormatter(logging.Formatter):
    """Custom formatter that outputs log records as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "env": ENV,
        }

        # Include extra fields passed via `extra={...}`
        for key, value in record.__dict__.items():
            if key not in (
                "name", "msg", "args", "levelname", "levelno", "pathname",
                "filename", "module", "exc_info", "exc_text", "stack_info",
                "lineno", "funcName", "created", "msecs", "relativeCreated",
                "thread", "threadName", "processName", "process"
            ):
                log_entry[key] = value

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            log_entry["stack"] = self.formatStack(record.stack_info)

        return json.dumps(log_entry, ensure_ascii=True)

# -------------------------------
# Handlers
# -------------------------------
# File handler with daily rotation
file_handler = TimedRotatingFileHandler(
    LOG_FILE,
    when="midnight",
    interval=1,
    backupCount=BACKUP_COUNT,
    utc=True
)
file_handler.setFormatter(JsonFormatter())
file_handler.setLevel(LOG_LEVEL)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(JsonFormatter())
console_handler.setLevel(LOG_LEVEL)

# -------------------------------
# Configure app logger
# -------------------------------
logger = logging.getLogger("app")
logger.setLevel(LOG_LEVEL)
logger.propagate = False  # Avoid duplicate logs

if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# -------------------------------
# Suppress noisy libraries
# -------------------------------
for lib in [
    "openai",
    "openai._base_client",
    "httpx",
    "httpcore",
    "langchain.agents.agent_iterator",
    "urllib3.connectionpool",
    "sentence_transformers",
    "sentence_transformers.SentenceTransformer",
    "transformers",
    "tokenizers",
    "filelock",
]:
    logging.getLogger(lib).setLevel(logging.WARNING)