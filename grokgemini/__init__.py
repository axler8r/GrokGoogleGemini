from loguru import logger

__app_name__ = "grokgemini"
__version__ = "0.8.0"

logging_confiig: dict[str, list[dict[str, str]]] = {
    "handlers": [
        {
            "sink": "log/grokgemini.log",
            "level": "TRACE",
            "rotation": "1 week",
            "compression": "zip",
            "mode": "a",
        },
        {
            "sink": "sys.stderr",
            "level": "WARNING",
        },
    ]
}

logger.configure(**logging_confiig)
