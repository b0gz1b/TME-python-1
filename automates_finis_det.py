#====================================#
# UE Calculabilite L3 / M1 SFTR      #
# TME Automates finis deterministes  #
# Mathieu.Jaume@lip6.fr              #
#====================================#

from automates_finis import *

# Liste des transitions de T dont l'origine est l'etat s
# ------------------------------------------------------

def lt_from_s(eqS,s,T):
    # eqS : fonction d'egalite sur les etats
    # s : etat
    # T : liste de transitions
    return [(s1,l,s2) for (s1,l,s2) in T if eqS(s1,s)]

# Liste des labels presents sur les transitions issues d'un etat s
# ----------------------------------------------------------------

def label_from(eqS,s,T):
    # eqS : fonction d'egalite sur les etats
    # s : etat
    # T : liste de transitions
    R = []
    for (si,l,sf) in T:
        if eqS(si,s) and l != None:
            R = ajout(eq_atom,l,R)
    return R

# Liste des labels presents sur les transitions issues d'un ensemble d'etats
# --------------------------------------------------------------------------

def label_from_set(eqS,S,T):
    # eqS : fonction d'egalite sur les etats
    # S : liste d'etats
    # T : liste de transitions
    R = []
    for s in S:
        R = union(eq_atom,label_from(eqS,s,T),R)
    return R

# Automates finis deterministes
#------------------------------

# determine si la relation de transition a partir d'un etat s est
# fonctionnelle et ne contient aucune epsilon-transition
# ---------------------------------------------------------------

def lt_from_s_deterministic(T):
    # T : liste de transitions
    def _aux(L):
        if len(L)==0:
            return True
        else:
            if L[0] == None or L[0] in L[1:]:
                return False
            else:
                return _aux(L[1:])
    return _aux([l for (_,l,_) in T])


# determine si un automate est deterministe
# -----------------------------------------

def is_deterministic(A):
    S,T,I,F,eqS = A
    if len(I)>1:
        return False
    else:
        for s in S:
            if not lt_from_s_deterministic(lt_from_s(eqS,s,T)):
                return False
    return True

# Determinisation
#----------------

# Egalite entre transitions d'un automate
# ---------------------------------------

def eq_trans(eqS,t1,t2):
    (si1,l1,sf1) = t1
    (si2,l2,sf2) = t2
    return l1==l2 and eqS(si1,si2) and eqS(sf1,sf2)

def make_eq_trans(eqS):
    def _eq_trans(t1,t2):
        return eq_trans(eqS,t1,t2)
    return _eq_trans

# Determinisation d'un automate fini avec epsilon-transitions
# -----------------------------------------------------------

def make_det(A):
    # A : automate fini
    # A COMPLETER
    S,T,I,F,eqS = A
    eqSet_det = make_eq_set(eqS)
    eqSet_trans_det = make_eq_trans(eqSet_det)
    if not is_deterministic(A):
        to_do = [eps_cl_set(eqS,I,T)] # File des ??tats ?? traiter
        done = [] # Ensembles des ??tats de l'automate d??termis??
        T_det = [] # Ensembles des transitions de l'automate d??termis??
        I_det = [to_do[0]] # Ensembles des ??tats initiaux de l'automate d??termis??
        F_det = [] # Ensembles des ??tats finaux de l'automate d??termis??
        while to_do: # Tant qu'il reste des ??tats ?? traiter
            done.append(to_do[-1]) # Selection de l'??tat ?? traiter
            to_do = to_do[:-1] # On retire l'??l??ment de la file
            L = label_from_set(eqS,S,T) # R??cup??ration des ??tiquettes des transitions partant de l'??tat
            for l in L: # Pour chacune de ces ??tiquettes
                state = []
                for s in done[-1]: # Pour chacun des ??tats de l'ensemble
                    for d in reach_from(eqS,s,l,T):
                        state = ajout(eqS,d,state) # On ajoute au nouvel ??tat les ??tats accesibles par l'??tiquette
                if state:
                    state = eps_cl_set(eqS,state,T) # On construit l'espilon-clot??re du nouvel ??tat
                    T_det = ajout(eqSet_trans_det,(done[-1],l,state),T_det) # On ajoute la transition ?? l'automate determinis??
                    if not is_in(eqSet_det,state,done): # Si l'??tat n'est pas dans l'automate
                        to_do = ajout(eqSet_det,state,to_do) # On l'ajoute ?? la file d'attente
                        if intersection(eqS,F,state): # Si il est compos?? d'au moins un ??tat final
                            F_det = ajout(eqSet_det,state,F_det) # On l'ajoute aux finaux
        return (done,T_det,I_det,F_det,eqSet_det)
    return A