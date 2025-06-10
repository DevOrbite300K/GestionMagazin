def client(self):
        self.initialiseFrameBody()
        
        
        clientinfo=LabelFrame(self.framebody, text="veiller saisir les information du client",
                            width=700, height=200, font=("arial", 15, "italic"), 
                            border=2)
        clientinfo.place(x=30, y=20)
        
        self.pi=Image.open("assets/iccli2.png")
        self.rpi=self.pi.resize((350, 200))
        self.pi1=ImageTk.PhotoImage(self.rpi)
        
        CTkLabel(self.framebody, text="", image=self.pi1).place(x=780, y=20)
        
        idclient=CTkEntry(clientinfo, width=150, placeholder_text="identifiant", corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black")
        idclient.place(x=10, y=10)
        nomclient=CTkEntry(clientinfo, width=150, placeholder_text="nom complet", corner_radius=0, height=40, 
                         font=("arial", 15, "bold"), placeholder_text_color="black")
        nomclient.place(x=10, y=70)
        
        telclient=CTkEntry(clientinfo, width=150, placeholder_text="Tel:", corner_radius=0, height=40, 
                         font=("arial", 15, "bold"), placeholder_text_color="black")
        telclient.place(x=10, y=120)
        
        adclient=CTkEntry(clientinfo, width=150, placeholder_text="Adresse:", corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black")
        adclient.place(x=170, y=10)
        
        
        listeclient=CTkFrame(self.framebody, width=1100, height=400)
        listeclient.place(x=30, y=250)
        CTkLabel(listeclient, text="La Liste Des Clients", width=150,
                 font=("arial", 35, "bold"), text_color="blue").place(x=350, y=10)
        
        
        def recherche(e):
            try:
                videtableauclient()
                curseur=self.connection.cursor()
                req="select * from Client where clientNomPrenom like ? or clientTelephone like ? or clientAdresse like ?"
                curseur.execute(req, ("%"+txtrecherche.get()+"%", "%"+txtrecherche.get()+"%", "%"+txtrecherche.get()+"%"))
                donnees=curseur.fetchall()
                
                for x in donnees:
                    tableclient.insert("", "end", values=x)
            except:
                messagebox.showinfo("info", "aucune lignes trouvé")
        
        txtrecherche=CTkEntry(listeclient, width=450, height=40,
                              corner_radius=0, placeholder_text="recherche par: nom, adresse",
                              font=("arial", 15, "italic"), placeholder_text_color="black")
        txtrecherche.place(x=310, y=60)
        txtrecherche.bind("<KeyRelease>", recherche)
        
        
        
        ### Gestions des actions sur les clients
        ## vider le tableau
        def videtableauclient():
            for s in tableclient.get_children():
                tableclient.delete(s)
        
        def chargertableclient():
            try:
                videtableauclient()
                curseur=self.connection.cursor()
                req="""select * from Client """
                curseur.execute(req)
                lignes=curseur.fetchall()
                
                for x in lignes:
                    tableclient.insert("", "end", values=x)
            except:
                messagebox.showerror("erreur", "exception leve") 
            
            
        ## La methode d'ajout d'un nouveau client
        def ajouter():
            ## vide la liste des fournisseur avant d'inserer un enregistrement
            try:
                
                curseur=self.connection.cursor()
                req=""" insert into Client(clientNomPrenom, clientTelephone, clientAdresse)
                    values(?, ?, ?)
                    """                
                if nomclient.get()=="" or telclient.get()=="" or adclient.get()=="":

                    messagebox.showwarning("Attention", "champs requis")
                else:
                    curseur.execute(req, (nomclient.get().upper(), telclient.get().upper(), adclient.get().upper()))
                    self.connection.commit()
                    chargertableclient()

                    messagebox.showinfo("info", "client ajouté")   
            except:
                messagebox.showerror("erreur", "doublons interdit sur le numero")      
            
           
        def modifier():
            curseur=self.connection.cursor()
            
            if idclient.get()=="" or nomclient.get()=="" or telclient.get()=="" or adclient.get()=="":
                messagebox.showwarning("attention", "veuillez renseigner tout les champs")
            else:
                
                curseur.execute("update Client  set clientNomPrenom =?, clientTelephone =?, clientAdresse=? where clientID =?", (nomclient.get().upper(), telclient.get().upper(), adclient.get().upper(), idclient.get()))
                self.connection.commit()
                messagebox.showinfo("info", "client modifier avec success")
                chargertableclient()
            
        def supprimer():
            try:
                
                curseur=self.connection.cursor()
            
                message=messagebox.askyesno(title="attention", message="voulez vous supprimer cet enregistrement")
                if message:
                    req=" delete from Client where clientID = ? "
            
                    curseur.execute(req, (idclient.get(), ))
                    self.connection.commit()
                    chargertableclient()
                
            except:
                pass        
            
        
        ## la methode permettant de selectionner une ligne dans la liste des fournisseurs
        def selectclient(e):
            
            idclient.delete(0, END)
            nomclient.delete(0, END)
            telclient.delete(0, END)
            adclient.delete(0, END)
               
            
            ligne=tableclient.focus()
            valeurs=tableclient.item(ligne, 'values')
            
            idclient.insert(0, valeurs[0])
            nomclient.insert(0, valeurs[1])
            telclient.insert(0, valeurs[2])
            adclient.insert(0, valeurs[3])
               
            
            ## le tableau pour les client
            
        
        vsb = ttk.Scrollbar(listeclient, orient="vertical")
        vsb.place(x=950, y=130, height=235)
        
        tableclient=ttk.Treeview(listeclient, columns=("fournisseurID", "nomcomplet", "telephone", "adresse"),
                                  show="headings", yscrollcommand=vsb.set, selectmode="browse")
        vsb.config(command=tableclient.yview)
        tableclient.heading("fournisseurID", text="ClientID")
        tableclient.heading("nomcomplet", text="Nom et Prenom")
        tableclient.heading("telephone", text="Telephone")
        tableclient.heading("adresse", text="Adresse")
        
        
        tableclient.place(x=140, y=130)
        
        tableclient.bind("<ButtonRelease-1>", selectclient) 
        
        chargertableclient()
        ### ****** les boutons pour client ***********
          
        CTkButton(clientinfo, text="Ajouter", font=("arial", 15, "bold"), corner_radius=5, height=40, border_width=1,
                  fg_color="white", text_color="black", border_color="green",  command=ajouter
                  ).place(x=370, y=10)
        CTkButton(clientinfo, text="Modifier", font=("arial", 15, "bold"), corner_radius=5, height=40, border_width=1,
                  fg_color="white", text_color="black", border_color="orange", command=modifier
                  ).place(x=370, y=65)
        CTkButton(clientinfo, text="Supprimer", font=("arial", 15, "bold"), corner_radius=5, height=40, border_width=1,
                  fg_color="white", text_color="black", border_color="red", 
                  command=supprimer).place(x=370, y=120)
        
        