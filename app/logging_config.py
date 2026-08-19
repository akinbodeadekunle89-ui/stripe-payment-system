import logging
import sys

# Configure the root logger
logger = logging.getLogger("payment_engine")
logger.setLevel(logging.INFO)

# 1. Console Handler (prints to your terminal)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)

# 2. File Handler (saves logs to a file named 'app.log' in your folder)
file_handler = logging.FileHandler("app.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
file_handler.setFormatter(file_formatter)

# Add both handlers to the logger (preventing duplicate handlers if re-imported)
if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)