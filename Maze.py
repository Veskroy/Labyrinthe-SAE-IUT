class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
        - clés : sommets
        - valeurs : ensemble des sommets voisins accessibles
    """
    def __init__(self, height: int, width: int, empty: bool):
        """
        Constructeur d'un labyrinthe de height cellules de haut 
        et de width cellules de large 
        Les voisinages sont initialisés à des ensembles vides
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
        """
        self.height    = height
        self.width     = width
        self.neighbors = {(i,j): set() for i in range(height) for j in range(width)}
        if empty is True:
            for i in range(height):
                for j in range(width):
                    if i+1 < height and j+1 < width:
                        self.neighbors[(i, j)].update({(i+1, j), (i, j+1)})
                        self.neighbors[(i+1, j)].update({(i, j), (i+1, j+1)})
                        self.neighbors[(i, j+1)].update({(i, j), (i+1, j+1)})
                    elif i+1 < height:
                        self.neighbors[(i, j)].update({(i+1, j)})
                        self.neighbors[(i+1, j)].update({(i, j)})
                    elif j+1 < width:
                        self.neighbors[(i, j)].update({(i, j+1)})
                        self.neighbors[(i, j+1)].update({(i, j)})

    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors)+"\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width-1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width-1):
            txt += "   ┃" if (0,j+1) not in self.neighbors[(0,j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height-1):
            txt += "┣"
            for j in range(self.width-1):
                txt += "━━━╋" if (i+1,j) not in self.neighbors[(i,j)] else "   ╋"
            txt += "━━━┫\n" if (i+1,self.width-1) not in self.neighbors[(i,self.width-1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i+1,j+1) not in self.neighbors[(i+1,j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width-1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt


    @classmethod
    def get_cells(self) -> list:
        return list(self.neighbors.keys())


    @classmethod
    def add_wall(self, c1, c2):
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:      # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2) # on le retire
        if c1 in self.neighbors[c2]:      # Si c3 est dans les voisines de c2
            self.neighbors[c2].remove(c1) # on le retire


    @classmethod
    def remove_wall(self, c1, c2) -> None:
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de la suppression d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Suppression du mur
        self.neighbors[c1].add(c2)
        self.neighbors[c2].add(c1)


    @classmethod
    def get_walls(self) -> list:
        """
        Retourne la liste des murs du labyrinthe
        """
        walls = []
        for c1 in self.get_cells():
            if (c1[0], c1[1]+1) in self.get_cells() and (c1[0], c1[1]+1) not in self.neighbors[c1]:
                walls.append([c1, (c1[0], c1[1]+1)])
            if (c1[0]+1, c1[1]) in self.get_cells() and (c1[0]+1, c1[1]) not in self.neighbors[c1]:
                walls.append([c1, (c1[0]+1, c1[1])])
        return walls


    @classmethod
    def fill(self) -> None:
        """
        Remplit le labyrinthe en ajoutant tous les murs
        """
        self.neighbors = Maze(self.height, self.width, False).neighbors


    @classmethod
    def empty(self) -> None:
        """
        Vide le labyrinthe en supprimant tous les murs
        """
        self.neighbors = Maze(self.height, self.width, True).neighbors


    @classmethod
    def get_contiguous_cells(self, c: tuple) -> list:
        """
        Retourne la liste des cellules contigues à la cellule c
        """
        # méthode précédente
        # return list(Maze(self.height, self.width, True).neighbors[c])
        
        contiguous_cells = []
        contiguous_cells.append((c[0]-1, c[1])) if c[0]-1 >= 0 else None
        contiguous_cells.append((c[0]+1, c[1])) if c[0]+1 < self.height else None
        contiguous_cells.append((c[0], c[1]-1)) if c[1]-1 >= 0 else None
        contiguous_cells.append((c[0], c[1]+1)) if c[1]+1 < self.width else None
        return contiguous_cells


    @classmethod
    def get_reachable_cells(self, c: tuple) -> list:
        """
        Retourne la liste des cellules accessibles à partir de la cellule c
        """
        return list(self.neighbors[c])