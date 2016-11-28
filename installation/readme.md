# Installation des raspi

On accède au raspi avec leur hostname (genre `ssh pi@master` ou `ssh pi@master.local`)
Pour régler le hostname, on change 2 fichiers : `/etc/hostname` et `/etc/hosts`



## Installation de ansible

J'ai la version `2.2.0.0`

    sudo pip install ansible --upgrade


## Installation des esclaves

    ansible-playbook --limit=slaves -i inventory playbook.yml


## Installation du master

    ansible-playbook --limit=master -i inventory playbook.yml


## Mise à jour du code

    ansible-playbook -i inventory playbook.yml --start-at-task=[Copy Zoomachine repository]

## Lancer une commande sur tout l'inventaire

    ansible all -e 'host_key_checking=False' -a "/sbin/poweroff" -i inventory --become # fait tout rebooter