#import
import random
import matplotlib.pyplot as plt
import math

#Variables générale
# compteur
j = 0

# compteur de génération
generation = 0

# paramètres de l'algorithme 
nbGenerationArret =500
nPop = 5000
objectif = 300

#Création de la premièere génération
def initialisation(j,nPop):
    tabAll = []
    while (j <= nPop):
        #Gene
        #angle
        a = 45

        #longueur section bras
        Lb =random.randint(1,100)

        #base section bras
        b =random.randint(1,100)

        #hauteur section bras
        h =random.randint(1,100)

        #longueur corde
        Lc =random.randint(1,100)

        #longueur de la fleche
        Lf = random.randint(1,100)

        #masse volumique de la fleche
        p = random.randint(200,20000)

        #module de young du matérieu de l'arc
        E = random.randint(1,1220)

        #Coefficient de poisson du matériau de l'arc
        v =round(random.uniform(0.10,0.49),2)

        #gravité terre 9,81m.s−2, lune 1,62m.s-2, jupiter 24,80.s-2
        g =9.81
        
        tabIndividu = [a,Lb,b,h,Lc,Lf,p,E,v,g]
        tabAll.append(tabIndividu)
        j=j+1
    return tabAll

#evaluation d'un individu
def evaluation(a,Lb,b,h,Lc,Lf,p,E,v,g):
    if limites(a,Lb,b,h,Lc,Lf,p,E,v,g) != True:
        return [0,0]   

    #ressort
    K=(E/(1-2*v))/3

    #Longueur à vide
    Lv = math.sqrt(math.pow(Lb,2)-math.pow(Lc,2))/2

    #Longueur du déplacement
    Ld =Lf-Lv

    #Masse projectile
    Mp = p*b*h*Lf

    #Vélocité
    V = math.sqrt((K*math.pow(Ld,2))/Mp)

    #Portée
    d =(math.pow(V,2)/g)*math.sin(2*math.radians(a))

    #Energie impact
    Ec = (1/2)*Mp*math.pow(V,2)

    #Equivalence joule
    EnergieTnt = Ec/4184
    return [d, int(EnergieTnt)]

# gestion des limites physiques
def limites(a,Lb,b,h,Lc,Lf,p,E,v,g):
    # #Limites
    # #moment quadratique du bras
    # I = (b*math.pow(h,3))/12

    # #Force de traction
    # F = k*Ld

    # f = (F*math.pow(Lb,3))/(48*E*I)
    #Bras < à corde
    testBrasCorde = Lb - Lc

    #une valeur = 0
    testValeur = a*Lb*b*h*Lc*Lf*p*E*v*g
    
    if testBrasCorde < 0 or testValeur == 0:
        return False
    else:
        return True

#Création de la nouvelle génération
def selection(tabPopulationIni):
    taille=len(tabPopulationIni)
    tabPopulation=[]
    while len(tabPopulation) < taille:
        # On défini 2 arènes
        arene1=[]
        arene2= []
        # on remplis chaques arènes de 4 combatants
        for i in range(4):
            # paramètres pour définir lorsque les arènes sont pleines 
            test = 0
            cpt=0
            while test == 0:
                # Séléction de 2 individus tiré aléatoirement parmis la population
                individu=tabPopulationIni[random.randint(0,taille-1)]
                individu2=tabPopulationIni[random.randint(0,taille-1)]
                # On vérifie si les individus on déja été tiré
                if individu not in arene1 and individu2 not in arene2:
                    test =  1
                # Protection anti boucle infini en cas de clones
                if cpt == taille/4:
                    test = 1
                cpt=cpt+1
            arene1.append(individu)
            arene2.append(individu2)
        #On récupère les gagnants
        parent1=fight(arene1)
        parent2=fight(arene2)

        # On envoie les parents s'accoupler
        tabPopulation = croisement(parent1,parent2,tabPopulation)
    return tabPopulation


# L'arene permettant de récuperer le meilleur individu
def fight(arene):
    nbCombat=2
    j=0
    final=[]
    # On programme les rounds
    while j < nbCombat :
        combat=[]
        for i in range(0,2):
            test = False
            cpt=0
            while test == False:
                combatant = arene[random.randint(0,3)]
                # on selection un individu parmis les 4
                if len(combat)==1 and combatant == combat[0]:
                    combatant = arene[random.randint(0,3)]
                else:
                    test = True
                 # protection anti boucle infini
                if cpt == 30:
                    test = True
                cpt=cpt+1
            combat.append(combatant)

        # Comparaison des notes demi final
        noteMax=0
        gagnant=[]
        for individu in combat:
            if individu[2] >= noteMax:
                noteMax = individu[2]
                gagnant=individu
        final.append(gagnant)

        j=j+1

    #Comparaison des finaliste 
    noteMax=0
    champion=[]
    for individu in final:
        if individu[2] >= noteMax:
            noteMax = individu[2]
            champion=individu
    return champion


#croisement des gênes parents
def croisement(parent1,parent2,tabPopulation):
    #taux de variation de la hauteur fixé entre 50 70%
    tH = 70
    chance=random.randint(0,100)
    if chance > tH:
        coupe=random.randint(1,5)
    else:
        coupe=4
    parent1=parent1[0]
    parent2=parent2[0]
    enfant1 = parent1[0:coupe]+parent2[coupe:10]
    tabPopulation.append(mutation(enfant1))

    enfant2 = parent2[0:coupe]+parent1[coupe:10]
    enfant2[coupe]=parent1[coupe]
    tabPopulation.append(mutation(enfant2))

    return tabPopulation

#mutation
def mutation(enfant):
    #taux de mutation fixé entre 0,1% à 10%
    tM =3
    chance=random.randint(0,100)
    if chance < tM:
        gene=random.randint(1,8)
        if gene == 6:
            enfant[gene] = random.randint(200,20000)
        elif gene == 7:
             enfant[gene] = random.randint(1,1220)
        elif gene == 8:
            enfant[gene] =round(random.uniform(0.10,0.49),2)
        else:
            enfant[gene]=random.randint(1,100)
    return enfant

def moyenne_liste(l):
    return(sum(l)/len(l))
    

def variance_liste(l):
    m = moyenne_liste(l)
    return(sum([(x-m)**2 for x in l])/len(l))

#Algo général
tabVariance = []
maxNote = 0
resultatTab=[]
tabMoyenne = []
moyenneResultat = []
tabEval= []
best= []
while j <= nbGenerationArret:
    tabNote=[0]
    j=j+1
    if generation == 0:
        print("Création de la population originel")
        tabPopulation = initialisation(j,nPop)
        print("Fonction d'évaluation")
        for individu in tabPopulation:
            resultat,energie= evaluation(individu[0],individu[1],individu[2],individu[3],individu[4],individu[5],individu[6],individu[7],individu[8],individu[9])
            note=int((abs(resultat)/objectif)*100)
            if note <= 0:
                note=1
            elif note >= 200:
                note = 5
            elif note > 100 :
                note= 100-(note-100)
            tabEval.append([individu,resultat,energie,note])
            tabNote.append(note)
            resultatTab.append(round(resultat,0))
            if note > maxNote:
                maxNote=note
                best= [individu,int(resultat), energie,note,"generation ",j-1]
    else:
        print("generation suivante")
        tabPopulation = selection(tabEval)
        tabEval=[]
        for individu in tabPopulation:
            resultat,energie= evaluation(individu[0],individu[1],individu[2],individu[3],individu[4],individu[5],individu[6],individu[7],individu[8],individu[9])
            note=int((abs(resultat)/objectif)*100)
            if note == 0:
                note=1
            elif note >= 200:
                note = 5
            elif note > 100:
                note= 100-(note-100)
            tabEval.append([individu,resultat,note])
            tabNote.append(note)
            resultatTab.append(round(resultat,0))
            if note > maxNote:
                maxNote =  note
                best= [individu,round(resultat),energie,note,"generation ",j-1]
    moyenneResultat.append(moyenne_liste(resultatTab))
    tabVariance.append(variance_liste(tabNote))
    tabMoyenne.append(moyenne_liste(tabNote))
    print(generation)
    generation = generation +1

print('fin')
print("best is ",best)

plt.subplot(411)
plt.plot(resultatTab)
plt.ylabel('energie')
plt.xlabel('individus')


plt.subplot(414)
plt.plot(tabVariance)
plt.ylabel('variance')
plt.xlabel('generation')

plt.subplot(413)
plt.plot(tabMoyenne)
plt.ylabel('Moyenne note')
plt.xlabel('generation')

plt.subplot(412)
plt.plot(moyenneResultat)
plt.ylabel('Moyenne distance')
plt.xlabel('generation')
plt.show()




        #     print(round(note,0))
        #     tab.append([individu,resultat,round(note)])
        #     tabNote.append(note)
        #     print([individu,resultat, note])
        #     resultatTab.append(round(resultat,0))
        # print(sum(resultatTab))

    #      for  val in tabNote:
    #     somme=somme+val
    # tabMoyenne.append(somme/nPop)
    # tabVariance.append(variance_liste(tabNote))