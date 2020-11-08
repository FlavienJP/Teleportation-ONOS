# Reproduction d'une attaque par téléportation sur un controleur ONOS

_Article MISC n° 1XX_

_Flavien Joly-Pottuz / Stefano Secci_ | _**CNAM PARIS**_

## Installation du système

Les étapes ci-dessous permettent la mise en place de l'infrastructure décrite dans l'article 
"MISC - La téléportation, de la fiction au SDN.".

**1 /**  Installation minimale d’Ubuntu 18.4 LTS (machine type :20Gb HDD/8Gb RAM/ 2vCPU)

_**Attention : Pensez à installer le serveur SSH pour effectuer l'ensemble des étapes suivantes depuis un terminal.**_

**2 /** Installation des utilitaires système nécessaires :

`apt-get install openvswitch-switch python3.6 python3-pip`

**3 /** Vérification de la version de python

Une version 3.6 minimum est nécessaire car des f-strings sont utilisés dans les scripts python.

```
python3 --version
Python 3.6.9 
```

**4 /** Installation de SCAPY

Installation de la version 2.4.3 de la librairie SCAPY.

```
pip3 install scapy
```


**5 /**	Installation de java 8 
```
# Pour la suite de l’installation on se place dans /opt
cd /opt

# On télécharge l’archive de la version 8
wget -c --content-disposition https://javadl.oracle.com/webapps/download/AutoDL?BundleId=239835_230deb18db3e4014bb8e3e8324f81b43

# On renomme le fichier téléchargé par un nom plus simple
mv jdk-8u221-linux-x64.tar.gz\?GroupName\=JSC\&FilePath\=%2FESD6%2FJSCDL%2Fjdk%2F8u221-b11%2F230deb18db3e4014bb8e3e8324f81b43%2Fjdk-8u221-linux-x64.tar.gz\&BHost\=javadl.sun.com\&File\=jdk-8u221-linux-x64.tar.gz\&AuthParam\=1576094699_9eebfcd8fa45d1 jdk-8u221-linux-x64.tar.gz

# On décompresse l’archive contenant les fichiers nécessaires à l’installation
tar xzf jdk-8u221-linux-x64.tar.gz

# On installe ensuite la totalité des composants a l'aide du script suivant
for JavaCommand in java jar java2groovy javac javadoc javafxpackager javah javap javapackager javaws
do
         sudo update-alternatives --install /usr/bin/$JavaCommand $JavaCommand /opt/jdk1.8.0_221/bin/$JavaCommand 1
done
```

**6 /**	Installation d’ONOS en mode service suivant la [documentation officielle](https://wiki.onosproject.org/display/ONOS/Running+ONOS+as+a+service )

```
# Téléchargement de la derniere version d’ONO (2.4.0)
wget https://repo1.maven.org/maven2/org/onosproject/onos-releases/2.4.0/onos-2.4.0.tar.gz

# Décompression des archives téléchargée 
tar xzf onos-2.4.0.tar.gz

# Création du lien symbolique vers la version 2.4.0 pour poursuivre l’installation
ln -s /opt/onos-2.4.0 /opt/onos

# On déploie alors ONOS afin qu’il tourne en tant que service
cp /opt/onos/init/onos.initd /etc/init.d/onos
update-rc.d onos defaults
cp /opt/onos/init/onos.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable onos

# ONOS installé et démarré, il faut installer le package nécessaire a la reproduction (OpenFlow)
service onos start
ssh -p 8101 karaf@localhost (mot de passe: karaf)
    app activate org.onosproject.fwd
    app activate org.onosproject.openflow
    logout
```

### Accéder au dashboard ONOS

Le dashboard est alors accessible depuis l'interface web situé a l'adresse suivante :

```
http://<IP-machine-hote>:8181/onos/ui/ 
```

Les identifiants sont 'onos/rocks'

## Récupération du code nécéssaire aux reproductions ##

Nous allons ensuite cloner le contenu de ce dépot via Git afin de récuperer les scripts.
```
git clone https://github.com/FlavienJP/Teleportation-ONOS
```

L'ensemble des scripts se trouvera alors dans `/opt/Teleportation-ONOS/scripts`, pensez à le prendre en compte lors de 
l'invocation des différents scripts.

L'installation des éléments nécéssaires à la reproduction est terminée.

