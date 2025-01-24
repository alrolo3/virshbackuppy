#!/bin/bash

echo "Actualizando el sistema..."
sudo dnf update -y

echo "Instalando dependencias del sistema..."
sudo dnf install -y python3 python3-pip libvirt libvirt-python virt-install qemu-kvm

echo "Instalando dependencias de Python..."
pip3 install -r requirements.txt

echo "Configurando permisos para libvirt..."
sudo usermod -aG libvirt $(whoami)

echo "Instalación completada. Reinicia tu sesión para aplicar los cambios."
