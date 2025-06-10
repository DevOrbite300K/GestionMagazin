def reçu(self):
        self.initialiseFrameBody()
        
        prodinfo=LabelFrame(self.framebody, text="les informations de la vente a imprimer",
                            width=700, height=200, font=("arial", 15, "italic"), 
                            border=2)
        prodinfo.place(x=30, y=20)
        
        
        self.pi=Image.open("assets/icrecu.png")
        self.rpi=self.pi.resize((350, 200))
        self.pi1=ImageTk.PhotoImage(self.rpi)
        
        CTkLabel(self.framebody, text="", image=self.pi1).place(x=780, y=20)
        
        ### Les champs de saisie
        
        idreçu=CTkEntry(prodinfo, width=150, placeholder_text="N° reçu", corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black")
        idreçu.place(x=10, y=10)
        nomprod=CTkEntry(prodinfo, width=150, placeholder_text="nom du produit", corner_radius=0, height=40, 
                         font=("arial", 15, "bold"), placeholder_text_color="black")
        nomprod.place(x=10, y=70)
        
        qtevendu=CTkEntry(prodinfo, width=150, placeholder_text="La quantite vendu", corner_radius=0, height=40, 
                         font=("arial", 15, "bold"), placeholder_text_color="black")
        qtevendu.place(x=10, y=120)
        
        puprod=CTkEntry(prodinfo, width=150, placeholder_text="le prix unitaire", corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black")
        puprod.place(x=170, y=10)
        
        telclient=CTkEntry(prodinfo, width=150, placeholder_text="la quantite", corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black")
        telclient.place(x=170, y=70)
        
        datevendu=CTkEntry(prodinfo, placeholder_text="la date de vente",  width=150, corner_radius=0, height=40,
                          font=("arial", 15, "bold"))
        datevendu.place(x=170, y=120)
        
        
        def videtablereçu():
            for s in tablereçu.get_children():
                tablereçu.delete(s)
                
        def chargertablereçu():
            videtablereçu()  
            try:
                curseur=self.connection.cursor()
                req="select * from Reçu"
                curseur.execute(req)
                donnees=curseur.fetchall()
                for x in donnees:
                    tablereçu.insert("", "end", values=x)
                
            except:
                pass    
            
        def selectionlignereçu(e):
                ligne=tablereçu.focus()
                valeurs=tablereçu.item(ligne, 'values')
                
                idreçu.configure(state="normal")
                nomprod.configure(state="normal")
                qtevendu.configure(state="normal")
                puprod.configure(state="normal")
                telclient.configure(state="normal")
                datevendu.configure(state="normal")
                
                idreçu.delete(0, END)
                nomprod.delete(0, END)
                qtevendu.delete(0, END)
                puprod.delete(0, END)
                telclient.delete(0, END)
                datevendu.delete(0, END)
                # Remplir les champs avec les valeurs sélectionnées
                idreçu.insert(0, valeurs[0])
                nomprod.insert(0, valeurs[1])
                qtevendu.insert(0, valeurs[2])
                puprod.insert(0, valeurs[3])
                telclient.insert(0, valeurs[4])
                datevendu.insert(0, valeurs[5])
                
                idreçu.configure(state="readonly")
                nomprod.configure(state="readonly")
                qtevendu.configure(state="readonly")
                puprod.configure(state="readonly")
                telclient.configure(state="readonly")
                datevendu.configure(state="readonly")
                
        
        def rechercherreçu(e):
            try:
                 videtablereçu()
                 curseur=self.connection.cursor()
                 req="select * from Reçu where produit like ? or telclient like ? or datevente like ?"
                 curseur.execute(req, ("%"+ txtrecherche.get() +"%", "%"+ txtrecherche.get() +"%", "%"+ txtrecherche.get() +"%" ))
                 resultat=curseur.fetchall()
                 
                 for x in resultat:
                     tablereçu.insert("", "end", values=x)
            except:
                messagebox.showinfo("info", "aucun enregistrement trouvé")
                
        
        def imprimer():
            doc = FPDF()
            try:
                doc_dir = Path.home() / "Documents" / "MonApp" / "temp"
                doc_dir.mkdir(parents=True, exist_ok=True)

                barcode_path = doc_dir / "codebarre.png"
                pdf_path = doc_dir / "document.pdf"

                ean = barcode.get("code128", f"produit:{nomprod.get()} //quantite vendu: {qtevendu.get()} //prix unitaire: {puprod.get()} ", writer=ImageWriter())
                ean.save(str(barcode_path.with_suffix("")), options={"write_text": True, "font_size": 10})

                doc.add_page()
                doc.set_font("Arial", size=25)
                doc.cell(0, 10, text=f"Reçu N°{idreçu.get()} - {datevendu.get()}", ln=True, align="C")
                ...
                doc.image(str(barcode_path), x=10, w=190, h=70)
                doc.output(str(pdf_path))

                os.startfile(str(pdf_path))
                messagebox.showinfo("Info", "Le reçu a été imprimé avec succès")

            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'imprimer le reçu : {e}")
                
                ## **************** Les boutons d'actions ***************************
        
        CTkButton(prodinfo, text="imprimer le reçu", font=("arial", 15, "bold"), corner_radius=0, height=40, 
                  fg_color="green", text_color="white", 
                  command=imprimer).place(x=370, y=10)
        CTkButton(prodinfo, text="supprimer le reçu", font=("arial", 15, "bold"), corner_radius=0, height=40,
                  fg_color="orange", text_color="white").place(x=370, y=65)
        
        
        
        listeprod=CTkFrame(self.framebody, width=1100, height=400)
        listeprod.place(x=30, y=250)
        CTkLabel(listeprod, text="La Liste Des Reçus", width=150,
                 font=("arial", 35, "bold"), text_color="blue").place(x=350, y=10)
        
        txtrecherche=CTkEntry(listeprod, width=450, height=40,
                              corner_radius=0, placeholder_text="recherche par: produit vendu , telephone client, date vendu",
                              font=("arial", 15, "italic"), placeholder_text_color="black")
        txtrecherche.place(x=310, y=60)
        
        txtrecherche.bind("<KeyRelease>", rechercherreçu)
        txtrecherche.bind("<Return>", rechercherreçu)
        
        
        
        ## le tableau pour les Reçu
        
        vsb = ttk.Scrollbar(listeprod, orient="vertical")
        vsb.place(x=1080, y=130, height=235)
        
        tablereçu=ttk.Treeview(listeprod, columns=("idreçu", "nomprod", "qtevendu", "puprod", "telclient", "datevendu"),
                                  show="headings", yscrollcommand=vsb.set, selectmode="browse")
        vsb.config(command=tablereçu.yview)
        tablereçu.heading("idreçu", text="ID Reçu")
        tablereçu.heading("nomprod", text="Produit Vendu")
        tablereçu.heading("qtevendu", text="Qte Vendu")
        tablereçu.heading("puprod", text="PrixUnitaire")
        tablereçu.heading("telclient", text="Telephone Client")
        tablereçu.heading("datevendu", text="Date Vendu")
        
        tablereçu.column("idreçu", width=150)
        tablereçu.column("qtevendu", width=100)
        
        tablereçu.bind("<ButtonRelease-1>", selectionlignereçu)
        tablereçu.place(x=20, y=130)    
        chargertablereçu()