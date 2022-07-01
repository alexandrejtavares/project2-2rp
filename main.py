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

    try:
        logger.info("VAGRANT - Initializing virtual machine.")
        subprocess.run(command)
        return True
    except:    
        logger.error("VAGRANT - Error initializing virtual machine.")
        return False

#----------------------------------------------------------------------
@logger.catch
def install_zeppelin():
    '''
    Installs Apache Zeppelin in the VM.
    '''
    try:
        logger.info(f"Installing Apache Zeppelin in the virtual machine.")
        ssh_command = "sudo yum install -y zeppelin"
        command = f"vagrant ssh -c '{ssh_command}' "
        subprocess.run(command)
        logger.info(f"Apache Zeppelin installed successfully.")
    except:    
        logger.debug(f"Command: {command}")
        logger.error("Error installing Apache Zeppelin.")

#----------------------------------------------------------------------
@logger.catch
def install_java():
    '''
    Installs Java in the VM.
    '''
    try:
        logger.info(f"Installing java in the virtual machine.")
        ssh_command = "sudo yum install -y java"
        command = f"vagrant ssh -c '{ssh_command}' "
        subprocess.run(command)
        logger.info(f"Java was installed successfully")
    except:    
        logger.debug(f"Command: {command}")
        logger.error("Error installing Java.")

if __name__ == "__main__":

    # Get program path
    app_dir = path.dirname(path.realpath(__file__))

    # Vagrant path
    vagrant_path = path.join(app_dir, "vagrant")

    # Change workdir to vagrant path
    os.chdir(vagrant_path)

    # Inicializa a máquina virtual
    if vagrant_up():
        # Instala o Java
        install_java()

        # Instala o Apache Zeppelin
        install_zeppelin()
