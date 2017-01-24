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
    for item in Path(start_path).rglob(dom + '/*/**/cur/*'):
        raw_counter += 1
        item_mtime = item.stat().st_mtime
        if not (item_mtime < min_time and item_mtime > max_time):
            continue
        if not item.is_file():
            continue
        if not ham_exclude_parts.isdisjoint(PurePath(item).parts):
            logger.debug("Skip because of excluded parts match: %s" % str(
                item.absolute()))
            continue
        counter += 1
        with subprocess.Popen(
                ["rspamc", "learn_ham", str(item.absolute())],
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
        counter, raw_counter, int((time.time()-t1)) / 60))