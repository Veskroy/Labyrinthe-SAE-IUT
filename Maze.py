import random


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


    def get_cells(self) -> list:
        """Retourne la liste des cellules du labyrinthe

        Returns
        -------
        :class:`list`
            Liste des cellules du labyrinthe
        """
        return list(self.neighbors.keys())


    def add_wall(self, c1: tuple, c2: tuple):
        """Ajouter un mur entre deux cellules

        Parameters
        ----------
        c1 : :class:`tuple`
            Première cellule (ligne, colonne)
        c2 : :class:`tuple`
            Deuxième cellule (ligne, colonne)
        """
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


    def remove_wall(self, c1: tuple, c2: tuple) -> None:
        """Supprime un mur entre deux cellules

        Parameters
        ----------
        c1 : :class:`tuple`
            Première cellule (ligne, colonne)
        c2 : :class:`tuple`
            Deuxième cellule (ligne, colonne)
        """
        assert 0 <= c1[0] < self.height and \
            0 <= c1[1] < self.width and \
            0 <= c2[0] < self.height and \
            0 <= c2[1] < self.width, \
            f"Erreur lors de la suppression d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Suppression du mur
        self.neighbors[c1].add(c2)
        self.neighbors[c2].add(c1)


    def get_walls(self) -> list:
        """Retourne la liste des murs du labyrinthe

        Returns
        -------
        :class:`list`
            Liste des murs du labyrinthe
        """
        walls = []
        for c1 in self.get_cells():
            if (c1[0], c1[1]+1) in self.get_cells() and (c1[0], c1[1]+1) not in self.neighbors[c1]:
                walls.append([c1, (c1[0], c1[1]+1)])
            if (c1[0]+1, c1[1]) in self.get_cells() and (c1[0]+1, c1[1]) not in self.neighbors[c1]:
                walls.append([c1, (c1[0]+1, c1[1])])
        return walls


    def fill(self) -> None:
        """Remplit le labyrinthe en ajoutant tous les murs
        """
        self.neighbors = Maze(self.height, self.width, False).neighbors


    def empty(self) -> None:
        """Vide le labyrinthe en supprimant tous les murs
        """
        self.neighbors = Maze(self.height, self.width, True).neighbors


    def get_contiguous_cells(self, c: tuple) -> list:
        """Retourne la liste des cellules contigues à la cellule c

        Parameters
        ----------
        c : :class:`tuple`
            Cellule (ligne, colonne)

        Returns
        -------
        :class:`list`
            Liste des cellules contigues à la cellule c
        """
        # méthode précédente
        # return list(Maze(self.height, self.width, True).neighbors[c])
        
        contiguous_cells = []
        contiguous_cells.append((c[0]-1, c[1])) if c[0]-1 >= 0 else None
        contiguous_cells.append((c[0]+1, c[1])) if c[0]+1 < self.height else None
        contiguous_cells.append((c[0], c[1]-1)) if c[1]-1 >= 0 else None
        contiguous_cells.append((c[0], c[1]+1)) if c[1]+1 < self.width else None
        return contiguous_cells


    def get_reachable_cells(self, c: tuple) -> list:
        """Retourne la liste des cellules accessibles à partir de la cellule c

        Parameters
        ----------
        c : :class:`tuple`
            Cellule (ligne, colonne)

        Returns
        -------
        :class:`list`
            Liste des cellules accessibles à partir de la cellule c
        """
        return list(self.neighbors[c])


    @classmethod
    def gen_btree(cls, height: int, width: int) -> 'Maze':
        """Génère un labyrinthe aléatoire selon l'algorithme "Binary Tree"

        Parameters
        ----------
        height : :class:`int`
            Hauteur du labyrinthe
        width : :class:`int`
            Largeur du labyrinthe

        Returns
        -------
        :class:`Maze`
            Labyrinthe généré
        """
        maze = Maze(height, width, False)
        for x, y in maze.get_cells():
            walls = list(set(maze.get_contiguous_cells((x, y))) - set(maze.get_reachable_cells((x, y))))
            c_south = (x+1, y)
            c_east = (x, y+1)
            if c_south in walls and c_east in walls:
                maze.remove_wall((x, y), (x, y+1)) if random.randint(0, 1) else maze.remove_wall((x, y), (x+1, y))
            elif c_south in walls: 
                maze.remove_wall((x, y), (x+1, y))
            elif c_east in walls:
                maze.remove_wall((x, y), (x, y+1))
        return maze


    @classmethod
    def gen_sidewinder(cls, height: int, width: int) -> 'Maze':
        """Génère un labyrinthe aléatoire selon l'algorithme "Sidewinder"

        Parameters
        ----------
        height : :class:`int`
            Hauteur du labyrinthe
        width : :class:`int`
            Largeur du labyrinthe

        Returns
        -------
        :class:`Maze`
            Labyrinthe généré
        """
        maze = Maze(height, width, False)
        for i in range(height-2):
            sequence = []
            for j in range(width-2):
                # print(i, j)
                sequence.append((i, j))
                if random.randint(0, 1):
                    last_cell = (i, j+1)
                    maze.remove_wall((i, j), (i, j+1))
                else:
                    random_cell = random.choice(sequence)
                    last_cell = (random_cell[0]+1, random_cell[1])
                    maze.remove_wall(random_cell, (random_cell[0]+1, random_cell[1]))
                    sequence = []
            sequence.append(last_cell)
            random_cell = random.choice(sequence)
            maze.remove_wall(random_cell, (random_cell[0]+1, random_cell[1]))
        # casser tous les murs est de la dernière ligne
        for j in range(width-1):
            maze.remove_wall((height-1, j), (height-1, j+1))
        return maze