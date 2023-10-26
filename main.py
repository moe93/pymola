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

A, B, C, D = model.linearize()
A_df, B_df, C_df, D_df = model.linearize( as_pdDataFrame=True )

# Sweep over azimuth angle
azimuth = [ i for i in range(0, 360, 30)]

n_depth = len( azimuth )
A_3D = np.zeros( (n_depth, A.shape[0], A.shape[1]), dtype=np.float32 )
B_3D = np.zeros( (n_depth, B.shape[0], B.shape[1]), dtype=np.float32 )
C_3D = np.zeros( (n_depth, C.shape[0], C.shape[1]), dtype=np.float32 )
D_3D = np.zeros( (n_depth, D.shape[0], D.shape[1]), dtype=np.float32 )

for ndx, angle in enumerate( azimuth ):
    model.set_param_value( paramNames[0], angle )
    A, B, C, D  = model.linearize()
    A_3D[ ndx ] = A;    B_3D[ ndx ] = B
    C_3D[ ndx ] = C;    D_3D[ ndx ] = D

pass

