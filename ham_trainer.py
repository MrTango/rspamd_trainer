#!/usr/bin/env python3

from config import ham_exclude_parts, included_domains
from config import min_time, max_time, start_path
from logger import rspamd_trainer_logger as logger
from pathlib import Path, PurePath
import subprocess
import time


raw_counter = 0
counter = 0

t1 = time.time()
for dom in included_domains:
    for item in Path(start_path).rglob(dom + '/*/**/cur'):
        if not item.is_dir():
            continue
        if not ham_exclude_parts.isdisjoint(PurePath(item).parts):
            logger.debug(
                "Skip because of excluded parts match: %s" % str(
                    item.absolute()))
            continue
        for message_file in item.glob("*.*"):
            raw_counter += 1
            msg_mtime = message_file.stat().st_mtime
            if not message_file.is_file():
                continue
            if not (msg_mtime < min_time and msg_mtime > max_time):
                continue
            counter += 1
            with subprocess.Popen(
                    ["rspamc", "learn_ham", str(message_file.absolute())],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT) as p:
                try:
                    outs, errs = p.communicate(timeout=15)
                except subprocess.TimeoutExpired:
                    p.kill()
                    outs, errs = p.communicate()
                logger.debug(outs)


logger.info(
    "Learned ham from user folders with %s out of %s files in %s minutes." % (
        counter, raw_counter, int((time.time() - t1)) / 60))
