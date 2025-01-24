# backup_modules/__init__.py

import logging

# Configuración del logger para los módulos de backup
logging.basicConfig(
    filename='/var/log/backup_modules.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

from .full_backup import FullBackupVM
from .inc_backup import IncBackupVM

__all__ = ['FullBackupVM', 'IncBackupVM']
