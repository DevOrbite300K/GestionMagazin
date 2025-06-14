from customtkinter import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import date

from pathlib import Path
import tempfile

import PIL
from PIL import ImageTk, Image

import qrcode
import os

from fpdf import FPDF
import barcode
from barcode.writer import ImageWriter

from config import *
class GESTION(CTk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.framebody=CTkFrame(self, border_width=0, width=870, fg_color="white")
        self.frametitle=CTkFrame(self, height=80, fg_color="darkblue", border_width=0, corner_radius=0)
        self.frameconn=CTkToplevel(self)
        
        self.connection= sqlite3.connect("stock.db")
        
        
        
        self.frameconn.protocol("WM_DELETE_WINDOW", self.quitter_app)
        
        
        
        
        self.frameauth=CTkFrame(self.frameconn, width=300, height=600, corner_radius=5, border_color="black")
        ##self.dash()
    
    
    
    
    def quitter_app(self):
            self.connection.close()
            self.destroy()
    ## La Fonction qui initialise le frame d'authentification
    
    def initialiseFrameAuth(self):
        for w in self.frameauth.winfo_children():
            w.destroy()
    
    ## La fonction qui gere l'inscription
    
    def inscription(self):
        self.initialiseFrameAuth()
        self.frameconn.geometry("400x600+400+50")
        
        self.frameconn.title("Formulaire2Inscription")
        self.frameconn.resizable(FALSE, FALSE)
        
        CTkLabel(self.frameauth, text="Inscription", font=("Arial", 25, "bold"),
                 ).place(x=20, y=10)
        
        #frame=CTkFrame(self.frameconn, width=300, height=300, corner_radius=5, border_color="black")
        self.frameauth.pack(pady=25)
        
        txtmail=CTkEntry(self.frameauth, width=250, placeholder_text="mail", font=("Arial", 25), height=50)
        txtmail.place(x=20, y=50, )
        
        txtpass=CTkEntry(self.frameauth, width=250, placeholder_text="password", font=("Arial", 25), height=50, show="*")
        txtpass.place(x=20, y=110)
        
        
        
        def inscription():
            try:
                curseur=self.connection.cursor()
                req="insert into Utilisateur(email, password) values(?, ?)"
                curseur.execute(req, (txtmail.get(), txtpass.get()))
                self.connection.commit()
                messagebox.showinfo("info", "Inscription reussie")
                
            except:
                pass
        
                
                
        
        CTkButton(self.frameauth, text="s'inscrire", width=250, height=50, border_width=0, text_color="white", font=("Arial", 15),
                  fg_color="green", command=inscription).place(x=20, y=180)
        CTkButton(self.frameauth, text="déjà inscrit ?", width=250, height=50, border_width=1, text_color="black", font=("Arial", 15),
                  fg_color="white", border_color="green", hover_color="white",
                  command=self.connexion).place(x=20, y=250)
    
        
    
    
    
    
    ## La Fonction De Connexion    
    def connexion(self):
        try:
            self.initialiseFrameAuth()
            self.frameconn.geometry("400x600+400+50")
            
            self.frameconn.title("Formulaire2Connexion")
            self.frameconn.resizable(FALSE, FALSE)
            
            CTkLabel(self.frameauth, text="Connexion", font=("Arial", 25, "bold"),
                    ).place(x=20, y=10)
            
            #frame=CTkFrame(self.frameconn, width=300, height=300, corner_radius=5, border_color="black")
            self.frameauth.pack(pady=25)
            
            txtmail=CTkEntry(self.frameauth, width=250, placeholder_text="mail", font=("Arial", 25), height=50)
            txtmail.place(x=20, y=50, )
            
            txtpass=CTkEntry(self.frameauth, width=250, placeholder_text="password", font=("Arial", 25), height=50, show="*")
            txtpass.place(x=20, y=110)
            
            
            def chargerUser():
                try:
                    
                    req="select email, password from Utilisateur"
                    curseur=self.connection.cursor()
                    curseur.execute(req)
                except:
                    pass
                
            
            def conn():
                try:
                    chargerUser()
                    curseur=self.connection.cursor()
                    
                    m=txtmail.get()
                    p=txtpass.get()
                    
                    curseur.execute("select email, password from Utilisateur where email=? and password=?", (m, p))
                    donnees=curseur.fetchone()
                    
                    if donnees:
                        messagebox.showinfo("info", f"bienvenue  {m}")
                        self.frameconn.destroy()
                        self.dash()
                    else:
                        messagebox.showerror("erreur", "donnees incorrect")
                        
                except:
                    pass
                try: 
                    pass
                    #self.frameconn.mainloop()
                except:
                    pass
                    
            
            CTkButton(self.frameauth, text="Connexion", width=250, height=50, border_width=0, text_color="white", font=("Arial", 15),
                    fg_color="green", command=conn).place(x=20, y=180)
            CTkButton(self.frameauth, text="pas inscrit ?", width=250, height=50, border_width=1, text_color="black", font=("Arial", 15),
                    fg_color="white", border_color="green", hover_color="white", 
                    command=self.inscription).place(x=20, y=250)
        
            #self.frameconn.mainloop()
            
        except:
            pass
        
    def dash(self):
        
        try:
                
            self.deiconify() 

            self.frameconn.destroy()
            self.geometry("1400x800+150+50")
            self.state("zoomed")
            self.title("Dashboard")
            self.resizable(FALSE, FALSE)
            
            framedash=CTkFrame(self, width=200, border_width=2, fg_color="darkblue", corner_radius=0)
            framedash.pack(side=LEFT, fill=Y, pady=0)
            CTkLabel(framedash, text="Admin Panel\nGestion", text_color="white", width=150, font=("Arial", 25, "bold")).place(x=20, y=10)
            
            self.frametitle.pack(fill=X, side=TOP)
            self.framebody.pack(fill=BOTH, expand=TRUE)
            
            
            CTkLabel(self.frametitle, text="GESTION DE\n STOCK MAGASIN", font=("Arial", 25, "bold"),
                    text_color="white").place(x=5, y=10)
            
            jour=date.today()
            jour2=jour.strftime("%d/%m/%Y")
            
            CTkLabel(self.frametitle, text=f"aujourd'hui: {jour2}", text_color="white",  font=("arial", 20, "italic")).place(x=500, y=30)
            
            self.pi=Image.open("assets/22.png")
            self.rpi=self.pi.resize((250, 90))
            self.pi1=ImageTk.PhotoImage(self.rpi)
            
            CTkLabel(self.frametitle, text="", image=self.pi1).place(x=950, y=0)
                
            ### creation des boutons de gestions.  avec les icones
            
            ### pour produit
            self.pi=Image.open("assets/icprod.png")
            self.rpi=self.pi.resize((70, 70))
            self.pi1=ImageTk.PhotoImage(self.rpi)
            btnProd=CTkButton(framedash, text="Produit", width=199, height=70, border_width=1, corner_radius=0, state="normal",
                            fg_color="darkblue", text_color="white", font=("arial", 25, "bold"), image=self.pi1, compound="right",
                            border_color="white", command=self.produit)
            btnProd.place(x=0, y=170)
            
            
            ## pour fournisseur
            self.pi=Image.open("assets/icfournn.png")
            self.rpi=self.pi.resize((80, 80))
            self.pi1=ImageTk.PhotoImage(self.rpi)
            btnfournisseur=CTkButton(framedash, text="Fourni", width=199, height=70, border_width=1, corner_radius=0, state="normal",
                            fg_color="darkblue", text_color="white", font=("arial", 25, "bold"), image=self.pi1, compound="right",
                            border_color="white", command=self.fournisseur)
            btnfournisseur.place(x=0, y=240)
            
            
            
            ## pour client
            self.pi=Image.open("assets/iccli.png")
            self.rpi=self.pi.resize((80, 80))
            self.pi1=ImageTk.PhotoImage(self.rpi)
            
            btnclient=CTkButton(framedash, text="Client", width=199, height=70, border_width=1, corner_radius=0, state="normal",
                            fg_color="darkblue", text_color="white", font=("arial", 25, "bold"), image=self.pi1, compound="right",
                            border_color="white", command=self.client)
            btnclient.place(x=0, y=310)
            
            
            ### pour vente 
            self.pi=Image.open("assets/icvenn.png")
            self.rpi=self.pi.resize((80, 80))
            self.pi1=ImageTk.PhotoImage(self.rpi)
            
            btncommande=CTkButton(framedash, text="Vente", width=199, height=70, border_width=1, corner_radius=0, state="normal",
                            fg_color="darkblue", text_color="white", font=("arial", 25, "bold"), image=self.pi1, compound="right",
                            border_color="white", command=self.vente)
            btncommande.place(x=0, y=380)
            
            ## pour reçu
            self.pi=Image.open("assets/icrecu3.png")
            self.rpi=self.pi.resize((80, 80))
            self.pi1=ImageTk.PhotoImage(self.rpi)
            
            btnreçu=CTkButton(framedash, text="Reçu", width=199, height=70, border_width=1, corner_radius=0, state="normal",
                            fg_color="chocolate", text_color="white", font=("arial", 25, "bold"), image=self.pi1, compound="right",
                            border_color="white", command=self.reçu)
            btnreçu.place(x=0, y=450)
            
            ## pour home
            self.pi=Image.open("assets/rapport2.png")
            self.rpi=self.pi.resize((80, 80))
            self.pi1=ImageTk.PhotoImage(self.rpi)
            
            btnrapport=CTkButton(framedash, text="Rapport", width=199, height=70, border_width=1, corner_radius=0, state="normal",
                            fg_color="black", text_color="white", font=("arial", 25, "bold"), image=self.pi1, compound="right",
                            border_color="white", command=self.home)
            btnrapport.place(x=0, y=540)
            
            
            
            def fermerApp():
                
                confirmer=messagebox.askyesno("attention", "voulez vous vraiment quitter l'application")
                if confirmer:
                    self.connection.close()
                    self.destroy()
                else:
                    pass
            ## bouton fermer
            self.pi=Image.open("assets/logout.png")
            self.rpi=self.pi.resize((50, 50))
            self.pi1=ImageTk.PhotoImage(self.rpi)
            
            CTkButton(framedash, text="", width=50, height=50, state="normal",
                            fg_color="darkblue", font=("arial", 25, "bold"), image=self.pi1, compound="right", hover=False,
                            command=fermerApp
                            ).place(x=65, y=680)
            
            
            
            
            
            
            self.home()
            
            
            self.mainloop()
        
            
        except:
            pass
 
    def initialiseFrameBody(self):
        for w in self.framebody.winfo_children():
            w.destroy()
    
    #### home
    
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
        
    
    
    ## la Gestion des produits #############################################################################################
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
        
        self.pi=Image.open("assets/icprod2.png")
        self.rpi=self.pi.resize((350, 200))
        self.pi1=ImageTk.PhotoImage(self.rpi)
        
        CTkLabel(self.framebody, text="", image=self.pi1).place(x=780, y=20)
        
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
        self.i=Image.open("Icones/actualise.png")
        self.ri=self.i.resize((30, 30))
        self.pri=ImageTk.PhotoImage(self.ri)
        
        CTkButton(listeprod, text="", hover=False, image=self.pri, width=30, height=35,  fg_color="beige", command=chargerproduit
                  ).place(x=770, y=60)
        
        
        
        
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
        
     
     
    ## La Gestion DES FOURNISEURS ########################################################################################
    def fournisseur(self):
        self.initialiseFrameBody()       
        
        fourinfo=LabelFrame(self.framebody, text="veiller saisir les information du fournisseur",
                            width=700, height=200, font=("arial", 15, "italic"), 
                            border=2)
        fourinfo.place(x=30, y=20)
        
        idfour=CTkEntry(fourinfo, width=150, placeholder_text="identifiant", corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black")
        idfour.place(x=10, y=10)
        nomfour=CTkEntry(fourinfo, width=150, placeholder_text="nom complet", corner_radius=0, height=40, 
                         font=("arial", 15, "bold"), placeholder_text_color="black")
        nomfour.place(x=10, y=70)
        
        telfour=CTkEntry(fourinfo, width=150, placeholder_text="Tel:", corner_radius=0, height=40, 
                         font=("arial", 15, "bold"), placeholder_text_color="black")
        telfour.place(x=10, y=120)
        
        adfour=CTkEntry(fourinfo, width=150, placeholder_text="Adresse:", corner_radius=0, height=40,
                          font=("arial", 15, "bold"), placeholder_text_color="black")
        adfour.place(x=170, y=10)
        
        self.pi=Image.open("assets/icfourn.jpg")
        self.rpi=self.pi.resize((350, 200))
        self.pi1=ImageTk.PhotoImage(self.rpi)
        
        CTkLabel(self.framebody, text="", image=self.pi1).place(x=780, y=20)
        
        
        
        
        
        listefour=CTkFrame(self.framebody, width=1100, height=400)
        listefour.place(x=30, y=250)
        CTkLabel(listefour, text="La Liste Des Fournisseur", width=150,
                 font=("arial", 35, "bold"), text_color="blue").place(x=350, y=10)
        
        def charger():
            
            try:
                
                videtableau()
                curseur=self.connection.cursor()
                req="""select * from Fournisseur """
                curseur.execute(req)
                lignes=curseur.fetchall()
                
                for x in lignes:
                    tablefournisseur.insert("", "end", values=x)
            except:
                pass
        
        def rechercher(e):
            videtableau()
            try:
                curseur=self.connection.cursor()
            
                req="select *  from Fournisseur where fournisseurNomPrenom like ? or fournisseurTelephone like ? or fournisseurAdresse like ?"
                curseur.execute(req, ('%'+ txtrecherche.get().upper() + '%', '%'+ txtrecherche.get().upper() + '%', '%'+ txtrecherche.get().upper() + '%'))
                lignes=curseur.fetchall()
                
                
                for x in lignes:
                    tablefournisseur.insert("", "end", values=x)
                
            except:
                messagebox.showerror("erreur", "exception leve")
                
            
        
        
        txtrecherche=CTkEntry(listefour, width=450, height=40,
                              corner_radius=0, placeholder_text="recherche par: nom, adresse",
                              font=("arial", 15, "italic"), placeholder_text_color="black")
        txtrecherche.place(x=310, y=60)
        
        txtrecherche.bind("<KeyRelease>", rechercher)
        
        self.i=Image.open("Icones/actualise.png")
        self.ri=self.i.resize((30, 30))
        self.pri=ImageTk.PhotoImage(self.ri)
        
        
        
        CTkButton(listefour, text="", hover=False, image=self.pri, width=30, height=35,  fg_color="beige", command=charger
                  ).place(x=770, y=60)
        
        
        
        
        
        ### Gestions des actions sur les fournisseur
        ## vider le tableau
        def videtableau():
            for s in tablefournisseur.get_children():
                tablefournisseur.delete(s)
        
        
            
            
            
        ## La methode d'ajout d'un nouveau fournisseur
        def ajouter():
            ## vide la liste des fournisseur avant d'inserer un enregistrement
            try:
                
                curseur=self.connection.cursor()
                req=""" insert into Fournisseur(fournisseurNomPrenom, fournisseurTelephone, fournisseurAdresse)
                    values(?, ?, ?)
                    """
                if nomfour.get()=="" or telfour.get()=="" or adfour.get()=="":
                
                    messagebox.showwarning("Attention", "champs requis")
                else:
                    curseur.execute(req, (nomfour.get().upper(), telfour.get().upper(), adfour.get().upper()))
                    self.connection.commit()
                    charger()
                    
                    messagebox.showinfo("info", "fournisseur ajouté")
                    
            except:
                    messagebox.showerror("erreur", "doublons interdit sur le numero")
            
                
            
            
           
        def modifier():
            
            curseur=self.connection.cursor()
            
            
            curseur.execute("update Fournisseur  set fournisseurNomPrenom =?, fournisseurTelephone =?, fournisseurAdresse=? where fournisseurID =?", (nomfour.get().upper(), telfour.get().upper(), adfour.get().upper(), idfour.get()))
            self.connection.commit()
            charger()
            
        def supprimer():
            
            try:
                
                curseur=self.connection.cursor()
            
                message=messagebox.askyesno(title="attention", message="voulez vous supprimer cet enregistrement")
                if message:
                    req=" delete from Fournisseur where fournisseurID = ? "
            
                    curseur.execute(req, idfour.get())
                    self.connection.commit()
                    charger()
                
            except:
                pass
        
        
        ## la methode permettant de selectionner une ligne dans la liste des fournisseurs
        def selectFournisseur(e):
            
            idfour.delete(0, END)
            nomfour.delete(0, END)
            telfour.delete(0, END)
            adfour.delete(0, END)
               
            
            ligne=tablefournisseur.focus()
            valeurs=tablefournisseur.item(ligne, 'values')
            
            idfour.insert(0, valeurs[0])
            nomfour.insert(0, valeurs[1])
            telfour.insert(0, valeurs[2])
            adfour.insert(0, valeurs[3])
            
            
        
        ## le tableau pour les fournisseurs
        
        vsb = ttk.Scrollbar(listefour, orient="vertical")
        vsb.place(x=950, y=130, height=235)
        
        tablefournisseur=ttk.Treeview(listefour, columns=("fournisseurID", "nomcomplet", "telephone", "adresse"),
                                  show="headings", yscrollcommand=vsb.set, selectmode="browse")
        vsb.config(command=tablefournisseur.yview)
        tablefournisseur.heading("fournisseurID", text="FournisseurID")
        tablefournisseur.heading("nomcomplet", text="Nom et Prenom")
        tablefournisseur.heading("telephone", text="Telephone")
        tablefournisseur.heading("adresse", text="Adresse")
        
        #tablefournisseur.column("FournisseurID", width=150)
        
        tablefournisseur.place(x=140, y=130)
        
        tablefournisseur.bind("<ButtonRelease-1>", selectFournisseur) 
        
        charger()
        ### ****** les boutons pour fournisseur ***********
          
        CTkButton(fourinfo, text="Ajouter", font=("arial", 15, "bold"), corner_radius=5, height=40, border_width=1,
                  fg_color="white", text_color="black", border_color="green", 
                  command=ajouter).place(x=370, y=10)
        CTkButton(fourinfo, text="Modifier", font=("arial", 15, "bold"), corner_radius=5, height=40, border_width=1,
                  fg_color="white", text_color="black", border_color="orange",
                  command=modifier).place(x=370, y=65)
        CTkButton(fourinfo, text="Supprimer", font=("arial", 15, "bold"), corner_radius=5, height=40, border_width=1,
                  fg_color="white", text_color="black", border_color="red", 
                  command=supprimer).place(x=370, y=120)
        
        
        
    
    
    
    
    ### Gestions des Ventes ##########################################################################################
    
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
        
        #tablevente.bind("<ButtonRelease-1>", selectFournisseur) 
    
    
    
    
    ### Gestion des Clients ################################################################################################
      
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
        
        
    
    
    ##### Gestions des reçus ############################################################################################
    
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