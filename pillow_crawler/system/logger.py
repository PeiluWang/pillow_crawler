# coding = utf-8
import logging
import logging.config

logging.config.fileConfig("logging.conf")

root_logger = logging.getLogger("root")
root_logger.debug("test debug")
root_logger.info("test info")
