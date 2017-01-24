rspamd_trainer
==============

A Python based rspamd training script. It parses the mail structure in the file system, finds all emails which are modified in a certain time period and calls rspamc learn_ham or rspamc learn_spam with every email found file.

It contains 2 scripts ham_trainer.py and spam_trainer.py.

You have to configure the paths in configure.py::

    FILE_LOGGER_LEVEL = 'DEBUG'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    CLI_LOGGER_LEVEL = 'DEBUG'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    RSPAMD_LOG_DIR = '/var/log/rspamd'
    RSPAMD_TRAINING_LOGFILE = 'training.log'

    now = time.time()
    min_time = now - 3 * 86400  # 3 days
    max_time = now - 33 * 86400  # 33 days
    start_path = "./shared/data/mail/"
    ham_exclude_parts = frozenset((
        '.Junk',
        '.Trash',
        '.Spam',
        '.Spamverdacht',
        '.Papierkorb'
    ))

    included_domains = (
        'domain1.com',
        'domain2.com',
    )


Ham trainer
-----------

To train ham just call::

    ./ham_trainer.py

Spam trainer
------------

To train spam, just call::

    ./spam_trainer.py

Logging
-------

The scripts are writing into the log file, be default: "/var/log/rspamd/training.log"

Regular training
----------------

To train every night, you can add the calls to your crontab.
The user should have write access to the log file and the permission to train rspamd.
