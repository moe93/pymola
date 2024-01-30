
from    scipy                           import  io
import  numpy                           as      np

def matlab_matrix( name: str, matrix: dict, path: str = None ):
    '''
    
    Convert numpy arrays into MATLAB indexable matrices.
    Recall, for numpy the indices correspond to:
        -> (Depth, Rows, Cols)

    For MATLAB, the indices correspond to:
        -> (Rows, Cols, Depth)

    '''
    
    # Convert into MATLAB style indexing matrix
    for key, val in matrix.items():
        ith_matrix = val
        ith_matrix = np.swapaxes(ith_matrix, 1, 0)
        ith_matrix = np.swapaxes(ith_matrix, 2, 1)
        matrix[ key ] = ith_matrix

    io.savemat( name, matrix )

    return 0

