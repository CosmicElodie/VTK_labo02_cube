# ======================================================================================
# Laboratoire   : n°2 - Simple Cube
# Élèves        : Crüll Loris, Lagier Elodie

# Décommenter les lignes suivantes pour afficher le cube selon les polyDatas souhaitées :
# ligne 88  -> 6 carrés
# ligne 100 -> 12 triangles
# ligne 116 -> 1 triangle strip
# ======================================================================================

import vtk

# ===========================================
# Coordonnées
# ===========================================
cube_coordinates = [
    #   X   Y   Z
    (0.5, 0.5, 0.5),
    (-0.5, 0.5, 0.5),
    (0.5, -0.5, 0.5),
    (-0.5, -0.5, 0.5),
    (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),
    (0.5, -0.5, -0.5),
    (-0.5, -0.5, -0.5)
]

squares = [(0, 2, 6, 4),
           (1, 3, 2, 0),
           (1, 5, 7, 3),
           (2, 3, 7, 6),
           (4, 5, 1, 0),
           (7, 5, 4, 6)]

triangles = [(0, 2, 4),
             (1, 3, 2),
             (1, 2, 0),
             (1, 5, 3),
             (2, 6, 4),
             (2, 3, 6),
             (3, 7, 6),
             (4, 5, 0),
             (5, 1, 0),
             (5, 7, 3),
             (5, 4, 6),
             (7, 5, 6)]

triangleStrip = [[0, 1, 2, 3, 6, 7, 4, 5, 2, 6, 0, 4, 1, 5, 3, 7]]

points = vtk.vtkPoints()
cells = vtk.vtkCellArray()  # faces -> polys 46:30 vidéo Cuicui
scalars = vtk.vtkFloatArray()

# on insère les 8 points
for i in range(0, 8):
    points.InsertPoint(i, cube_coordinates[i])

# on forme les faces
for face in squares:
    cells.InsertNextCell(4, face)

# float array associé aux vtkPoints
for i in range(0, 8):
    scalars.InsertTuple1(i, i)

# on créé le cube
cube = vtk.vtkPolyData()
cube.SetPoints(points)
cube.SetPolys(cells)
cube.GetPointData().SetScalars(scalars)

# On créé le reader qui va nous permettre de lire les données des différents fichiers
cube_reader = vtk.vtkPolyDataReader()


# Permet de créer un fichier contenant les coordonnées des polyDatas passées
def create_file(filename, data):
    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(filename)
    writer.SetInputData(data)
    writer.Write()


# ===========================================
# utilise 6 carrés
# ===========================================
create_file('cubeSquares.vtk', cube)
cube_reader.SetFileName('cubeSquares.vtk')

# ===========================================
# utilise 12 triangles
# ===========================================
polys = vtk.vtkCellArray()

for face in triangles:
    polys.InsertNextCell(3, face)

cube.SetPolys(polys)
create_file('cubeTriangles.vtk', cube)
# cube_reader.SetFileName('cubeTriangles.vtk')

# ===========================================
# utilise 1 triangle strip
# ===========================================
strip = vtk.vtkCellArray()
for current_strip in triangleStrip:
    strip.InsertNextCell(len(current_strip))
    for cell in current_strip:
        strip.InsertCellPoint(cell)

cube = vtk.vtkPolyData()
cube.SetPoints(points)
cube.SetStrips(strip)
cube.GetPointData().SetScalars(scalars)
create_file('cubeTriangleStrips.vtk', cube)
# cube_reader.SetFileName('cubeTriangleStrips.vtk')

# On procède comme dans le fichier cone5.py
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(cube_reader.GetOutputPort())
mapper.SetScalarRange(0, 10)

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().BackfaceCullingOn()

renderer = vtk.vtkRenderer()
renderer.SetBackground(0.5, 0.7, 0.65)
renderer.AddActor(actor)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(600, 600)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()
iren.Start()
