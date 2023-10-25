from    platform                        import  system
from    pathlib                         import  Path
import  pandas                          as      pd

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
# A_df, B_df, C_df, D_df = model.linearize( as_pdDataFrame=True )

pass

