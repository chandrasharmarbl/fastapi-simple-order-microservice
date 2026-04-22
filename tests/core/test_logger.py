import logging
from app.core.logger import get_logger


def test_get_logger_returns_configured_logger():
    logger = get_logger("test_module")
    
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_module"
    assert logger.level == logging.INFO
    
    # Check if a handler is attached
    assert len(logger.handlers) > 0
