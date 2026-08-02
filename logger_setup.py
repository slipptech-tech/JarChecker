import logging
from pathlib import Path

class LoggerSetup:
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(log_dir / "jarchecker.log", encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger

if __name__ == "__main__":
    log = LoggerSetup.get_logger("JarCheckerCore")
    log.info("Logger initialized successfully.")