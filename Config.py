import sqlite3
class DB:
    def __init__(self):
        self.creationBase()
        self.creationtable()
        
    def creationBase(self):
        conn=sqlite3.connect("stock.db")
        
    def creationtable(self):
        try:
            conn=sqlite3.connect("stock.db")
            cur=conn.cursor()
            reqFournisseur="""
                    CREATE TABLE IF NOT EXISTS Fournisseur (
                        fournisseurID INTEGER PRIMARY KEY AUTOINCREMENT,
                        fournisseurNomPrenom TEXT NOT NULL,
                        fournisseurTelephone TEXT unique,
                        fournisseurAdresse TEXT not null
                                            )
                """
            reqProduit="""
                    CREATE TABLE IF NOT EXISTS Produit (
                        produitID INTEGER PRIMARY KEY AUTOINCREMENT,
                        ProduitNom TEXT NOT NULL ,
                        produitCategorie TEXT,
                        produitPU REAL NOT NULL,
                        produitQte INTEGER NOT NULL DEFAULT 0,
                        fournisseurID INTEGER,
                        FOREIGN KEY (fournisseurID) REFERENCES Fournisseur(fournisseurID)
                                                                                            )
              
                    """
            
            cur.execute(reqFournisseur)
            cur.execute(reqProduit)
            ### les tables ne sont pas creer d'abord
            reqClient=""" create table if not exists Client (

                        clientID INTEGER PRIMARY KEY AUTOINCREMENT,
                        clientNomPrenom varchar(150) ,
                        clientTelephone varchar(15) unique , 
                        clientAdresse varchar (100)
                
                                                            )
                        """
                        
            reqVente=""" create table if not exists Vente(
                
                venteID integer primary key AUTOINCREMENT,
                produitID integer not null,
                prixUnitaire  REAL not null,
                quantiteVendu integer not null,
                dateVente date not null,
                clientTelephone varchar(15), 
                infoVente varchar(255),         
                foreign key (produitID) references Produit(produitID)            
            )         
            """
            cur.execute(reqClient)
            cur.execute(reqVente)
            
            reqReçu="""
                        create table if not exists Reçu(
                            idreçu integer primary key autoincrement,
                            produit varchar(150) not null,
                            qtevendu integer not null,
                            pu REAL not null,
                            telclient varchar(15),
                            datevente date not null
                        )  
                    """
            cur.execute(reqReçu)
            
            reqUser=""" create table if not exists Utilisateur(
                
                id integer primary key autoincrement,
                email varchar(200) unique not null,
                password varchar(255) unique not null
                
                ) """
            
            cur.execute(reqUser)
        except:
            print("echec de connexion")
        
    