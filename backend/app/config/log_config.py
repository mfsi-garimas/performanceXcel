import json
import logging
from datetime import datetime, timezone
from logging.handlers import TimedRotatingFileHandler
from app.config.env_config import settings
import os

ENV = settings.ENV
LOG_LEVEL = logging.DEBUG if ENV == "dev" else logging.INFO

LOG_DIR = os.path.join(os.path.dirname(__file__), '../logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "agentic_backend.log")
MAX_MB = 10
BACKUP_COUNT = 3

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
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            log_entry["stack"] = self.formatStack(record.stack_info)
        return json.dumps(log_entry, ensure_ascii=True)

# Remove all handlers associated with the root logger object (avoid duplicate logs)
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)


# File handler with daily rotation
file_handler = TimedRotatingFileHandler(
    LOG_FILE, when="midnight", interval=1, backupCount=BACKUP_COUNT, utc=True
)
file_handler.setFormatter(JsonFormatter())
file_handler.setLevel(LOG_LEVEL)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(JsonFormatter())
console_handler.setLevel(LOG_LEVEL)


# Configure root logger
logging.basicConfig(level=LOG_LEVEL, handlers=[file_handler, console_handler])
logger = logging.getLogger("app")

# Suppress verbose OpenAI and HTTP client logs
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("openai._base_client").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("langchain.agents.agent_iterator").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
logging.getLogger("sentence_transformers.SentenceTransformer").setLevel(logging.WARNING)
logging.getLogger("transformers").setLevel(logging.WARNING)
logging.getLogger("tokenizers").setLevel(logging.WARNING)
logging.getLogger("filelock").setLevel(logging.WARNING)