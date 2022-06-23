#!python3
# -*- coding: utf-8 -*-

from os import path
import os
import subprocess
import sys
from loguru import logger

# VM name
vm_name = "teste-zeppelin"

#----------------------------------------------------------------------
@logger.catch
def vagrant_up() -> bool:
    command = "vagrant up"
    print (command)

    try:
        logger.info("Inicializando máquina virtual.")
        subprocess.run(command)
        return True
    except:    
        logger.error("VAGRANT - Erro ao iniciar a máquina virtual.")
        return False

#----------------------------------------------------------------------
@logger.catch
def install_zeppelin():
    '''
    Try to install Apache Zeppelin in VM.
    '''
    try:
        ssh_command = "sudo yum install -y zeppelin"
        command = f"vagrant ssh -c '{ssh_command}' "
        logger.debug(f"Instalando o Apache Zeppelin na máquina virtual. Comando: {command}")
    except:    
        logger.error("Erro ao instalar o Apache Zeppelin.")

# Get program path
app_dir = path.dirname(path.realpath(__file__))

# Vagrant path
vagrant_path = path.join(app_dir, "vagrant")

# Change workdir to vagrant path
os.chdir(vagrant_path)

# Inicializa a máquina virtual
vagrant_up()

# Instala o Apache Zeppelin
install_zeppelin()
