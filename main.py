from    platform                        import  system
from    pathlib                         import  Path
import  pandas                          as      pd
import  numpy                           as      np

import  pymola

# --- While Dymola runs on different operating systems, I only need it to run on Windows for personal reasons.
if( system() != "Windows" ): exit

# --- Current path where this script is running from
currentPath = Path(__file__).resolve().parent
# --- Name of FMU model we are interested in simulating
fmuName = "FMU_QFT_MIMO_Regime3.fmu"
# --- Full path to FMU
fmuPath = Path( currentPath, 'data', fmuName )

model       = pymola.Pymola( fmuPath )
variables   = model.get_variables()
states      = model.get_states()
inputs      = model.get_inputs()
outputs     = model.get_outputs()

# paramNames  = [ 'fMU_linHub.hub_revolute.phi', 'fMU_linHub.hub_revolute.w' ]
paramNames  = [ 'fMU_linHub.hub_revolute.phi' ]
paramValues = [None] * len( paramNames )

for ndx, parameter in enumerate( paramNames ):
    paramValues[ ndx ] = model.get_param_value( parameter )

# Get nominal plant S.S. matrices
A_nom, B_nom, C_nom, D_nom = model.linearize()
A_df, B_df, C_df, D_df = model.linearize( as_pdDataFrame=True )

# Sweep over azimuth angle
azimuth = [ i for i in range(0, 360, 30)]
n_depth = len( azimuth )

# Initialize 3D matrices for data storage
A_3D = np.zeros( (n_depth, A_nom.shape[0], A_nom.shape[1]), dtype=np.float32 )
B_3D = np.zeros( (n_depth, B_nom.shape[0], B_nom.shape[1]), dtype=np.float32 )
C_3D = np.zeros( (n_depth, C_nom.shape[0], C_nom.shape[1]), dtype=np.float32 )
D_3D = np.zeros( (n_depth, D_nom.shape[0], D_nom.shape[1]), dtype=np.float32 )

for ndx, angle in enumerate( azimuth ):
    model.set_param_value( paramNames[0], angle )
    A, B, C, D  = model.linearize()
    # Store A, B, C, D in the ndx-th depth of the *_3D matrix
    A_3D[ ndx ] = A;    B_3D[ ndx ] = B
    C_3D[ ndx ] = C;    D_3D[ ndx ] = D

# Find min/max elements and create a matrix that corresponds to them
A_max = A_3D.max( axis=0 ); A_min = A_3D.min( axis=0 )  # min/max across depth
B_max = B_3D.max( axis=0 ); B_min = B_3D.min( axis=0 )  # min/max across depth
C_max = C_3D.max( axis=0 ); C_min = C_3D.min( axis=0 )  # min/max across depth
D_max = D_3D.max( axis=0 ); D_min = D_3D.min( axis=0 )  # min/max across depth

# ======================================
# --- 3D BAR COLORMAP PLOTS (A MATRIX)
# ======================================
import  matplotlib.pyplot               as      plt
from    matplotlib                      import  colormaps # Import colormaps!

# Find percent change between max and min
def get_change( max_elem, min_elem):
    if max_elem == min_elem:
        return 0
    try:
        if(min_elem == 0): return 0
        else: return (abs(max_elem - min_elem) / abs(min_elem)) * 100.0
    except ZeroDivisionError:
        # return float('inf')
        return 0
    
delta_A = np.zeros_like( A_nom )
for ith_Row, ith_Col in np.ndindex(A_nom.shape):
    print( f'(ith_Row, ith_Col) = ({ith_Row}, {ith_Col})' )
    max_elem = A_max[ith_Row, ith_Col]
    min_elem = A_min[ith_Row, ith_Col]
    delta_A[ith_Row, ith_Col] = get_change(max_elem, min_elem)

# Normalize values
A_final = delta_A / np.amax(delta_A)

fig = plt.figure()
ax = plt.axes(projection = "3d")
 
countries = [" ","Australia", " ","Brazil", " ","Canada", " ","France"]

data = A_final.T
years = [None, None, 2005, None, 2010, None, 2015]
 
numOfRows = data.shape[0]
numOfCols = data.shape[1]
 
xpos = np.arange(0, numOfCols, 1)
ypos = np.arange(0, numOfRows, 1)
xpos, ypos = np.meshgrid(xpos + 0.5, ypos + 0.5)
 
xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros(numOfCols * numOfRows)
 
dx = np.ones(numOfRows * numOfCols) * 0.5
dy = np.ones(numOfCols * numOfRows) * 0.5
dz = data.flatten()

# --- Color map stuff
# cmap = cm.get_cmap('jet') # Get desired colormap
cmap = colormaps['jet'] # Get desired colormap
max_height = np.max(dz)   # get range of colorbars
min_height = np.min(dz)
# scale each z to [0,1], and get their rgb values
rgba = [cmap((k-min_height)/max_height) for k in dz]
ax.set_xticks( [i+1 for i in range(0, numOfCols)],
               [ '$x_1$', '$x_2$', '$x_3$', '$x_4$',
                 '$x_5$', '$x_6$', '$x_7$', '$x_8$',
                 '$x_9$', '$x_{10}$', '$x_{11}$' ] )
ax.set_yticks( [i+1 for i in range(0, numOfRows)],
               [ '$x_1$', '$x_2$', '$x_3$', '$x_4$',
                 '$x_5$', '$x_6$', '$x_7$', '$x_8$',
                 '$x_9$', '$x_{10}$', '$x_{11}$' ] )
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')
# ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba )
# --- END
 
# ax.bar3d(xpos, ypos, zpos, dx, dy, dz)
# ax.set_xticklabels(countries)
# ax.set_yticklabels(years)

ax.set_xlabel( 'Row' )
ax.set_ylabel( 'Column' )
ax.set_zlabel( r'Normalized % change: $|\delta(min, max) \ / \ min|$' )

plt.show()

# ======================================
# --- 3D BAR COLORMAP PLOTS (B MATRIX)
# ======================================

delta_B = np.zeros_like( B_nom )
for ith_Row, ith_Col in np.ndindex(B_nom.shape):
    print( f'(ith_Row, ith_Col) = ({ith_Row}, {ith_Col})' )
    max_elem = B_max[ith_Row, ith_Col]
    min_elem = B_min[ith_Row, ith_Col]
    delta_B[ith_Row, ith_Col] = get_change(max_elem, min_elem)

# Normalize values
B_final = delta_B / np.amax(delta_B)

fig = plt.figure()
ax = plt.axes(projection = "3d")

data = B_final.T
 
numOfRows = data.shape[0]
numOfCols = data.shape[1]
 
xpos = np.arange(0, numOfCols, 1)
ypos = np.arange(0, numOfRows, 1)
xpos, ypos = np.meshgrid(xpos + 0.5, ypos + 0.5)
 
xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros(numOfCols * numOfRows)
 
dx = np.ones(numOfRows * numOfCols) * 0.5
dy = np.ones(numOfCols * numOfRows) * 0.5
dz = data.flatten()

cmap = colormaps['jet'] # Get desired colormap
max_height = np.max(dz)   # get range of colorbars
min_height = np.min(dz)

# scale each z to [0,1], and get their rgb values
rgba = [cmap((k-min_height)/max_height) for k in dz]
ax.set_xticks( [i+1 for i in range(0, numOfCols)],
               [ '$x_1$', '$x_2$', '$x_3$', '$x_4$',
                 '$x_5$', '$x_6$', '$x_7$', '$x_8$',
                 '$x_9$', '$x_{10}$', '$x_{11}$' ] )
ax.set_yticks( [i+1 for i in range(0, numOfRows)], 
               [ '$u_1$', '$u_2$', '$u_3$', '$u_4$' ] )
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')

ax.set_xlabel( 'Row' )
ax.set_ylabel( 'Column' )
ax.set_zlabel( r'Normalized % change: $|\delta(min, max) \ / \ min|$' )

plt.show()

pass

