from loguru import logger

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
