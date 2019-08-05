import os
import os.path
import re
from .Triangle import Triangle
from .Solid import Solid
from .Point import Point
from typing import List

class File(object):
    """ File-object

    Example for a file definition

    >>> file1 = File(1, "foo.txt")
    """

    def __init__(self,ID=None, Filepath=None):
        self.__filepath = Filepath
        self.__id = ID

    @property
    def id(self):
        return self.__id

    @ id.setter
    def id(self, ID):
        self.__id = ID

    @property
    def filepath(self):
        return self.__filepath

    @filepath.setter
    def filepath(self, filepath):
        self.__filepath = filepath


class STL(File):
    """ STL-File with geometric data

    :param ID (int): Id of the file
    :param Filepath (str): Path of the file

    Example for creating an stl-object

    >>> file1 = STL(1, "./foo.stl")
    >>> part = file.parts[0]

    .. note::
        The file will automatically import the results if the file is given
        Otherwise you need to call import_stl
    """
    def __init__(self, ID=None, Filepath=None):
        File.__init__(self, ID, Filepath)
        self.__parts = []
        # If file is given the importin will started
        if self.filepath:
            self.read()

    def get_parts(self)->List[Solid]:
        """
        :return: All solid objects which are imported
        """
        return self.__parts

    def add_solid(self, solid: Solid):
        self.__parts.append(solid)


    def write(self, filename):
        """ This method can export the current data into an stl-file

        """
        if os.path.isfile(filename):
            raise ValueError ("File does exist alread %f", filename)
        print("Export stl in", filename)
        o_file = open(filename,"w")
        for part in self.__parts:
            solid = part
            o_file.write("solid Exported from DMST-STL\n")
            for triangle in solid.triangles:
                o_file.write("facet normal " + str(triangle.normal[0]) + " " + str(triangle.normal[1]) + " " + str(triangle.normal[2]) + "\n")
                o_file.write("outer loop\n")
                for point in triangle.points:
                    o_file.write("vertex " + str(point.x) + " " + str(point.y) + " " + str(point.z) + "\n")
                o_file.write("endloop\n")
                o_file.write("endfacet\n")
            o_file.write("endsolid\n")

    def read(self):
        """ This method imports the geometry to the parts attribute

        """

        if not os.path.isfile(self.filepath):
            raise ValueError ("Given file doesnt exist %f", self.filepath)
        i_file = open(self.filepath, "r")

        # Patterns which are needed
        s_pat = "solid"
        l_pat = "outer loop"
        f_pat = "facet"
        p_pat = "vertex"

        f_e_pat = "endfacet"
        s_e_pat = "endsolid"
        l_e_pat = "endloop"

        solid_is_found = False
        facet_is_found = False
        loop_is_found = False
        id_s = 0 # ID of the solid
        id_t = 0 # ID for triangles
        id_p = 0 # ID for points

        tmp_p_list = [] # Saves all found points
        id_p_old = 0 #ID for points

        # Reading the file
        for line in i_file:
            line = line[0:-1]

            # Solid is found

            if re.match(s_pat, line, 2):
                id_s +=1
                s = Solid(id_s, [])
                self.__parts.append(s)
                solid_is_found = True
                continue
            # Solid is closed
            if re.match(s_e_pat, line, 2):
                solid_is_found = False
                continue

            # Facet is found
            if re.match(f_pat, line,2) and solid_is_found:
                id_t += 1
                facet_is_found = True
                t = Triangle(id_t, [])
                words = line.split(" ")
                nx = float(words[2])
                ny = float(words[3])
                nz = float(words[4])
                t.normal = [nx, ny, nz]
                s.triangles.append(t)
                continue
            # Facet is closed
            if re.match(f_e_pat, line,2) and solid_is_found and facet_is_found:

                facet_is_found = False
                continue

            # Loop is found
            if re.match(l_pat, line,2) and solid_is_found and facet_is_found:
                loop_is_found = True
                continue
            # Loop is closed
            if re.match(l_e_pat, line,2) and solid_is_found and facet_is_found and loop_is_found:
                loop_is_found = False
                continue

            # Vertex is found
            if re.match(p_pat, line,2) and solid_is_found and facet_is_found and loop_is_found:
                # Finding new point coord
                words = line.split(" ")
                x = float(words[1])
                y = float(words[2])
                z = float(words[3])

                # Checking if point_id exists already
                # If the point_id is found choose the same ID
                p_is_found = False
                controll_count = 0
                for t_p in tmp_p_list:
                    if t_p.x == x and t_p.y == y and t_p.z == z:
                        id_p_old = t_p.id
                        controll_count += 1
                        p_is_found = True
                    if controll_count > 1:
                        raise ValueError("Two same points have different ID s")

                # Creating a new point_id or selectin an old
                if p_is_found:
                    p = Point(id_p_old, x, y, z)
                else:
                    id_p += 1
                    p = Point(id_p, x, y, z)
                    tmp_p_list.append(p)

                # Resulting point
                t.points.append(p)
        i_file.close()
        if id_s== 0 or id_t== 0 or id_p== 0:
            raise ValueError("Fileformat STL does not match: Define Solid-->Faces-->Vertexes")
        print("STL-File succesfully imported")
        print("Solids: ", id_s)
        print("Triangles", id_t)
        print("Different Vertices", id_p)