from pathlib import Path

from concurrent_log_handler import ConcurrentTimedRotatingFileHandler

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_ROOT = PROJECT_ROOT / "logs"
LOG_DIR_GENERAL = LOG_ROOT / "general"
LOG_DIR_ERRORS = LOG_ROOT / "errors"
LOG_DIR_CELERY_GENERAL = LOG_ROOT / "celery_general"
LOG_DIR_CELERY_ERRORS = LOG_ROOT / "celery_errors"

for directory in (
    LOG_DIR_GENERAL,
    LOG_DIR_ERRORS,
    LOG_DIR_CELERY_GENERAL,
    LOG_DIR_CELERY_ERRORS,
):
    directory.mkdir(parents=True, exist_ok=True)


class UtcConcurrentTimedRotatingFileHandler(
    ConcurrentTimedRotatingFileHandler,
):
    def __init__(
        self,
        filename: str,
        when: str = "midnight",
        interval: int = 1,
        backup_count: int = 30,
        encoding: str = "utf-8",
    ):
        super().__init__(
            filename,
            when=when,
            interval=interval,
            backupCount=backup_count,
            encoding=encoding,
            utc=True,
        )


logging_settings = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": (
                "%(filename)s:%(lineno)d #%(levelname)-8s "
                "[%(asctime)s] - %(name)s - %(message)s"
            ),
        },
    },
    "handlers": {
        "app_file": {
            "()": UtcConcurrentTimedRotatingFileHandler,
            "filename": LOG_DIR_GENERAL / "app.log",
            "formatter": "default",
            "level": "INFO",
        },
        "app_error_file": {
            "()": UtcConcurrentTimedRotatingFileHandler,
            "filename": LOG_DIR_ERRORS / "error.log",
            "formatter": "default",
            "level": "ERROR",
        },
        "celery_file": {
            "()": UtcConcurrentTimedRotatingFileHandler,
            "filename": LOG_DIR_CELERY_GENERAL / "celery.log",
            "formatter": "default",
            "level": "INFO",
        },
        "celery_error_file": {
            "()": UtcConcurrentTimedRotatingFileHandler,
            "filename": LOG_DIR_CELERY_ERRORS / "celery_error.log",
            "formatter": "default",
            "level": "ERROR",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
    },
    "loggers": {
        "": {
            "handlers": ["app_file", "app_error_file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "celery": {
            "handlers": ["celery_file", "celery_error_file", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
