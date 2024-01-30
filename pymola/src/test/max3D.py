import  numpy                           as      np

N_DEPTH = 3
N_ROWS  = 3
N_COLS  = 3

A = np.zeros( (N_DEPTH, N_ROWS, N_COLS), dtype=np.float32 )

A1 = np.ones( (N_ROWS, N_COLS) ) * 1; A1[0,0] = 10; A1[1,0] = -10
A2 = np.ones( (N_ROWS, N_COLS) ) * 2; A2[1,1] = 20; A2[2,1] = -20
A3 = np.ones( (N_ROWS, N_COLS) ) * 3; A3[2,2] = 30; A3[0,2] = -30

A[0] = A1; A[1] = A2; A[2] = A3

A_max = A.max(axis=0)
A_min = A.min(axis=0)

pass