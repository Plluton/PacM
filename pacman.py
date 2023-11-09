from tkinter import *
import random


#Dictionnaire des objets animés
def creer_acteur(nom, role, x, y, costume, vies, vitesse):
    return {
        'nom' : nom,
        'role' : role ,
        'x' : x,
        'y' : y,
        'costume' : costume,
        'vies' : vies,
        'vitesse' : vitesse,
        'ax' : 0,
        'ay' : 0,
        'direction' : '',
        'etat' : 'vivant'
        }
    

#Creation des objets, de leur position et de comptage
def dessiner_labyrinte(mode):
    largeur = len(cases)
    global x_depart
    global y_depart
    global compteur_pastilles
    for i in range(0, largeur):
        liste = cases[i]
        longueur = len(liste)
        for j in range(0, longueur):
            if mode == 1 :
                if liste[j] == 1:
                    canvas.create_rectangle(j*20, i*20, j*20+20, i*20+20, fill='navy', outline='navy', width=1)
            if mode == 2:
                if liste[j] == 4:
                    x_depart = j*20
                    y_depart = i*20
                if liste[j] == 2:
                    canvas.create_oval(j*20+8, i*20+8, j*20+12, i*20+12, fill='silver', tags=('pacdot'))
                    compteur_pastilles = compteur_pastilles + 1
                if liste[j] == 3:
                    canvas.create_oval(j*20+4, i*20+4, j*20+16, i*20+16, fill='pink', tags=('pacgum'))
                    compteur_pastilles = compteur_pastilles + 1

def start_game():
    
    text_fin1 = canvas.create_text(230-2, 190-2, text='Game Over', fill='black', font='Modern 30 bold')
    text_fin2 = canvas.create_text(230+2, 190+2, text='Game Over', fill='black', font='Modern 30 bold')
    text_fin3 = canvas.create_text(230, 190, text='Game Over', fill='White', font='Modern 30 bold')
    text_fin4 = canvas.create_text(230, 230, text='Press Enter to start', fill='White', font='Modern 15 bold')  
    
    
    def attendre():
        global vitesse_du_jeu
        global compteur_points
        global level
        if 'Return' in pacman['direction']:
            canvas.delete(text_fin1)
            canvas.delete(text_fin2)
            canvas.delete(text_fin3)
            canvas.delete(text_fin4)
            pacman['vies'] = 3
            etiquette_vie['text'] = 'Vies: ' + str(pacman['vies'])               
            vitesse_du_jeu = 20
            compteur_points = 0
            level = 1
            etiquette_level['text'] = 'Level: ' + str(level)
            
            animer_pacman(pacman, 0, 1)
            deplacement()
            return
        canvas.after(10, attendre)
        
    attendre()
     
        

#Déplacement géneral
def deplacement():
    global vitesse_du_jeu
    mouvement(pacman)
    manger(pacman)
    for m in monstres:
        mouvement(m)
        deplacement_monstre(m)
        collision_pacman_monstres(m)
        animer_monstre(m)
    gestion_de_la_peur()
    if pacman['vies'] == 0:
        start_game()
        return
    canvas.after(vitesse_du_jeu, deplacement)
    
#Mouvement d'un acteur
def mouvement(acteur):
    x_case = int(acteur['x']/20)
    y_case = int(acteur['y']/20)
    global angle
    if y_case*20 == int(acteur['y']) and x_case*20 == int(acteur['x']):

        if cases[y_case][x_case+1] != 1 and acteur['direction'] == 'Right':
            acteur['ax'] = 1
            acteur['ay'] = 0
        if cases[y_case][x_case-1] != 1 and acteur['direction'] == 'Left':
            acteur['ax'] = -1
            acteur['ay'] = 0
        if cases[y_case-1][x_case] != 1 and acteur['direction'] == 'Up':
            acteur['ay'] = -1
            acteur['ax'] = 0
        if cases[y_case+1][x_case] != 1 and acteur['direction'] == 'Down':
            acteur['ay'] = 1
            acteur['ax'] = 0
            
        if cases[y_case][x_case+acteur['ax']] == 1:
            acteur['ax'] = 0
        if cases[y_case+acteur['ay']][x_case] == 1:    
            acteur['ay'] = 0

    acteur['x'] += acteur['ax'] * acteur['vitesse']        
    acteur['y'] += acteur['ay'] * acteur['vitesse']
               

def animer_pacman(acteur, angle_tempo, sens):
    angle = {'Left' : 180,
             'Right' : 0,
             'Up' : 90,
             'Down' : 270
             }
    
    angle_tempo += sens
    if angle_tempo >= 30:
        sens = - 1
    if angle_tempo <= 0:
        sens = + 1
        
    if acteur['direction'] in angle:
        start = angle_tempo + angle[acteur['direction']]
    else:
        start = angle_tempo
        
    extent = 360 - 2 * angle_tempo
    canvas.coords(acteur['costume'], acteur['x'], acteur['y'], acteur['x']+20, acteur['y']+20)
    canvas.itemconfigure(acteur['costume'], start=start, extent=extent )
    if pacman['vies'] == 0:
        return
    canvas.after(10, animer_pacman, acteur, angle_tempo, sens)
       
def gestion_de_la_peur():
    global manger_monstre
    
    if manger_monstre > 0:
        manger_monstre -= 1
        if manger_monstre <= 100:
            if manger_monstre % 10 == 0:
                for m in monstres:
                    if m['etat'] != 'mort':
                        canvas.itemconfigure(m['costume'], image=image_peur2)
            if manger_monstre % 10 == 5:
                for m in monstres:
                    if m['etat'] != 'mort':
                        canvas.itemconfigure(m['costume'], image=image_peur)
        if manger_monstre == 0:
            for m in monstres:
                if m['etat'] != 'mort':
                    canvas.itemconfigure(m['costume'], image=m['nom'])
                    m['vitesse'] = 1
                
def animer_monstre(acteur):
    canvas.coords(acteur['costume'], acteur['x'], acteur['y'])
    

# Déplacement Pacman
def deplacement_pacman(event):
    global compteur_pastilles
    pacman['direction'] = event.keysym
    if event.keysym == 'n':
        compteur_pastilles = 0

# Déplacement Monstre
def deplacement_monstre(acteur):
    choix = [] #liste des choix possible pour les directions du monstre
    x_case = int(acteur['x']/20)
    y_case = int(acteur['y']/20)

    if acteur['etat'] == 'mort' and x_case == 11 and y_case == 10:
        # Le fantôme est mort et a atteint sa base, réinitialiser sa position et état
        acteur['x'] = 11 * 20
        acteur['y'] = 10 * 20
        acteur['etat'] = 'vivant'
        canvas.itemconfigure(acteur['costume'], image=acteur['nom'])
        return    
    
    if y_case*20 == int(acteur['y']) and x_case*20 == int(acteur['x']):
        
        # ajouter les directions possibles dans choix
        if cases[y_case][x_case+1] != 1: 
            choix.append('Right')
        if cases[y_case][x_case-1] != 1:
            choix.append('Left')
        if cases[y_case-1][x_case] != 1:
            choix.append('Up')
        if cases[y_case+1][x_case] != 1:
            choix.append('Down')
            
        # retirer de retourner en arrière
        if acteur['direction'] == 'Right' and 'Left' in choix:
            choix.remove('Left')
        if acteur['direction'] == 'Left' and 'Right' in choix:
            choix.remove('Right')
        if acteur['direction'] == 'Up' and 'Down' in choix:
            choix.remove('Down')
        if acteur['direction'] == 'Down' and 'Up' in choix:
            choix.remove('Up')
         
        
        if acteur['etat'] == 'vivant' and 0 == random.choice([0, 1, 2]):
            if x_case > int(pacman['x']/20) and 'Right' in choix and len(choix) > 1:
                choix.remove('Right')
            if x_case < int(pacman['x']/20) and 'Left' in choix and len(choix) > 1:
                choix.remove('Left') 
            if y_case > int(pacman['y']/20) and 'Down' in choix and len(choix) > 1:
                choix.remove('Down')           
            if y_case < int(pacman['y']/20) and 'Up' in choix and len(choix) > 1:
                choix.remove('Up')

                
        # Retour a la base d'un fantome avec l'etat "mort"
        if acteur['etat'] == 'mort':
            if x_case > 11 and 'Left' in choix:
                acteur['direction'] = 'Left'
                return
            if x_case < 11 and 'Right' in choix:
                acteur['direction'] = 'Right'
                return
            if y_case > 10 and 'Up' in choix:
                acteur['direction'] = 'Up'
                return
            if y_case < 10 and 'Down' in choix:
                acteur['direction'] = 'Down'
                return
            
            if x_case == 11 and y_case == 10:
                canvas.itemconfigure(acteur['costume'], image=acteur['nom'])
                acteur['vitesse'] = 1
                acteur['etat'] = 'vivant'

        # choisir une direction possible au hasard
        acteur['direction'] = random.choice(choix)

def manger(pacman):
    global manger_monstre
    global compteur_points
    global compteur_pastilles
    liste_items = canvas.find_overlapping(pacman['x'], pacman['y'], pacman['x']+20, pacman['y']+20) # Renvoie une liste d'items
    for c in liste_items:
        if 'pacdot' in canvas.gettags(c):
            compteur_points += 10
            compteur_pastilles -= 1
            etiquette_points['text'] = 'Points: ' + str(compteur_points) 
            canvas.delete(c)
        if 'pacgum' in canvas.gettags(c):
            compteur_points += 100
            compteur_pastilles -= 1
            etiquette_points['text'] = 'Points: ' + str(compteur_points) 
            canvas.delete(c)
            manger_monstre = 500
            for m in monstres:
                if m['etat'] != 'mort':
                    canvas.itemconfigure(m['costume'], image=image_peur)
                    m['vitesse'] = 0.7
    if compteur_pastilles == 0:
        fin_de_partie('win')

def fin_de_partie(mode):
    global vitesse_du_jeu
    global manger_monstre
    global level
    
    # Ce qui se passe dans tous les cas
    # Sur les acteurs
    for m in monstres:    
        m['vitesse'] = 1
        m['etat'] = 'vivant'
        m['x'] = 11 * 20
        m['y'] = 10 * 20
        m['ax'] = 0
        m['ay'] = 0
        canvas.itemconfigure(m['costume'], image=m['nom'])
        m['direction'] = ''
    
    pacman['direction'] = ''
    pacman['x'] = x_depart
    pacman['y'] = y_depart
    pacman['ax'] = 0
    pacman['ay'] = 0
    
    # sur les variable globales
    manger_monstre = 0
    
    # Ce qui se passe quand on gagne
    if mode == 'win':
        level += 1
        etiquette_level['text'] = 'Level: ' + str(level)
        if vitesse_du_jeu > 6:
            vitesse_du_jeu -= 2
            
        dessiner_labyrinte(2)
        
    # En cas d'échec
    if mode == 'lose':
        pacman['vies'] = pacman['vies'] - 1
        etiquette_vie['text'] = 'Vies: ' + str(pacman['vies'])
       
            
# Collision pacman/monstres
def collision_pacman_monstres(m):
    global manger_monstre
    global compteur_points
    x_case_p = int(pacman['x']/20) # x_case de pacman # enventuellement prendre le centre de la case
    y_case_p = int(pacman['y']/20) # y_case de pacman
    x_case_m = int(m['x']/20) # x_case des monstres
    y_case_m = int(m['y']/20) # y_case des monstres
    
    if x_case_p == x_case_m and y_case_p == y_case_m: 
        if manger_monstre == 0:
            fin_de_partie('lose') 
        else:
            if m['etat'] != 'mort':
                compteur_points += 1000
                etiquette_points['text'] = 'Points: ' + str(compteur_points)     
                canvas.itemconfigure(m['costume'], image=image_yeux)
                m['etat'] = 'mort'
                m['vitesse'] = 2
    


# Création d'un canevas
fenetre = Tk()
fenetre.title("PacMan")
canvas = Canvas(fenetre, width=460, height=460, bg="black")
canvas.pack(padx=20, pady=40)

# Création des compteurs
etiquette_vie = Label(fenetre, text='Vies: 0', font='Modern 18 bold',
                   fg='black', height=1, width=8)
etiquette_vie.place(x=0, y=503)

etiquette_points = Label(fenetre, text='Points: 0', font='Modern 18 bold',
                   fg='black', height=1, width=20)
etiquette_points.place(x=95, y=503)

etiquette_level = Label(fenetre, text='Level: 1', font='Modern 18 bold',
                   fg='black', height=1, width=8)
etiquette_level.place(x=380, y=503) 

# Variables globales
compteur_pastilles = 0
compteur_points = 0
x_depart = 0
y_depart = 0
angle = 20
manger_monstre = 0
vitesse_du_jeu = 20
level = 1

# Création des cases
cases = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
         [1,3,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,3,1],
         [1,2,1,1,1,2,1,1,1,1,2,1,2,1,1,1,1,2,1,1,1,2,1],
         [1,2,1,1,1,2,1,1,1,1,2,1,2,1,1,1,1,2,1,1,1,2,1],
         [1,2,2,2,2,2,2,2,2,2,2,3,2,2,2,2,2,2,2,2,2,2,1],
         [1,2,1,1,1,2,1,2,1,1,1,1,1,1,1,2,1,2,1,1,1,2,1],
         [1,2,2,2,2,2,1,2,2,2,2,1,2,2,2,2,1,2,2,2,2,2,1],
         [1,2,1,1,1,2,1,1,2,1,2,2,2,1,2,1,1,2,1,1,1,2,1],
         [1,3,2,2,1,2,1,1,2,1,1,2,1,1,2,1,1,2,1,2,2,3,1],
         [1,1,1,2,1,2,1,1,2,1,0,0,0,1,2,1,1,2,1,2,1,1,1],
         [1,1,1,2,1,3,2,2,2,1,0,0,0,1,2,2,2,3,1,2,1,1,1],
         [1,1,1,2,1,2,1,1,2,1,1,1,1,1,2,1,1,2,1,2,1,1,1],
         [1,2,2,2,1,2,1,2,2,2,2,4,2,2,2,2,1,2,1,2,2,2,1],
         [1,2,1,1,1,2,1,2,1,1,1,1,1,1,1,2,1,2,1,1,1,2,1],
         [1,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,1],
         [1,2,1,1,1,2,1,1,1,1,2,1,2,1,1,1,1,2,1,1,1,2,1],
         [1,2,2,2,1,2,2,2,2,2,2,3,2,2,2,2,2,2,1,2,2,2,1],
         [1,1,1,2,1,2,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,1,1],
         [1,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,1],
         [1,3,1,1,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,1,1,3,1],
         [1,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,2,1,2,2,2,2,1],
         [1,1,1,1,2,2,2,1,1,1,2,3,2,1,1,1,2,2,2,1,1,1,1],
         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
         
         

dessiner_labyrinte(1)
dessiner_labyrinte(2)


# Création de pacman
fenetre.bind("<Key>", deplacement_pacman)
pacman = creer_acteur('pacman', 'joueur', x_depart, y_depart, canvas.create_arc(0, 0, 20, 20, fill='gold', style='pieslice', start=20, extent=320), 0, 2)

# Création monstres
image_blinky = PhotoImage(file = "blinky.png")
image_pinky = PhotoImage(file = "pinky.png")
image_inky = PhotoImage(file = "inky.png")
image_clyde = PhotoImage(file = "clyde.png")
image_peur = PhotoImage(file = "peur.png")
image_peur2 = PhotoImage(file = "peur2.png")
image_yeux = PhotoImage(file = "eyes.png")
monstres = [
    creer_acteur(image_blinky, 'fantome', 11*20, 10*20, canvas.create_image(0, 0, anchor = NW, image = image_blinky), 3, 2),
    creer_acteur(image_pinky, 'fantome', 10*20, 10*20, canvas.create_image(0, 0, anchor = NW, image = image_pinky), 3, 2),
    creer_acteur(image_inky, 'fantome', 12*20, 10*20, canvas.create_image(0, 0, anchor = NW, image = image_inky), 3, 2),
    creer_acteur(image_clyde, 'fantome', 11*20, 9*20, canvas.create_image(0, 0, anchor = NW, image = image_clyde), 3, 2),
]

animer_pacman(pacman, 0, 1)
deplacement()
fenetre.mainloop()