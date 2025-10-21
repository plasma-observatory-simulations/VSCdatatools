import numpy as np
import os

DEFAULT_FILE_PATH = "./PO_constellation"

def clean(FILE_PATH = DEFAULT_FILE_PATH):
    try:
        os.remove(FILE_PATH + ".vtu")
        os.remove(FILE_PATH + ".txt")
    except:
        pass

def export_vtk(x,y,z, FILE_PATH=DEFAULT_FILE_PATH):

    from pyevtk.hl import unstructuredGridToVTK
    from pyevtk.vtk import VtkTriangle, VtkQuad

    connectivity = []
    offset = []
    cell_types = []


    #if using the above single spacecraft code then replace len(x1) with 1 
    for i in [0]:
       connectivity.extend([i*4, i*4+2, i*4+1, i*4+3])
       offset.append((i+1)*4)
       cell_types.append(10) #9 = Quad, 10 = Tetra
    for i in [1]:
       connectivity.extend([0, i*4+1, i*4, i*4+2])
       offset.append((i+1)*4)
       cell_types.append(10) #9 = Quad, 10 = Tetra

    for i in range(len(x)):
       connectivity.append(i)
       cell_types.append(1)
       offset.append(7+i+2)

    connectivity = np.array(connectivity, dtype=np.int32)
    offset = np.array(offset, dtype=np.int32)
    cell_types = np.array(cell_types, dtype=np.uint8)

    # print(x,connectivity, offset, cell_types)
    pointdata = {'ids':np.array([1,2,3,4,5,6,7])}
    unstructuredGridToVTK(FILE_PATH, np.ascontiguousarray(x), np.ascontiguousarray(y), np.ascontiguousarray(z), connectivity = connectivity, offsets=offset, cell_types = cell_types, pointData=pointdata)

def export_np(x,y,z, FILE_PATH=DEFAULT_FILE_PATH):
    float_fmt = "%20.16e"
    pts_array = np.vstack([np.array([1,2,3,4,5,6,7]),x,y,z]).T
    np.savetxt(FILE_PATH+".txt", pts_array, fmt="%d, "+float_fmt+", "+float_fmt+", "+float_fmt+"")

def import_np(FILE_PATH=DEFAULT_FILE_PATH):
    pass

def run(outerscale = 5000e3, FILE_PATH=DEFAULT_FILE_PATH):

    # Define vertices
    x = np.zeros(7)
    y = np.zeros(7)
    z = np.zeros(7)

    # inner tetrahedron size factor; required: < 1/4
    f=1.0/5.0

    x[0], y[0], z[0] = 0.0, 0.0, 0.0
    x[1], y[1], z[1] = 1.0, 1.0, 0.0
    x[2], y[2], z[2] = 1.0, 0.0, 1.0
    x[3], y[3], z[3] = 0.0, 1.0, 1.0
    x[4], y[4], z[4] = 1.0, 1.0, 0.0
    x[5], y[5], z[5] = 1.0, 0.0, 1.0
    x[6], y[6], z[6] = 0.0, 1.0, 1.0

    normf = np.sqrt((x[0]-x[1])**2 + (y[0]-y[1])**2 + (z[0]-z[1])**2)

    x /= normf
    y /= normf
    z /= normf

    x[4:] *= f
    y[4:] *= f
    z[4:] *= f

    x *= outerscale
    y *= outerscale
    z *= outerscale

    # This concludes setting the coordinates. Now these will be saved to various formats.
    try:
        export_np(x,y,z, FILE_PATH=DEFAULT_FILE_PATH)
    except Exception as e:
        print("Could not export in a numpy format, error was "+ str(e))
        raise e
    try:
        export_vtk(x,y,z, FILE_PATH=DEFAULT_FILE_PATH)
    except Exception as e:
        print("Could not export in a vtk format, error was "+ str(e))
        raise e


if __name__ == "__main__":
    FILE_PATH=DEFAULT_FILE_PATH
    run(FILE_PATH=DEFAULT_FILE_PATH)
