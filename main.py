import sys
from automates_finis_det import *
from automates_finis import *
from ensembles import *

def main():
	exBA = (["2D","2A","1","G"],\
		[("2D","A","2A"),("2D","R","1"),("2D","D","G"),("2A","A","2D"),("2A","R","1"),("2A","A","G"),("1","R","2D"),("1","R","2A"),("1","R","G"),("1","D","1"),("1","A","1"),("2A","D","2A")],\
		["2D","2A","1"],\
		["G"],\
		eq_atom)
	exBA_det = make_det(exBA)
	S,T,I,F,eqSD = exBA_det
	for t in T:
		print(t)
	# On en déduit que les étapes à suivre sont:
	# 	- aucun :
	# 		G | résolu en 0 coup
	# 	- diagonal :
	# 		(2D-d->G) | résolu en 1 coup
	# 	- diagonal puis adjacent puis diagonal si besoin :
	# 		(2A-d->2A) (2A-a->[2D,G]) ([2D,G]-d->G) | résolu entre 2 et 3 coups
	# 	- diagonal puis adjacent puis diagonal puis retournement puis diagonal si besoin puis adjacent si besoin puis diagonale si besoin :
	# 		(1-d->1) (1-a->1) (1-d->1) (1-r->[2A,2D,G]) ([2A,2D,G]-d->[2A,G]) ([2A,G]-a->[2D,G]) ([2D,G]-d->G) | résolu entre 4 et 7 coups
	# Donc pour toute configuration initiale on applique "dadrdad" (on s'arête dès qu'on a tout les verres dans le même sens)
if __name__ == '__main__':
    sys.exit(main())