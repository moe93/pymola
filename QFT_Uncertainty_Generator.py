'''
Generate uncertainties in the model for QFT bounds.

Author      :   Mohammad Odeh
E-mail      :   contact@mohammadodeh.com
Date        :   Oct. 21st, 2023
Modified    :   Oct. 21st, 2020 too and one
'''

# --- Add the dymola.egg file to path to access the Dymola API
import sys
egg_path = './eggs/dymola.egg'
sys.path.append(egg_path)

# --- Do the rest of the usual imports here
from    platform                            import  system
from    dymola.dymola_interface             import  DymolaInterface
from    dymola.dymola_exception             import  DymolaException
from    pathlib                             import  Path
from    scipy.io                            import  loadmat
import  numpy                               as      np
import  pandas                              as      pd

# --- While Dymola runs on different operating systems, I only need it to run on Windows for personal reasons.
if( system() != "Windows" ): exit

# ==============================================================================
# START HERE
# ==============================================================================

SAVE_PLOTS = True                       # FLAG: if True; save figures to file

if __name__ == '__main__':

    # --- Current path where this script is running from
    currentPath = Path(__file__).resolve().parent
    # --- Not the best way to create a path, but will suffice for now
    modelPath = Path( "C:\\", "Users", "mo780715", "Desktop", "fowt", "FOWT", "package.mo" )
    # --- Name of model we are interested in simulating
    modelName = "FOWT.Tests.Experimental.Linearize.TurbineMIMO_QFT.Regime3.LinearModels.FOCAL_MIMO_Regime3_embedded_GenTrq"

    # Create empty dymola object
    dymola = None
    try:
        # Instantiate Dymola interface and start
        dymola = DymolaInterface()      

        # # --- Open model in Dymola and check its return value
        # print( "[INFO] Opening model." )

        # openModel = dymola.openModel( modelPath.__str__()   ,   # Path to model
        #                               mustRead = False      ,   # Don't re-read
        #                               changeDirectory = False ) # Keep directory

        # # If we failed to open the file, throw error and exit.
        # if( not openModel ):
        #     print( "Could not open file. Below is the error log." )
        #     print( dymola.getLastErrorLog() )
        #     exit(1)
        # else:
        #     print( "[INFO] Model found and opened.")
        
        # # --- Linearize model
        # print( "[INFO] Linearizing model." )

        # linearModel = dymola.linearizeModel( modelName,
        #                                      startTime  = 0.0,
        #                                      stopTime   = 0.1 )
        # if( not linearModel ):
        #     print( "[INFO] Could not linearize. Below is the error log." )
        #     print( dymola.getLastErrorLog() )
        #     exit(1)
        # else:
        #     print( "[INFO] Linearization successful." )

        # --- Explore generated .mat file
        linearMat   = loadmat( "dslin.mat" )
        nStates     = (linearMat["nx"])[0][0]           # Total states (as int)
        ABCD        = linearMat["ABCD"]                 # Extract ABCD matrix
        A           = ABCD[0:nStates , 0:nStates ]      # [A] matrix
        B           = ABCD[0:nStates , nStates:  ]      # [B] matrix
        C           = ABCD[nStates:  , 0:nStates ]      # [C] matrix
        D           = ABCD[nStates:  , nStates:  ]      # [D] matrix

        # Get states, inputs, and outputs names'
        xuyNames    = linearMat["xuyName"]
        xStart      = 0         ;   xStop = nStates
        uStart      = xStop     ;   uStop = uStart+B.shape[1]
        yStart      = uStop
        xNames      = xuyNames[xStart:xStop].tolist()   # States  (x) names
        uNames      = xuyNames[uStart:uStop].tolist()   # Inputs  (u) names
        yNames      = xuyNames[yStart:     ].tolist()   # Outputs (y) names

        # Clean up names (remove whitespace then remove \x00 encoding)
        for index, name in enumerate( xNames ):
            xNames[ index ] = name.strip().rstrip( '\x00' )
        
        for index, name in enumerate( uNames ):
            uNames[ index ] = name.strip().rstrip( '\x00' )

        for index, name in enumerate( yNames ):
            yNames[ index ] = name.strip().rstrip( '\x00' )

        # Convert to pd dataframes
        A_df     = pd.DataFrame( A, index=xNames, columns=xNames )
        B_df     = pd.DataFrame( B, index=xNames, columns=uNames )
        C_df     = pd.DataFrame( C, index=yNames, columns=xNames )
        D_df     = pd.DataFrame( D, index=yNames, columns=uNames )

    except DymolaException as ex:
        print(("Error: " + str(ex)))

    finally:
        if dymola is not None:
            dymola.close()
            dymola = None
