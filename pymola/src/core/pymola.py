'''
Using the PyFMI, we sweep over parameters and vary variables for creating linearized models for QFT controller design

Author      :   Mohammad Odeh
E-mail      :   contact@mohammadodeh.com
Date        :   Oct. 25th, 2023
Modified    :   Oct. 25th, 2020 too and one
'''

# --- Do the rest of the usual imports here
from    .base                           import  PymolaObject
from    ..util.Plotter                  import  Plotter

import  numpy                           as      np
import  pandas                          as      pd


class Pymola( PymolaObject, Plotter ):

    def __init__( self, fmu ) -> None:
        """
        
        Parameters
        ----------
        fmu:
            Path to Functional Mockup Unit (FMU) 
        """
        
        # Initialize inherited class
        PymolaObject.__init__( self, fmu )
        Plotter.__init__( self )

    def get_variables( self ) -> list:
        """
        
        Get model variables and format into a readable manner

        """

        self.modelVars = self.model.get_model_variables()
        return self.modelVars


    def get_states( self ) -> list:
        """
        
        Get model states and format into a readable manner

        """
        modelStates = self.model.get_states_list()      # Model states

        # --- Extract names
        self.xNames = [None] * len( modelStates )       # Init list of size
        for ndx, name in enumerate( modelStates ):      # Loop over list
            self.xNames[ ndx ] = name                   #   Populate
        del modelStates                                 # Delete variable

        return self.xNames


    def get_inputs( self ) -> list:
        """
        
        Get model inputs and format into a readable manner
        
        """
        modelInputs = self.model.get_input_list()       # Model inputs

        # --- Extract inputs
        self.uNames = [None] * len( modelInputs )       # Init list of size
        for ndx, name in enumerate( modelInputs ):      # Loop over list
            self.uNames[ ndx ] = name                   #   Populate
        del modelInputs                                 # Delete variable

        return self.uNames

    def get_outputs( self ) -> list:
        """
        
        Get model outputs and format into a readable manner
        
        """

        modelOutputs= self.model.get_output_list()      # Model outputs

        # --- Extract outputs
        self.yNames = [None] * len( modelOutputs )      # Init list of size
        for ndx, name in enumerate( modelOutputs ):     # Loop over list
            self.yNames[ ndx ] = name                   #   Populate
        del modelOutputs                                # Delete variable

        return self.yNames
    
    def get_param_value( self, param_name: str ) -> int | float | str:
        """
        
        Get value of a specific model parameter

        Parameters
        ----------
        param_name:
            String containing name of parameter of interest
        
        """
    
        # Get references of variables of interest that we want to manipulate
        param_ref   = self.modelVars[ param_name ].value_reference
        # Get values from references
        param_val   = self.model.get_real( param_ref )

        return param_val

    def set_param_value( self, param_name: str, new_val: int|float ) -> None:
        """
        
        Set value of a specific model parameter

        Parameters
        ----------
        param_name:
            String containing name of parameter of interest
        new_val:
            Integer or float (Modelica Integer or Real) for new parameter value
        """
    
        # Get references of variables of interest that we want to manipulate
        param_ref   = self.modelVars[ param_name ].value_reference

        # Set new value
        if isinstance( new_val, int ):
            self.model.set_integer( param_ref, new_val )
        elif isinstance( new_val, float ):
            self.model.set_real( param_ref, new_val )
        else:
            Exception( 'Invalid input. Only int and float are permitted' )

    
    def linearize( self, as_pdDataFrame: bool = False ) -> tuple[np.ndarray|pd.DataFrame, np.ndarray|pd.DataFrame, np.ndarray|pd.DataFrame, np.ndarray|pd.DataFrame]:
        """
        
        PyFMI linearizes model internally with the call of get_state_space_representation()

        Parameters
        ----------
        as_pdDataFrame (optional):
            If True, return as a pandas dataframe. Default False.

        """
        
        # --- Get S.S. representation and extract A, B, C, D matrices
        stateSpace  = self.model.get_state_space_representation()
        A = stateSpace[0].A;    B = stateSpace[1].A
        C = stateSpace[2].A;    D = stateSpace[3].A

        if( as_pdDataFrame ):
            # Convert to pd dataframes
            A   = pd.DataFrame( A, index=self.xNames, columns=self.xNames )
            B   = pd.DataFrame( B, index=self.xNames, columns=self.uNames )
            C   = pd.DataFrame( C, index=self.yNames, columns=self.xNames )
            D   = pd.DataFrame( D, index=self.yNames, columns=self.uNames )
        
        return A, B, C, D
    
    def sweep( self, param_names_vals: dict, TOL: float = 1e-6 ):
        """
        
        Sweep over a list of parameters

        Parameters
        ----------
        param_names_vals:
            Dictionary containing parameter name as dict key and desired values as the dict value.
        TOL:
            If below TOL, set element to zero.

        """
        # # Get parameters and their values
        # param, val = self._extract_dict( param_names_vals )

        # Loop over parameters and their values
        for param_name, param_val in param_names_vals.items():
            
            # Get number of variations
            n_depth = len( param_val )
            # This is the first run for this (key, val) pair
            init_run = True

            # Fix one parameter and loop over it's variations
            for ndx, value in enumerate(param_val):
                self.set_param_value( param_name, value )
                A, B, C, D  = self.linearize()
                # Add depth to matrices (3rd dim)
                A = np.expand_dims(A, axis=0);  B = np.expand_dims(B, axis=0)
                C = np.expand_dims(C, axis=0);  D = np.expand_dims(D, axis=0)
                # Remove numbers below threshold (due to numerical limitations)
                A[np.abs(A) < TOL] = 0;     B[np.abs(B) < TOL] = 0
                C[np.abs(C) < TOL] = 0;     D[np.abs(D) < TOL] = 0

                if( init_run ):
                    # Initialize 3D matrices for data storage
                    A_3D = np.zeros_like( A );  B_3D = np.zeros_like( B )
                    C_3D = np.zeros_like( C );  D_3D = np.zeros_like( D )

                    # Disable init_run
                    init_run = False
                    
                # Store A, B, C, D in the ndx-th depth of the *_3D matrix
                A_3D = np.concatenate((A, A_3D), axis=0)
                B_3D = np.concatenate((B, B_3D), axis=0)
                C_3D = np.concatenate((C, C_3D), axis=0)
                D_3D = np.concatenate((D, D_3D), axis=0)

        return A_3D[:-1], B_3D[:-1], C_3D[:-1], D_3D[:-1]
    