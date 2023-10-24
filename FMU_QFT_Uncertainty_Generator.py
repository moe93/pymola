'''
PyFMI based model.
    Generate uncertainties in the model for QFT bounds.

Author      :   Mohammad Odeh
E-mail      :   contact@mohammadodeh.com
Date        :   Oct. 24th, 2023
Modified    :   Oct. 24th, 2020 too and one
'''

# --- Add the dymola.egg file to path to access the Dymola API
import sys
egg_path = './eggs/dymola.egg'
sys.path.append(egg_path)

# --- Do the rest of the usual imports here
from    pyfmi                           import  load_fmu
from    pyfmi                           import  fmi

from    platform                        import  system
from    pathlib                         import  Path
from    scipy.io                        import  loadmat
import  numpy                           as      np
import  pandas                          as      pd

# --- While Dymola runs on different operating systems, I only need it to run on Windows for personal reasons.
if( system() != "Windows" ): exit

# ==============================================================================
# START HERE
# ==============================================================================

SAVE_PLOTS = True                       # FLAG: if True; save figures to file

if __name__ == '__main__':

    # --- Current path where this script is running from
    currentPath = Path(__file__).resolve().parent
    # --- Name of FMU model we are interested in simulating
    fmuName = "FMU_QFT_MIMO_Regime3.fmu"
    # --- Full path to FMU
    fmuPath = Path( currentPath, 'data', fmuName )
    
    try:
        # --- Load FMU and get states, inputs, and outputs
        model       = load_fmu( fmuPath )
        modelVars   = model.get_model_variables()       # All model outputs
        modelStates = model.get_states_list()           # Model states
        modelInputs = model.get_input_list()            # Model inputs
        modelOutputs= model.get_output_list()           # Model outputs

        # --- Extract names of states, inputs, and outputs
        xNames = [None] * len( modelStates )            # Init list of size
        uNames = [None] * len( modelInputs )            # ...
        yNames = [None] * len( modelOutputs )           # ...
        
        for ndx, name in enumerate( modelStates ):      # Loop over list
            xNames[ ndx ] = name                        #   Populate
        for ndx, name in enumerate( modelInputs ):      # ...
            uNames[ ndx ] = name                        #   ...
        for ndx, name in enumerate( modelOutputs ):     # ...
            yNames[ ndx ] = name                        #   ...

        del modelStates                                 # Delete variable
        del modelInputs                                 # ...
        del modelOutputs                                # ...

        # Initialize model
        model.initialize()

        # Get references of variables of interest that we want to manipulate
        phi_ref     = modelVars['fMU_linHub.hub_revolute.phi'].value_reference
        omega_ref   = modelVars['fMU_linHub.hub_revolute.w'  ].value_reference

        # Get values from references
        phi         = model.get_real( phi_ref   )
        omega       = model.get_real( omega_ref )

        # --- Get S.S. representation and extract A, B, C, D matrices
        stateSpace  = model.get_state_space_representation()
        A = stateSpace[0].A;    B = stateSpace[1].A
        C = stateSpace[2].A;    D = stateSpace[3].A

        # Convert to pd dataframes
        A_df     = pd.DataFrame( A, index=xNames, columns=xNames )
        B_df     = pd.DataFrame( B, index=xNames, columns=uNames )
        C_df     = pd.DataFrame( C, index=yNames, columns=xNames )
        D_df     = pd.DataFrame( D, index=yNames, columns=uNames )


        # ======================================================================
        # ---   Change rotor speed and re-linearize
        # ======================================================================
        model.set_real( omega_ref, omega*1.075 )
        omega_updated = model.get_real( omega_ref )
        # --- Get S.S. representation and extract A, B, C, D matrices
        stateSpace  = model.get_state_space_representation()
        A = stateSpace[0].A;    B = stateSpace[1].A
        C = stateSpace[2].A;    D = stateSpace[3].A


    # except DymolaException as ex:
    #     print(("Error: " + str(ex)))

    finally:
        pass
