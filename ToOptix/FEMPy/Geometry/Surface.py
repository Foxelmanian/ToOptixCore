from .Triangle import Triangle
from .Solid import Solid

class Surface():

    def __init__(self):
        self.__triangles = []

    @property
    def triangles(self):
        return self.__triangles

    @triangles.setter
    def triangles(self, Triangles):
        self.__triangles = Triangles

    def create_surface_on_elements(self, elements):
        eFace = {} # Counts how many times is there a face
        for elem in elements:
            if len(elem.get_nodes()) == 8 or len(elem.get_nodes()) == 20:
                n1 = elem.get_nodes()[0].id
                n2 = elem.get_nodes()[1].id
                n3 = elem.get_nodes()[2].id
                n4 = elem.get_nodes()[3].id
                n5 = elem.get_nodes()[4].id
                n6 = elem.get_nodes()[5].id
                n7 = elem.get_nodes()[6].id
                n8 = elem.get_nodes()[7].id
                f = sorted([n1, n2, n3, n4])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face2
                f = sorted([n5, n8, n7, n6])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face3
                f = sorted([n1, n5, n6, n2])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face4
                f = sorted([n2, n6, n7, n3])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face5
                f = sorted([n3, n7, n8, n4])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face6
                f = sorted([n4, n8, n5, n1])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
            if len(elem.get_nodes()) == 6  or len(elem.get_nodes()) == 15:
                n1 = elem.get_nodes()[0].id
                n2 = elem.get_nodes()[1].id
                n3 = elem.get_nodes()[2].id
                n4 = elem.get_nodes()[3].id
                n5 = elem.get_nodes()[4].id
                n6 = elem.get_nodes()[5].id
                # Face1
                f = sorted([n1, n2, n3])
                try:
                    eFace[f[0], f[1], f[2]] = eFace[f[0], f[1], f[2]] + 1
                except:
                    eFace[f[0], f[1], f[2]] = 1
                # Face2
                f = sorted([n4, n6, n5])
                try:
                    eFace[f[0], f[1], f[2]] = eFace[f[0], f[1], f[2]] + 1
                except:
                    eFace[f[0], f[1], f[2]] = 1
                # Face3
                f = sorted([n1, n4, n5, n2])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face4
                f = sorted([n2, n5, n6, n3])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1
                # Face5
                f = sorted([n3, n6, n4, n1])
                try:
                    eFace[f[0], f[1], f[2], f[3]] = eFace[f[0], f[1], f[2], f[3]] + 1
                except:
                    eFace[f[0], f[1], f[2], f[3]] = 1

            if len(elem.get_nodes()) == 4 or len(elem.get_nodes()) == 10:
                n1 = elem.get_nodes()[0].id
                n2 = elem.get_nodes()[1].id
                n3 = elem.get_nodes()[2].id
                n4 = elem.get_nodes()[3].id
                # Face1
                f = sorted([n1, n2, n3])
                try:
                    eFace[f[0], f[1], f[2]] = eFace[f[0], f[1], f[2]] + 1
                except:
                    eFace[f[0], f[1], f[2]] = 1
                # Face2
                f = sorted([n1, n4, n2])
                try:
                    eFace[f[0], f[1], f[2]] = eFace[f[0], f[1], f[2]] + 1
                except:
                    eFace[f[0], f[1], f[2]] = 1
                # Face3
                f = sorted([n2, n4, n3])
                try:
                    eFace[f[0], f[1], f[2]] = eFace[f[0], f[1], f[2]] + 1
                except:
                    eFace[f[0], f[1], f[2]] = 1
                # Face4
                f = sorted([n3, n4, n1])
                try:
                    eFace[f[0], f[1], f[2]] = eFace[f[0], f[1], f[2]] + 1
                except:
                    eFace[f[0], f[1], f[2]] = 1
        tn = 0
        for elem in elements:
            if len(elem.get_nodes()) == 8 or len(elem.get_nodes()) == 20:
                n1 = elem.get_nodes()[0].id
                n2 = elem.get_nodes()[1].id
                n3 = elem.get_nodes()[2].id
                n4 = elem.get_nodes()[3].id
                n5 = elem.get_nodes()[4].id
                n6 = elem.get_nodes()[5].id
                n7 = elem.get_nodes()[6].id
                n8 = elem.get_nodes()[7].id
                n11 = elem.get_nodes()[0]
                n22 = elem.get_nodes()[1]
                n33 = elem.get_nodes()[2]
                n44 = elem.get_nodes()[3]
                n55 = elem.get_nodes()[4]
                n66 = elem.get_nodes()[5]
                n77 = elem.get_nodes()[6]
                n88 = elem.get_nodes()[7]
                # Face1
                f = sorted([n1, n2, n3, n4])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n11, n22, n33], [n1, n2, n3])
                    self.triangles.append(tmp_tri)
                    tn += 1
                    tmp_tri = Triangle(tn, [n33, n44, n11], [n3, n4, n1])
                    self.triangles.append(tmp_tri)
                    tn += 1
                # Face2
                f = sorted([n5, n8, n7, n6])
                if eFace[f[0], f[1], f[2], f[3]] == 1:

                    tmp_tri = Triangle(tn, [n55, n88, n77], [n5, n8, n7])
                    self.triangles.append(tmp_tri)
                    tn += 1
                    tmp_tri = Triangle(tn, [n77, n66, n55], [n7, n6, n5])
                    self.triangles.append(tmp_tri)
                    tn += 1
                # Face3
                f = sorted([n1, n5, n6, n2])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n11, n55, n66], [n1, n5, n6])

                    self.triangles.append(tmp_tri)
                    tn += 1
                    tmp_tri = Triangle(tn, [n66, n22, n11], [n6, n2, n1])
                    self.triangles.append(tmp_tri)
                    tn += 1
                # Face4
                f = sorted([n2, n6, n7, n3])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n22, n66, n77], [n2, n6, n7])
                    self.triangles.append(tmp_tri)
                    tn += 1
                    tmp_tri = Triangle(tn, [n77, n33, n22], [n7, n3, n2])
                    self.triangles.append(tmp_tri)
                    tn += 1
                # Face5
                f = sorted([n3, n7, n8, n4])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n33, n77, n88], [n3,n7,n8])
                    self.triangles.append(tmp_tri)
                    tn += 1

                    tmp_tri = Triangle(tn, [n88, n44, n33], [n8,n4,n3])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face6
                f = sorted([n4, n8, n5, n1])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n44, n88, n55], [n4,n8,n5])
                    self.triangles.append(tmp_tri)
                    tn += 1

                    tmp_tri = Triangle(tn, [n55, n11, n44], [n5,n1,n4])
                    self.triangles.append(tmp_tri)
                    tn += 1

            if len(elem.get_nodes()) == 6 or len(elem.get_nodes()) == 15:
                n1 = elem.get_nodes()[0].id
                n2 = elem.get_nodes()[1].id
                n3 = elem.get_nodes()[2].id
                n4 = elem.get_nodes()[3].id
                n5 = elem.get_nodes()[4].id
                n6 = elem.get_nodes()[5].id
                n11 = elem.get_nodes()[0]
                n22 = elem.get_nodes()[1]
                n33 = elem.get_nodes()[2]
                n44 = elem.get_nodes()[3]
                n55 = elem.get_nodes()[4]
                n66 = elem.get_nodes()[5]
                # Face1
                f = sorted([n1, n2, n3])
                if eFace[f[0], f[1], f[2]] == 1:
                    tmp_tri = Triangle(tn, [n11, n22, n33], [n1, n2, n3])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face2
                f = sorted([n4, n6, n5])
                if eFace[f[0], f[1], f[2]] == 1:
                    tmp_tri = Triangle(tn, [n44, n66, n55], [n4,n6,n5])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face3
                f = sorted([n1, n4, n5, n2])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n11, n44, n55], [n1,n4,n5])
                    self.triangles.append(tmp_tri)
                    tn += 1

                    tmp_tri = Triangle(tn, [n55, n22, n11], [n5,n2,n1])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face4
                f = sorted([n2, n5, n6, n3])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n22, n55, n66], [n2,n5,n6])
                    self.triangles.append(tmp_tri)
                    tn += 1

                    tmp_tri = Triangle(tn, [n66, n33, n22], [n6,n3,n2])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face5
                f = sorted([n3, n6, n4, n1])
                if eFace[f[0], f[1], f[2], f[3]] == 1:
                    tmp_tri = Triangle(tn, [n33, n66, n44], [n3,n6,n4])
                    self.triangles.append(tmp_tri)
                    tn += 1

                    tmp_tri = Triangle(tn, [n44, n11, n33], [n4,n1,n3])
                    self.triangles.append(tmp_tri)
                    tn += 1

            if len(elem.get_nodes()) == 4 or len(elem.get_nodes()) == 10:
                n1 = elem.get_nodes()[0].id
                n2 = elem.get_nodes()[1].id
                n3 = elem.get_nodes()[2].id
                n4 = elem.get_nodes()[3].id
                n11 = elem.get_nodes()[0]
                n22 = elem.get_nodes()[1]
                n33 = elem.get_nodes()[2]
                n44 = elem.get_nodes()[3]
                # Face1
                f = sorted([n1, n2, n3])
                if eFace[f[0], f[1], f[2]] == 1:
                    tmp_tri = Triangle(tn, [n11, n22, n33], [n1,n2,n3])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face2
                f = sorted([n1, n4, n2])
                if eFace[f[0], f[1], f[2]] == 1:
                    tmp_tri = Triangle(tn, [n11, n44, n22],[n1,n4,n2])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face3
                f = sorted([n2, n4, n3])
                if eFace[f[0], f[1], f[2]] == 1:
                    tmp_tri = Triangle(tn, [n22, n44, n33], [n2,n4,n3])
                    self.triangles.append(tmp_tri)
                    tn += 1

                # Face4
                f = sorted([n3, n4, n1])
                if eFace[f[0], f[1], f[2]] == 1:
                    tmp_tri = Triangle(tn, [n33, n44, n11], [n3,n4,n1])
                    self.triangles.append(tmp_tri)
                    tn += 1