from config import FILE_LOGGER_LEVEL, CLI_LOGGER_LEVEL, RSPAMD_LOG_DIR
from config import RSPAMD_TRAINING_LOGFILE
from logging import DEBUG, WARNING, INFO, ERROR, CRITICAL
from pathlib import Path
import logging


LOG_LEVEL = {
    'DEBUG': DEBUG,
    'WARNING': WARNING,
    'INFO': INFO,
    'ERROR': ERROR,
    'CRITICAL': CRITICAL,
}


rspamd_log_dir = Path(RSPAMD_LOG_DIR)
logfile = rspamd_log_dir / Path(RSPAMD_TRAINING_LOGFILE)

rspamd_trainer_logger = logging.getLogger('rspamd_trainer')
rspamd_trainer_logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL[CLI_LOGGER_LEVEL])

fh = logging.FileHandler(str(logfile.absolute()))
fh.setLevel(LOG_LEVEL[FILE_LOGGER_LEVEL])

formatter = logging.Formatter(
    '%(asctime)s %(name)s[%(levelname)s]: %(message)s')

ch.setFormatter(formatter)
fh.setFormatter(formatter)

rspamd_trainer_logger.addHandler(ch)
rspamd_trainer_logger.addHandler(fh)
