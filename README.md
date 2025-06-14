# Gestion Magazin de ventes sous python

ce projet consiste a automatiser la gestion de vente dans un magazin donnée

# comment l'installer ?

1. avoir github installer
2. combiner les touches windows + R
3. entrer la commande: git clone https://github.com/DevOrbite300K/GestionMagazin

# dependances a installer 
1. avoir python installer
2. dans l'invite de commande taper: pip install customtkinter
3. dans l'invite de commande taper : pip install qrcode
4. dans l'invite de commande taper : pip install fpdf2


# attention: si vous etes nouveau a utiliser l'application penser a creer votre utilisateur comme suit:
1. ouvrer votre application ou projet dans le cmd et taper les commandes suivantes:

import sqlite3

conn=sqlite3.connect("./stock.db")

cur=conn.cursor()
req="insert into Utilisateur(email, password) values(?, ?)"

cur.execute(req, ("root@gmail.com", "root"))
conn.commit()

vous pouvez mainant utiliser ces identifiant la pour vous connecter:
email: root@gmail.com
password: root
