import libvirt
import sys

try:
    conn = libvirt.openReadOnly(None)
except libvirt.libvirtError:
    print('Failed to open connection to the hypervisor')
    sys.exit(1)

try:
    domains = conn.listAllDomains()
    for domain in domains:
        print(domain.ID(), domain.name())

except libvirt.libvirtError:
    print('Failed to find the main domain')
    sys.exit(1)