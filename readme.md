# Alexandre Tavares - Vagrant Project

## Tarefas

- Criar um script Vagrant que suba uma máquina CentOS 7.x com 2 CPUs (2 cores de processador), 4 GB de memória RAM e 50gb de HD chamada “teste-zeppelin”. O acesso a ela deve ser através de uma chave privada, não com senha.  
- Criar um programa em python que faça a instalação do Java e do Apache Zeppelin nessa máquina recém criada. Além disso, o programa deve subir o webserver do Zeppelin na porta 8888 e fazer uma criação de usuários a partir da lista presente no arquivo Lista_Usuarios_Zeppelin.txt.  

## Ferramentas
- Vagrant 2.2.19
- Oracle VirtualBox 6.1.20
- CentOS 7
- JDK 1.8.0_332
- Wget 1.14
- 

## Como Executar
Execute o comando:

``
python main.py
``

O programa executará os passos abaixo:

1. Inicialização da VM "teste-zeppelin" no Virtual Box.
2. Instalação do Java na VM.
3. Instalação do Apache Zeppelin.


## Documentação Utilizada

- https://www.vagrantup.com/docs  
- https://zeppelin.apache.org/docs  
- https://www.oracle.com/java/technologies/jdk-script-friendly-urls/  
    
 