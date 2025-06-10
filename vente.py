def vente(self):
        self.initialiseFrameBody()
        
        venteinfo=LabelFrame(self.framebody, text="veiller saisir les informations de la vente",
                            width=550, height=200, font=("arial", 15, "italic"), 
                            border=2)
        venteinfo.place(x=30, y=20)
        
        def calculatrice():
            os.system("calc")
        
        self.pi=Image.open("assets/calculer.jpg")
        self.rpi=self.pi.resize((120, 200))
        self.pi1=ImageTk.PhotoImage(self.rpi)
        
        CTkButton(self.framebody, text="", image=self.pi1, fg_color="white", border_color="white", 
                  hover=False, command=calculatrice).place(x=580, y=20)
        
        ### declaration des variable
        Date=StringVar()
        d=date.today().strftime("%d/%m/%Y")
        Date.set(d)
        print(d)
        
        
        panierframe=CTkFrame(self.framebody,
                            width=400, height=570
                            )
        panierframe.place(x=750, y=80)
        
        CTkLabel(panierframe, text="scanner pour voir les informations de la vente", font=("arial", 10, "bold"), text_color="blue"
                 ).place(x=10, y=10)
        
        facture=Frame(panierframe, width=400, height=600)
        facture.place(x=10, y=50)
        
        
        def recupereprix(event):
            try:
                   
                produitSelectionne = nomprod.get()
                
                curseur = self.connection.cursor()
                req = "SELECT ProduitPU FROM Produit WHERE ProduitNom = ?"
                curseur.execute(req, (produitSelectionne, ))
                valeur = curseur.fetchone()
                if valeur:
                    prixrecupere.set(valeur[0])
                    puprod.configure(state="readonly")
                    
                    quantite=int(qteprod.get())
                    if not quantite:
                        quantite=1
                        prix=float(prixrecupere.get())
                        total=quantite*prix
                        lbltotal.configure(text=f"Montant Total:\n {str(total)} GNF")
                    else:
                        prix=float(prixrecupere.get())
                        total=quantite*prix
                        lbltotal.configure(text=f"Montant Total:\n {str(total)} GNF")
                    
                else:
                    prixrecupere.set("Non trouvé")
            except Exception as e:
                pass
        
        ### Les champs de saisie
        
        
        prixrecupere=StringVar()
        
        reference=CTkEntry(venteinfo, width=150, placeholder_text="reference", corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black")
        reference.place(x=10, y=10)
        nomprod=CTkComboBox(venteinfo, width=150, corner_radius=0, height=40, values=["liste produits"], 
                         font=("arial", 15, "bold"), command=recupereprix)
        nomprod.place(x=10, y=70)
        
        
        
        def total(e):
            try:
                qte=int(qteprod.get())
                if type(qte)==type(""):
                    qte=1
                    prix=float(prixrecupere.get())
                    total=qte*prix
                    lbltotal.configure(text=f"Montant Total:\n {str(total)} GNF")
                else:
                    prix=float(prixrecupere.get())
                    total=qte*prix
                    lbltotal.configure(text=f"Montant Total:\n {str(total)} GNF")
            
            except:
                pass
                #messagebox.showerror("erreur", "veiller entrer une valeur numerique")
        
        
        qteprod=CTkEntry(venteinfo, width=150, placeholder_text="la quantite", corner_radius=0, height=40, 
                         font=("arial", 15, "bold"), placeholder_text_color="black")
        qteprod.place(x=10, y=120)
        
        qteprod.bind("<KeyRelease>", total)
        qteprod.bind("<Return>", total)
        
        datevente=CTkEntry(venteinfo, width=150, textvariable=Date, corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black")
        datevente.place(x=170, y=10)
        
        telclient=CTkEntry(venteinfo, width=150, placeholder_text="telephone client", corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black")
        telclient.place(x=170, y=70)
        puprod=CTkEntry(venteinfo, textvariable=prixrecupere,  width=150, placeholder_text="le prix unitaire", corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black", 
                          state="readonly")
        puprod.place(x=170, y=120)
        
        
        def recupereProduit():
            try:
                curseur=self.connection.cursor()
                req="select ProduitNom from Produit"
                curseur.execute(req)
                contenu=curseur.fetchall()
                contenu2=[]
                for valeurs in contenu:
                    for x in valeurs:
                        contenu2.append(x)
                nomprod.configure(values=contenu2)
                nomprod.set("produit")
                
                
                
                
            except:
                messagebox.showerror("erreur", "exception leve")
        recupereProduit()
        
        
        def videtablevente():
            for x in tablevente.get_children():
                tablevente.delete(x)
                
        def chargetablevente():
            try:
                videtablevente()
                curseur=self.connection.cursor()
                req="select VenteID, dateVente, infoVente from Vente"
                curseur.execute(req)
                donnees=curseur.fetchall()
                for x in donnees:
                    tablevente.insert("", "end", values=x)
            except:
                messagebox.showerror("erreur", "exception leve")
        self.qr_img = None  # Initialiser l'attribut pour stocker l'image du QR code   
        self.label_img = None  # Initialiser l'attribut pour stocker le label de l'image     
        def selectionnervente(event):
            try:
                ligne = tablevente.focus()
                valeurs = tablevente.item(ligne, 'values')
                print(valeurs)

                # Réinitialiser les champs
                nomprod.set("")
                qteprod.delete(0, END)
                telclient.delete(0, END)
                puprod.delete(0, END)
                reference.delete(0, END)
                Date.set("")

                # Remplir les champs avec les valeurs sélectionnées
                reference.insert(0, valeurs[0])
                Date.set(valeurs[1])
                telclient.insert(0, valeurs[2])

                # Afficher le QR code dans le cadre de la facture
                chemin = os.path.join("infovente", f"vente_{valeurs[0]}.png")
                if os.path.exists(chemin):
                    img1 = Image.open(chemin).resize((370, 300))
                    self.qr_img = ImageTk.PhotoImage(img1)

                    self.label_img = CTkLabel(facture, image=self.qr_img, text="")
                    self.label_img.place(x=5, y=55)
                else:
                    messagebox.showerror("Erreur", "QR code non trouvé.")
            

            except Exception as e:
                messagebox.showerror("Erreur", f"Exception levée : {e}")
        
        def effectuerVente():
            try:
                
                curseur = self.connection.cursor()
                
                          
                chargetablevente()

                # Récupérer ID et quantité du produit
                curseur.execute("SELECT produitID, ProduitQte FROM Produit WHERE ProduitNom = ?", (nomprod.get(),))
                resultat = curseur.fetchone()

                if not resultat:
                    messagebox.showerror("Erreur", "Produit non trouvé.")
                    return

                produitID, qte_dispo = resultat

                # Validation des champs
                if not nomprod.get().strip() or not qteprod.get().strip() or not telclient.get().strip():
                    messagebox.showwarning("Attention", "Tous les champs sont requis.")
                    return

                try:
                    qte_vendue = int(qteprod.get())
                    prix_unitaire = float(puprod.get())
                except ValueError:
                    messagebox.showerror("Erreur", "Quantité et prix doivent être numériques.")
                    return

                nouvellequantite = qte_dispo - qte_vendue
                if nouvellequantite < 0:
                    messagebox.showwarning("Stock insuffisant", "La quantité demandée dépasse le stock disponible.")
                    return
                
                
                
                
                # Insertion temporaire de la vente sans infoVente
                curseur.execute("""
                    INSERT INTO Vente(produitID, prixUnitaire, quantiteVendu, dateVente, clientTelephone, infoVente)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (produitID, prix_unitaire, qte_vendue, Date.get(), telclient.get(), ""))

                vente_id = curseur.lastrowid  # Récupère l'ID auto-incrémenté     
                
                # Création du dossier QR code si besoin
                
                if getattr(sys, 'frozen', False):
                    app_dir = os.path.dirname(sys.executable)
                else:
                    app_dir = os.path.dirname(os.path.abspath(__file__))

                dossier_qr = os.path.join(app_dir, "infovente")
                
                #dossier_qr = "infovente"
                if not os.path.exists(dossier_qr):
                    os.makedirs(dossier_qr)

                # Génération du QR code
                contenu_qr = (
                f"**** Information de la vente ****\n\n"
                f"Produit : {nomprod.get().upper()}\n"
                f"Quantité vendue : {qte_vendue}\n"
                f"Prix unitaire : {prix_unitaire}\n"
                f"Date de vente : {Date.get()}\n"
                f"Telephone Client : {telclient.get()}\n"
                )
                
                documents = Path.home() / "Documents" / "MonApp" / "infovente"
                documents.mkdir(parents=True, exist_ok=True)

                chemin = documents / f"vente_{vente_id}.png"
                
                #chemin = os.path.join(dossier_qr, f"vente_{vente_id}.png")
                qrcode.make(contenu_qr).save(chemin)
                
                curseur.execute("""
                UPDATE Vente SET infoVente = ? WHERE VenteID = ?
                """, (chemin, vente_id))
                
                self.connection.commit()
                # Affichage du QR code dans le cadre de la facture
                #img1= Image.open(chemin)
                #img1 = img1.resize((370, 500))  # Redimensionner l'image

                # Insertion de la vente dans la table reçu
                
                req="insert into Reçu(produit, qtevendu, pu, telclient, datevente) values(?, ?, ?, ?, ?)"
                curseur.execute(req, (nomprod.get().upper(), qte_vendue, prix_unitaire, telclient.get(), Date.get()))
                self.connection.commit()
                

                # Mise à jour de la quantité
                curseur.execute("UPDATE Produit SET ProduitQte = ? WHERE produitID = ?", (nouvellequantite, produitID))

                # Vérification de l'existence du client
                curseur.execute("SELECT 1 FROM Client WHERE clientTelephone = ?", (telclient.get(),))
                client_existe = curseur.fetchone()

                if not client_existe:
                    curseur.execute("""
                    INSERT INTO Client(clientNomPrenom, clientTelephone, clientAdresse)
                    VALUES (?, ?, ?)
                    """, ("", telclient.get(), ""))

                self.connection.commit()
                messagebox.showinfo("Succès", "Vente effectuée avec succès.")
                chargetablevente()

            except Exception as e:
                messagebox.showerror("Erreur", f"Exception levée : {e}")

        def supprimervente():
            try:
                curseur=self.connection.cursor()
                message=messagebox.askyesno(title="attention", message="voulez vous supprimer cet enregistrement")
                if message:
                    req=" delete from Vente where VenteID = ? "
            
                    curseur.execute(req, reference.get())
                    self.connection.commit()
                    chargetablevente()
                    messagebox.showinfo("info", "vente supprimer")
                    
                    ## supprimer le qrcode correspondant aussi
                    chemin = os.path.join("infovente", f"vente_{reference.get()}.png")
                    if os.path.exists(chemin):
                        os.remove(chemin)
                    else:
                        messagebox.showerror("Erreur", " Vente supprimer mais QR code non trouvé.")
                
            except:
                pass
            
        def filtrerpardate(e):
            entre=txtrecherche.get()
            
            if entre=="":
                pass
            else:
                videtablevente()
                try:
                    curseur=self.connection.cursor()
            
                    req = "SELECT VenteID, dateVente, infoVente FROM Vente WHERE dateVente like ?"
                    curseur.execute(req, ('%'+ entre.strip() + '%', ))
                    lignes=curseur.fetchall()
                    
                    
                    for x in lignes:
                        tablevente.insert("", "end", values=x)
                except Exception as e:
                    messagebox.showerror("Erreur", f"Exception levée : {e}")
        
        
        ## les boutons d'actions
        CTkButton(venteinfo, text="effectuer la vente", font=("arial", 15, "bold"), corner_radius=0, height=40, 
                  fg_color="blue", text_color="white", 
                  command=effectuerVente).place(x=370, y=10)
        CTkButton(venteinfo, text="supprimer la vente", font=("arial", 15, "bold"), corner_radius=0, height=40,
                  fg_color="orange", text_color="white", 
                  command=supprimervente).place(x=370, y=65)
        
        lbltotal=CTkLabel(venteinfo, text="", font=("arial", 15, "italic"),
                  text_color="red" 
                  )
        lbltotal.place(x=370, y=115)
        
        
        ### historique des ventes#########
        
        
        listevente=CTkFrame(self.framebody, width=700, height=400)
        listevente.place(x=30, y=250)
        CTkLabel(listevente, text="historique des ventes", width=150,
                 font=("arial", 25, "bold"), text_color="blue").place(x=100, y=10)
        
        
        
        
        txtrecherche=CTkEntry(listevente, width=340, height=40,
                              corner_radius=0, placeholder_text="filtrer par date de vente",
                              font=("arial", 15, "italic"), placeholder_text_color="black")
        txtrecherche.place(x=30, y=60)
        txtrecherche.bind("<KeyRelease>", filtrerpardate)
        
        
        self.i=Image.open("Icones/actualise.png")
        self.ri=self.i.resize((30, 30))
        self.pri=ImageTk.PhotoImage(self.ri)
        
        
        
        CTkButton(listevente, text="", hover=False, image=self.pri, width=30, height=35,  fg_color="beige", command=chargetablevente
                  ).place(x=580, y=60)
        
        
        vsb = ttk.Scrollbar(listevente, orient="vertical")
        vsb.place(x=635, y=100, height=232)
        # Créer le tableau avec une barre de défilement
        
        tablevente=ttk.Treeview(listevente, columns=("numVente", "dateVente", "infoVente"),
                                  show="headings", yscrollcommand=vsb.set)
        tablevente.heading("numVente", text="Vente N°")
        tablevente.heading("dateVente", text="la date de vente")
        tablevente.heading("infoVente", text="Les Informations sur la vente")
        
        
        ## l'evenement lier au selection du tableau
        tablevente.bind("<ButtonRelease-1>", selectionnervente)
        
        tablevente.place(x=30, y=100)
        vsb.config(command=tablevente.yview)
        
        chargetablevente()