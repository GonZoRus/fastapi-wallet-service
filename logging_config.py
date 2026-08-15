import logging.config


def configure_logging() -> None:
    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {
                "simple": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "simple",
                    "level": "INFO",
                }
            },
            "loggers": {},
            "root": {
                "level": "INFO",
                "handlers": ["console"],
            },
            "disable_existing_loggers": False,
        }
    )
