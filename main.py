import libvirt
import sys
import os
import logging
from datetime import datetime
from backup_modules.full_backup import FullBackupVM
from backup_modules.inc_backup import IncBackupVM

logging.basicConfig(
    filename='/var/log/backup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def ensure_directory(path):
    """Crea la carpeta si no existe."""
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f'Folder created: {path}')
        return True
    else:
        logging.info(f'Folder created: {path}')
        return False

# Verificar y crear las carpetas base
backup_base = '/backup'
vm_backup_dir = os.path.join(backup_base, 'vm')
ensure_directory(backup_base)
ensure_directory(vm_backup_dir)

# Obtener la fecha actual en formato yyyy-mm
today_date = datetime.today().strftime('%Y-%m')
monthly_backup_dir = os.path.join(vm_backup_dir, today_date)

# Verificar y crear carpeta mensual
ensure_directory(monthly_backup_dir)

try:
    conn = libvirt.open(None)
except libvirt.libvirtError:
    logging.error('Failed to open connection to the hypervisor')
    sys.exit(1)

try:
    domains = conn.listAllDomains()
    for domain in domains:
        if domain.ID() > 0:
            backup_dir = os.path.join(monthly_backup_dir, domain.name())
            if ensure_directory(backup_dir):
                backup_thread = FullBackupVM(domain, backup_dir)
            else:
                backup_thread = IncBackupVM(domain, backup_dir)
            backup_thread.start()
except libvirt.libvirtError:
    logging.error('Failed to find the domain')
    sys.exit(1)

conn.close()
