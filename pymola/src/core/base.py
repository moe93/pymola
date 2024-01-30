'''
Base Pymola object definition

Author      :   Mohammad Odeh
E-mail      :   contact@mohammadodeh.com
Date        :   Oct. 25th, 2023
Modified    :   Oct. 25th, 2020 too and one
'''

from    pyfmi                           import  load_fmu

import  numpy                           as      np
import  pandas                          as      pd

class PymolaObject( object ):
    def __init__( self, fmu ) -> None:
        """
        
        Parameters
        ----------
        fmu:
            Path to Functional Mockup Unit (FMU) 
        """

        self.model = load_fmu( fmu )                    # Load FMU
        self.model.initialize()                         # Initialize model
    
    