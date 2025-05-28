def produit(self):
        self.initialiseFrameBody()
        
        
        def produitstockinferieur5():
            try:
                
                
                curseur=self.connection.cursor()
                curseur.execute("select ProduitNom from Produit where produitQte < 5")
                donnees=curseur.fetchall()
                for x in donnees:
                    messagebox.showwarning("attention", "le produit "+x[0]+" est inferieur a 5")
            except:
                messagebox.showinfo("info", "aucun produit n'a la quantite inferieur a 5")
        
        produitstockinferieur5()
        
        prodinfo=LabelFrame(self.framebody, text="veiller saisir les information du produit",
                            width=700, height=200, font=("arial", 15, "italic"), 
                            border=2)
        prodinfo.place(x=30, y=20)
        
        pi=Image.open("assets/icprod2.png")
        rpi=pi.resize((350, 200))
        pi1=ImageTk.PhotoImage(rpi)
        
        CTkLabel(self.framebody, text="", image=pi1).place(x=780, y=20)
        
        ### Les champs de saisie
        
        codeprod=CTkEntry(prodinfo, width=150, placeholder_text="code", corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black")
        codeprod.place(x=10, y=10)
        nomprod=CTkEntry(prodinfo, width=150, placeholder_text="nom", corner_radius=0, height=40, 
                         font=("arial", 15, "bold"), placeholder_text_color="black")
        nomprod.place(x=10, y=70)
        
        catprod=CTkEntry(prodinfo, width=150, placeholder_text="categorie", corner_radius=0, height=40, 
                         font=("arial", 15, "bold"), placeholder_text_color="black")
        catprod.place(x=10, y=120)
        
        puprod=CTkEntry(prodinfo, width=150, placeholder_text="le prix unitaire", corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black")
        puprod.place(x=170, y=10)
        
        quantiteprod=CTkEntry(prodinfo, width=150, placeholder_text="la quantite", corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black")
        quantiteprod.place(x=170, y=70)
        
        fournisseurprod=CTkComboBox(prodinfo, width=150, corner_radius=0, height=40,
                          font=("arial", 15, "bold"), values=["fournisseur", "barry", "diallo", "sow "] )
        fournisseurprod.place(x=170, y=120)
          
        
        
        def colonnefournisseur():
            curseur=self.connection.cursor()
            curseur.execute(
            """
                select fournisseurTelephone from Fournisseur 
            """
            )
            fournisseurprod.set("numero des fournisseurs")
            contenu=curseur.fetchall()
            numfour=[]
            
            for c in contenu:
                #print(c)
                for d in c:
                    #print(d)
                    numfour.append(d)
            fournisseurprod.configure(values=numfour)
                
            
        colonnefournisseur()
        ### methode de selection du tableau
        
        def selectTableau(event):
            
            try:
                
                codeprod.delete(0, END)
                nomprod.delete(0, END)
                catprod.delete(0, END)
                puprod.delete(0, END)
                quantiteprod.delete(0, END)
                fournisseurprod.set("")
                
                
                ligne=tableproduit.focus()
                valeurs=tableproduit.item(ligne, 'values')
                
                codeprod.insert(0, valeurs[0])
                nomprod.insert(0, valeurs[1])
                catprod.insert(0, valeurs[2])
                puprod.insert(0, valeurs[3])
                quantiteprod.insert(0, valeurs[4])
                fournisseurprod.configure(values=[valeurs[5]])
                fournisseurprod.set(valeurs[5])
            except:
                pass
        
        #### ********** Les Methodes des actions pour les produits *********
        
        def videchampsaisieproduit():
            codeprod.delete(0, END)
            nomprod.delete(0, END)
            catprod.delete(0, END)
            puprod.delete(0, END)
            quantiteprod.delete(0, END)
            fournisseurprod.set("")
            
            
        def ajouter():
            
            ## vider le tableau avant d'ajouter de nouvelle lignes
            
            
            try:
                
                
                curseur=self.connection.cursor()
            
                reqIdf="select fournisseurID from Fournisseur where fournisseurTelephone = ?"
                curseur.execute(reqIdf, (fournisseurprod.get(), ))
            
                resultat=curseur.fetchone()
                idf=resultat[0]
                
                insert= "insert into Produit(ProduitNom, produitCategorie, produitPU, produitQte, fournisseurID) values (?, ?, ?, ?, ?)"
                if nomprod.get()=="" or catprod.get()=="" or puprod.get()=="" or quantiteprod.get()=="":
                    messagebox.showwarning("attention", "champs requis")
                else:
                    curseur.execute("select ProduitQte from Produit where ProduitNom=?", (nomprod.get().upper(), ))
                    valeur=curseur.fetchone()
                    
                    if valeur:
                        existe=valeur[0]
                        quantite=int(quantiteprod.get())
                        nouvellequantite=existe+quantite
                        curseur.execute("update Produit set produitQte =?  where ProduitNom =? ", (nouvellequantite, nomprod.get().upper()))
                        self.connection.commit()
                        messagebox.showinfo("info", "quantite mis a jour pour le produit existant")
                        videchampsaisieproduit()
                        
                    
                    else:
                        curseur.execute(insert, (nomprod.get().upper(), catprod.get().upper(), puprod.get().upper(), quantiteprod.get().upper(), idf))
                
                        self.connection.commit()
                        messagebox.showinfo("info", "produit ajouté")
                        videchampsaisieproduit()
                chargerproduit()
                
            except:
                messagebox.showwarning("attention", "exception lever")  
            
        def modifier():
            
            try:
                
                curseur=self.connection.cursor()
                
            
                curseur.execute("update Produit set ProduitNom=?, produitCategorie=?, produitPU=?, produitQte=?  where produitID=? ", (nomprod.get().upper(), catprod.get().upper(), puprod.get().upper(), quantiteprod.get().upper(), codeprod.get()))
                self.connection.commit()
                messagebox.showinfo("info", "produit modifier")
                chargerproduit()
            except:
                messagebox.showerror("info", "exception lever")
                
        def supprimer():
            try:
                
                curseur=self.connection.cursor()
                message=messagebox.askyesno(title="attention", message="voulez vous supprimer cet enregistrement")
                if message:
                    req=" delete from Produit where produitID = ? "
            
                    curseur.execute(req, codeprod.get())
                    self.connection.commit()
                    chargerproduit()
                    messagebox.showinfo("info", "produit supprimer")
            except:
                messagebox.showerror("info", "exception lever")
        def chargerproduit():
            try:
                videtableauprod()
                curseur=self.connection.cursor()
                curseur.execute("select * from Produit")
                donnees=curseur.fetchall()
                for x in donnees:
                    tableproduit.insert("", "end", values=x)
            except:
                pass
        
        def rechercher(e): 
            entre=txtrecherche.get() 
            if entre=="":
                pass
            else:
                videtableauprod()
                try:
                    curseur=self.connection.cursor()
            
                    req="select *  from Produit where ProduitNom like ? or produitCategorie like ? or fournisseurID like ? or produitQte like ?"
                    curseur.execute(req, ('%'+ entre.upper() + '%', '%'+ entre.upper() + '%', '%'+ entre.upper() + '%', '%'+ entre.upper() + '%'))
                    lignes=curseur.fetchall()
                    
                    
                    for x in lignes:
                        tableproduit.insert("", "end", values=x)
                except:
                    messagebox.showerror("erreur", "exception leve")
                        
        ## **************** Les boutons d'actions ***************************
        
        CTkButton(prodinfo, text="Ajouter", font=("arial", 15, "bold"), corner_radius=0, height=40, 
                  fg_color="green", text_color="white", command=ajouter).place(x=370, y=10)
        CTkButton(prodinfo, text="Modifier", font=("arial", 15, "bold"), corner_radius=0, height=40,
                  fg_color="orange", text_color="white", command=modifier).place(x=370, y=65)
        CTkButton(prodinfo, text="Supprimer", font=("arial", 15, "bold"), corner_radius=0, height=40, 
                  fg_color="red", text_color="white",
                  command=supprimer).place(x=370, y=120)
        
        
        listeprod=CTkFrame(self.framebody, width=1100, height=400)
        listeprod.place(x=30, y=250)
        CTkLabel(listeprod, text="La Liste Des Produits", width=150,
                 font=("arial", 35, "bold"), text_color="blue").place(x=350, y=10)
        
        txtrecherche=CTkEntry(listeprod, width=450, height=40,
                              corner_radius=0, placeholder_text="recherche par: nom, categories, fournisseur, qte",
                              font=("arial", 15, "italic"), placeholder_text_color="black")
        txtrecherche.place(x=310, y=60)
        
        txtrecherche.bind("<KeyRelease>", rechercher)
        
        
        
        ##boutons rafraichir
        i=Image.open("Icones/actualise.png")
        ri=i.resize((30, 30))
        pri=ImageTk.PhotoImage(ri)
        
        CTkButton(listeprod, text="", hover=False, image=pri, width=30, height=35,  fg_color="beige", command=chargerproduit
                  ).place(x=770, y=60)
        
        def exportexcel():
            import pandas as pd
            try:
                donnees=pd.read_sql_query("select * from Produit", self.connection)
                donnees.to_excel("produit.xlsx")
                
                os.startfile("produit.xlsx")
                messagebox.showinfo("info", "produit exporter sous excel")
            except:
                pass
                
        
        ##boutons excel
        i=Image.open("assets/excel.png")
        ri=i.resize((30, 30))
        pri=ImageTk.PhotoImage(ri)
        
        CTkButton(listeprod, text="", hover=False, image=pri, width=30, height=35,  fg_color="beige", command=exportexcel
                  ).place(x=820, y=60)
        
        
        
        
        ## le tableau pour les produits
        
        vsb = ttk.Scrollbar(listeprod, orient="vertical")
        vsb.place(x=1080, y=130, height=235)
        
        tableproduit=ttk.Treeview(listeprod, columns=("code", "nom", "categorie", "prixUnitaire", "quantite", "fournisseur"),
                                  show="headings", yscrollcommand=vsb.set, selectmode="browse")
        vsb.config(command=tableproduit.yview)
        tableproduit.heading("code", text="Codes")
        tableproduit.heading("nom", text="Noms")
        tableproduit.heading("categorie", text="Categories")
        tableproduit.heading("prixUnitaire", text="PrixUnitaire")
        tableproduit.heading("quantite", text="Quantite")
        tableproduit.heading("fournisseur", text="Fournisseurs")
        
        
        
        tableproduit.column("code", width=150)
        tableproduit.column("quantite", width=100)
        
        tableproduit.place(x=20, y=130)
        
        tableproduit.bind("<ButtonRelease-1>", selectTableau)
        
        ## vider le tableau
        def videtableauprod():
            for s in tableproduit.get_children():
                tableproduit.delete(s)            
                
        
        chargerproduit()
        