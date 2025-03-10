import logging
import threading
from time import sleep
import lxml.etree as ET
import libvirt

class IncBackupVM(threading.Thread):
    def __init__(self,domain, backup_dir):
        super().__init__()
        self.backup_xml_string = None
        self.checkpoint_xml_string = None
        self.domain = domain
        self.backup_dir = backup_dir
        self.last_checkpoint =  str(max([int(checkpoint.getName()) for checkpoint in domain.listAllCheckpoints()]))


    def run(self):
        """Método que ejecuta el backup completo."""
        logging.info(f'Iniciando respaldo completo para {self.domain.name()}')
        self.prepare_backup()
        self.perform_backup()
        logging.info(f'Respaldo completo finalizado para {self.domain.name()}')

    def generate_backup_xml(self):
        root = ET.Element("domainbackup", mode="push")
        incremental = ET.SubElement(root, "incremental")
        incremental.text = self.last_checkpoint
        disks = ET.SubElement(root, "disks")
        disk = ET.SubElement(disks, "disk", name="vda", backup="yes", type="file", backupmode="incremental")
        target = ET.SubElement(disk, "target", file=f"{self.backup_dir}/{self.domain.name()}-{self.last_checkpoint}.qcow2.bak")
        driver = ET.SubElement(disk, "driver", type="qcow2")

        self.backup_xml_string = ET.tostring(root, pretty_print=True, encoding='unicode')
        print("Generated backup XML:\n", self.backup_xml_string)

    def generate_checkpoint_xml(self):
        root = ET.Element("domaincheckpoint")
        description = ET.SubElement(root, "description")
        description.text = "Incremental backup for VM"
        # name = ET.SubElement(root, "name")
        # name.text = "full-rocky9"
        disks = ET.SubElement(root, "disks")
        disk = ET.SubElement(disks, "disk", name="vda", checkpoint="bitmap")

        self.checkpoint_xml_string = ET.tostring(root, pretty_print=True, encoding='unicode')
        print("Generated checkpoint XML:\n", self.checkpoint_xml_string)

    def monitor_backup(self):
        while True:
            stats = self.domain.jobStats(0)
            if stats['disk_remaining'] == 0:
                break
        sleep(2)
        stats = self.domain.jobStats(1)
        if stats.get('success'):
            logging.info(f"Backup completado con éxito para la VM: {self.domain.name()}")
        else:
            logging.error(f"Backup fallido para la VM: {self.domain.name()}")

    def prepare_backup(self):
        self.generate_backup_xml()
        self.generate_checkpoint_xml()

    def perform_backup(self):
        self.domain.backupBegin(self.backup_xml_string, self.checkpoint_xml_string)
        self.monitor_backup()
