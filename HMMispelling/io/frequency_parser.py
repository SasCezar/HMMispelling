import csv
import numpy as np
import math as mh

def load_probabilities( file ):

    i = 0
    probability = np.matrix([])

    with open( file, 'r' ) as csv_file:

        reader = csv.reader( csv_file )
        next( reader ) # Skip of header row

        for row in reader:

            row_values = row[1:] # Remove first column
            row_float = [ float(k) for k in row_values ] # Casting to float
            probability = np.matrix( row_float ) if i == 0 else np.vstack( [probability, row_float] )
            i += 1

        if ( probability[0,:].sum != 1 ):
            probability = normalize_distribution( probability )

    return probability


def normalize_distribution( matrix ):

    r = matrix.shape[0]
    c = matrix.size
    matrix_norm = np.matrix([])

    if r == 1:
        for i in np.nditer(matrix):
            el = i / 100 # Apply the function
            matrix_norm = np.hstack(( matrix_norm, [[el]] )) # Append the new element
    else:
        for i in np.nditer(matrix):
            if i == 0:
                el = 0 # To avoid e^0 = 1 the element should not be transformed
            else:
                el = round( mh.exp(i), 0 ) # Apply the function if the element in matrix is not 0
            matrix_norm = np.hstack(( matrix_norm, [[el]] )) # Append the new element

        slice = int(c/r)
        matrix_norm = matrix_norm.reshape(1, r, slice)

        matrix_norm = np.apply_along_axis(normalize, 1, matrix_norm)
        #matrix_norm = matrix_norm.round(3)

    return matrix_norm


def normalize(v):

    norm = np.linalg.norm(v, ord=1)
    if norm == 0:
        norm = np.finfo(v.dtype).eps
    return v/norm
