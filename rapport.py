def home(self):
        
        self.initialiseFrameBody()
        ## code des composant cards de la fenetre 1
        
        def chargerproduit():
            curseur=self.connection.cursor()
            curseur.execute("select count(*) from Produit")
            nombre=curseur.fetchone()
            return nombre[0]
        
        def  recuperervaleurproduit():
            chargerproduit()
            prodstock.configure(text=chargerproduit())
            

        
        
        
        
        
        
        ## pour produit en stock 
        self.pi=Image.open("assets/stock.png")
        self.rpi=self.pi.resize((50, 50))
        self.pi1=ImageTk.PhotoImage(self.rpi)
        
        fprod=CTkFrame(self.framebody, width=230, height=100, fg_color="white", border_color="blue", corner_radius=5, border_width=2)
        fprod.place(x=50, y=50)
        
        
        CTkLabel(fprod, text="Produits en\nStock", text_color="black", font=("arial", 15, "italic"),
                 image=self.pi1, compound="right").place(x=10, y=10)
        prodstock=CTkLabel(fprod, text="", text_color="black", font=("arial", 25, "bold"))
        prodstock.place(x=100, y=60)
        
        recuperervaleurproduit()
        
        
        
        prodvendu=CTkFrame(self.framebody, width=230, height=100, fg_color="white", border_color="blue", corner_radius=5, border_width=2)
        prodvendu.place(x=330, y=50)
        #pour produit vendu
        self.pi=Image.open("assets/vendu1.png")
        self.rpi=self.pi.resize((50, 50))
        self.pi1=ImageTk.PhotoImage(self.rpi)
        
        def produitvendu():
            curseur=self.connection.cursor()
            curseur.execute("select count(*) from Vente")
            nombre=curseur.fetchone()
            return nombre[0]
        def recuperervaleurproduitvendu():
            produitvendu()
            totalvendu.configure(text=produitvendu())
        CTkLabel(prodvendu, text="Nombre de\nProduit Vendu", text_color="black", font=("arial", 15, "italic"),
                 image=self.pi1, compound="right").place(x=10, y=10)
        totalvendu=CTkLabel(prodvendu, text="", text_color="black", font=("arial", 25, "bold"))
        totalvendu.place(x=100, y=60)
        
        
        recuperervaleurproduitvendu()
        
        
        #pour chiffre d'affaire
        self.pi=Image.open("assets/chiffre2.jpg")
        self.rpi=self.pi.resize((50, 50))
        self.pi1=ImageTk.PhotoImage(self.rpi)
        
        fvente=CTkFrame(self.framebody, width=230, height=100, fg_color="white", border_color="blue", corner_radius=5, border_width=2)
        fvente.place(x=600, y=50)
        
        CTkLabel(fvente, text="Chiffre d'affaire\nTotal", text_color="black", font=("arial", 15, "italic"),
                 image=self.pi1, compound="right").place(x=10, y=10)
        
        sommetotalevente=CTkLabel(fvente, text="", text_color="black", font=("arial", 15, "bold"))
        sommetotalevente.place(x=10, y=60)
        
        def sommetotaleventes():
            curseur=self.connection.cursor()
            curseur.execute("select sum(prixUnitaire * quantiteVendu) from Vente")
            nombre=curseur.fetchone()
            return nombre[0]
        def recuperervaleursommetotaleventes():
            sommetotaleventes()
            s=float(sommetotaleventes())
            totalFormat = "{:,.0f}".format(s).replace(",", " ")
            sommetotalevente.configure(text=str(totalFormat)+" GNF")
        recuperervaleursommetotaleventes()
        
        
        fclient=CTkFrame(self.framebody, width=230, height=100, fg_color="white", border_color="blue", corner_radius=5, border_width=2)
        fclient.place(x=860, y=50)
        #pour client
        self.pi=Image.open("assets/client.png")
        self.rpi=self.pi.resize((50, 50))
        self.pi1=ImageTk.PhotoImage(self.rpi)
        
        CTkLabel(fclient, text="Clients", text_color="black", font=("arial", 15, "italic"),
                 image=self.pi1, compound="right").place(x=10, y=10)
        
        nbclient=CTkLabel(fclient, text="", text_color="black", font=("arial", 25, "bold"))
        nbclient.place(x=100, y=60)
        
        def recuperervaleurclient():
            curseur=self.connection.cursor()
            curseur.execute("select count(*) from Client")
            nombre=curseur.fetchone()
            return nombre[0]
        def recuperervaleurclient2():
            recuperervaleurclient()
            nbclient.configure(text=recuperervaleurclient())
        recuperervaleurclient2()
            
        
        
        ## images pour la fenetre
        
        self.image1=Image.open("assets/8.png")
        self.i1r=self.image1.resize((700, 400))
        self.ph=ImageTk.PhotoImage(self.i1r)
        
        CTkLabel(self.framebody, text="", image=self.ph).place(x=450, y=250)
        
        
        ## quantite total restant
        fquantite=CTkFrame(self.framebody, width=230, height=100, fg_color="white", border_color="blue", corner_radius=5, border_width=2)
        fquantite.place(x=50, y=200)
        
        self.pi=Image.open("assets/stock2.png")
        self.rpi=self.pi.resize((50, 50))
        self.pi1=ImageTk.PhotoImage(self.rpi)
        
        CTkLabel(fquantite, text="Quantite Totale\n Restante", text_color="black", font=("arial", 15, "italic"),
                 image=self.pi1, compound="right").place(x=10, y=10)
        labqteR=CTkLabel(fquantite, text="", font=("arial", 25, "bold"))
        labqteR.place(x=100, y=60)
        
        def chargerquantiteR():
            curseur=self.connection.cursor()
            curseur.execute("select sum(produitQte) from Produit")
            nombre=curseur.fetchone()
            return nombre[0]
        def quantiteR():
            chargerquantiteR()
            labqteR.configure(text=chargerquantiteR())
        quantiteR()