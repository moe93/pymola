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
# --- 3D BAR COLORMAP PLOTS
# ======================================
import  matplotlib.pyplot               as  plt
import  matplotlib.cm                   as  cm          # Import colormap stuff!


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x, y = np.random.rand(2, 100) * 4
hist, xedges, yedges = np.histogram2d(x, y, bins=4, range=[[0, 4], [0, 4]])

# Construct arrays for the anchor positions of the 16 bars.
# Note: np.meshgrid gives arrays in (ny, nx) so we use 'F' to flatten xpos,
# ypos in column-major order. For numpy >= 1.7, we could instead call meshgrid
# with indexing='ij'.
xpos, ypos = np.meshgrid(xedges[:-1] + 0.25, yedges[:-1] + 0.25)
xpos = xpos.flatten('F')
ypos = ypos.flatten('F')
zpos = np.zeros_like(xpos)

# Construct arrays with the dimensions for the 16 bars.
dx = 0.5 * np.ones_like(zpos)
dy = dx.copy()
dz = hist.flatten()

cmap = cm.get_cmap('jet') # Get desired colormap
max_height = np.max(dz)   # get range of colorbars
min_height = np.min(dz)

# scale each z to [0,1], and get their rgb values
rgba = [cmap((k-min_height)/max_height) for k in dz] 

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')

plt.show()

pass

