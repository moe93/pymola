'''
Utility to plot 3D colormapped bar charts and/or QFT templates

Author      :   Mohammad Odeh
E-mail      :   contact@mohammadodeh.com
Date        :   Oct. 25th, 2023
Modified    :   Oct. 25th, 2020 too and one
'''

import  numpy                           as      np

import  matplotlib.pyplot               as      plt
from    matplotlib                      import  colormaps # Import colormaps!

plt.ion()

class Plotter( object ):

    def __init__( self ):
        pass
    

    @staticmethod
    def _check_matrix( mat: np.ndarray ) -> None:
        """
        
        Check matrix type and dimensionality

        Parameters
        ----------
        mat:
            Matrix to check.

        """
        # Check if matrix is np.ndarray or not
        if( isinstance(mat, np.ndarray) is not True):
            Exception( 'Matrix is not a np.ndarray' )

        # Check if matrix has correct dimensionality
        if( len(mat) != 3):
            Exception( f'Matrix is {len(mat)}D matrix, must be a 3D matrix' )


    @staticmethod
    def get_change( max_elem, min_elem ):
        if max_elem == min_elem:
            return 0
        try:
            if(min_elem == 0): return 0
            else: return (abs(max_elem - min_elem) / abs(min_elem)) * 100.0
        except ZeroDivisionError:
            # return float('inf')
            return 0
    

    def plot_bar3d_All( self, A: np.ndarray, B: np.ndarray, C: np.ndarray, D: np.ndarray ) -> None:
        """
        
        Plot all matrices (A, B, C, D) in 3D colormapped bar representation

        Parameters
        ----------
        A:
            (n-x-n) state-space matrix.

        """
        pass
    

    def plot_bar3d_A( self, A: np.ndarray, title: str, variation: list ) -> None:
        """
        
        Plot A matrix in 3D colormapped bar representation

        Parameters
        ----------
        A:
            (Z x N x N) state-space matrix, where Z is the depth (number of variations for parameter `title`)
        title:
            Title of figure window
        variation:
            List of varied values for parameter `title`

        """
        self._check_matrix( A )

        for ndx, angle in enumerate( A ):
            # Get A at angle
            A_angle = A[ ndx ]

            fig = plt.figure( num=f'{title} = {variation[ndx]}' )
            ax = plt.axes(projection = "3d")

            data = A_angle.T
            
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
                       [ '$x_1$', '$x_2$', '$x_3$', '$x_4$',
                         '$x_5$', '$x_6$', '$x_7$', '$x_8$',
                         '$x_9$', '$x_{10}$', '$x_{11}$' ] )
            ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')

            ax.set_xlabel( 'Row' )
            ax.set_ylabel( 'Column' )
            ax.set_zlabel( r'Normalized % change: $|\delta(min, max) \ / \ min|$' )

            plt.show()

    
    # def plot_bar3d_a( self, A: np.ndarray, B: np.ndarray, C: np.ndarray, D: np.ndarray ) -> None:
    #     """
        
    #     Extract key, value pair from input dict of parameters and desired values

    #     Parameters
    #     ----------
    #     param_names_vals:
    #         Dictionary containing parameter name as dict key and desired values as the dict value.

    #     """
    #     for ndx, angle in enumerate( azimuth ):
    #     # Get A at angle
    #     A_angle = B_3D[ ndx ]

    #     # Get change from average
    #     A_temp = np.zeros_like( B_mean )
    #     for ith_Row, ith_Col in np.ndindex(B_mean.shape):
    #         crnt_elem = A_angle[ith_Row, ith_Col]
    #         mean_elem = A_mean[ith_Row, ith_Col]
    #         A_temp[ith_Row, ith_Col] = get_change(crnt_elem, mean_elem)

    #     # Normalize values
    #     AA = A_temp / np.amax(A_temp)

    #     fig = plt.figure(num=f'Azimuth = {angle}')
    #     ax = plt.axes(projection = "3d")

    #     data = AA.T
        
    #     numOfRows = data.shape[0]
    #     numOfCols = data.shape[1]
        
    #     xpos = np.arange(0, numOfCols, 1)
    #     ypos = np.arange(0, numOfRows, 1)
    #     xpos, ypos = np.meshgrid(xpos + 0.5, ypos + 0.5)
        
    #     xpos = xpos.flatten()
    #     ypos = ypos.flatten()
    #     zpos = np.zeros(numOfCols * numOfRows)
        
    #     dx = np.ones(numOfRows * numOfCols) * 0.5
    #     dy = np.ones(numOfCols * numOfRows) * 0.5
    #     dz = data.flatten()

    #     cmap = colormaps['jet'] # Get desired colormap
    #     max_height = np.max(dz)   # get range of colorbars
    #     min_height = np.min(dz)

    #     # scale each z to [0,1], and get their rgb values
    #     rgba = [cmap((k-min_height)/max_height) for k in dz]
    #     ax.set_xticks( [i+1 for i in range(0, numOfCols)],
    #                 [ '$x_1$', '$x_2$', '$x_3$', '$x_4$',
    #                     '$x_5$', '$x_6$', '$x_7$', '$x_8$',
    #                     '$x_9$', '$x_{10}$', '$x_{11}$' ] )
    #     # ax.set_yticks( [i+1 for i in range(0, numOfRows)],
    #     #            [ '$x_1$', '$x_2$', '$x_3$', '$x_4$',
    #     #              '$x_5$', '$x_6$', '$x_7$', '$x_8$',
    #     #              '$x_9$', '$x_{10}$', '$x_{11}$' ] )
    #     ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')

    #     ax.set_xlabel( 'Row' )
    #     ax.set_ylabel( 'Column' )
    #     ax.set_zlabel( r'Normalized % change: $|\delta(min, max) \ / \ min|$' )

    #     plt.show()

    # def plot_bar3d_a( self, A: np.ndarray, B: np.ndarray, C: np.ndarray, D: np.ndarray ) -> None:
    #     """
        
    #     Extract key, value pair from input dict of parameters and desired values

    #     Parameters
    #     ----------
    #     param_names_vals:
    #         Dictionary containing parameter name as dict key and desired values as the dict value.

    #     """
    #     for ndx, angle in enumerate( azimuth ):
    #     # Get A at angle
    #     A_angle = B_3D[ ndx ]

    #     # Get change from average
    #     A_temp = np.zeros_like( B_mean )
    #     for ith_Row, ith_Col in np.ndindex(B_mean.shape):
    #         crnt_elem = A_angle[ith_Row, ith_Col]
    #         mean_elem = A_mean[ith_Row, ith_Col]
    #         A_temp[ith_Row, ith_Col] = get_change(crnt_elem, mean_elem)

    #     # Normalize values
    #     AA = A_temp / np.amax(A_temp)

    #     fig = plt.figure(num=f'Azimuth = {angle}')
    #     ax = plt.axes(projection = "3d")

    #     data = AA.T
        
    #     numOfRows = data.shape[0]
    #     numOfCols = data.shape[1]
        
    #     xpos = np.arange(0, numOfCols, 1)
    #     ypos = np.arange(0, numOfRows, 1)
    #     xpos, ypos = np.meshgrid(xpos + 0.5, ypos + 0.5)
        
    #     xpos = xpos.flatten()
    #     ypos = ypos.flatten()
    #     zpos = np.zeros(numOfCols * numOfRows)
        
    #     dx = np.ones(numOfRows * numOfCols) * 0.5
    #     dy = np.ones(numOfCols * numOfRows) * 0.5
    #     dz = data.flatten()

    #     cmap = colormaps['jet'] # Get desired colormap
    #     max_height = np.max(dz)   # get range of colorbars
    #     min_height = np.min(dz)

    #     # scale each z to [0,1], and get their rgb values
    #     rgba = [cmap((k-min_height)/max_height) for k in dz]
    #     ax.set_xticks( [i+1 for i in range(0, numOfCols)],
    #                 [ '$x_1$', '$x_2$', '$x_3$', '$x_4$',
    #                     '$x_5$', '$x_6$', '$x_7$', '$x_8$',
    #                     '$x_9$', '$x_{10}$', '$x_{11}$' ] )
    #     # ax.set_yticks( [i+1 for i in range(0, numOfRows)],
    #     #            [ '$x_1$', '$x_2$', '$x_3$', '$x_4$',
    #     #              '$x_5$', '$x_6$', '$x_7$', '$x_8$',
    #     #              '$x_9$', '$x_{10}$', '$x_{11}$' ] )
    #     ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')

    #     ax.set_xlabel( 'Row' )
    #     ax.set_ylabel( 'Column' )
    #     ax.set_zlabel( r'Normalized % change: $|\delta(min, max) \ / \ min|$' )

    #     plt.show()

    # def plot_bar3d_a( self, A: np.ndarray, B: np.ndarray, C: np.ndarray, D: np.ndarray ) -> None:
    #     """
        
    #     Extract key, value pair from input dict of parameters and desired values

    #     Parameters
    #     ----------
    #     param_names_vals:
    #         Dictionary containing parameter name as dict key and desired values as the dict value.

    #     """
    #     for ndx, angle in enumerate( azimuth ):
    #     # Get A at angle
    #     A_angle = B_3D[ ndx ]

    #     # Get change from average
    #     A_temp = np.zeros_like( B_mean )
    #     for ith_Row, ith_Col in np.ndindex(B_mean.shape):
    #         crnt_elem = A_angle[ith_Row, ith_Col]
    #         mean_elem = A_mean[ith_Row, ith_Col]
    #         A_temp[ith_Row, ith_Col] = get_change(crnt_elem, mean_elem)

    #     # Normalize values
    #     AA = A_temp / np.amax(A_temp)

    #     fig = plt.figure(num=f'Azimuth = {angle}')
    #     ax = plt.axes(projection = "3d")

    #     data = AA.T
        
    #     numOfRows = data.shape[0]
    #     numOfCols = data.shape[1]
        
    #     xpos = np.arange(0, numOfCols, 1)
    #     ypos = np.arange(0, numOfRows, 1)
    #     xpos, ypos = np.meshgrid(xpos + 0.5, ypos + 0.5)
        
    #     xpos = xpos.flatten()
    #     ypos = ypos.flatten()
    #     zpos = np.zeros(numOfCols * numOfRows)
        
    #     dx = np.ones(numOfRows * numOfCols) * 0.5
    #     dy = np.ones(numOfCols * numOfRows) * 0.5
    #     dz = data.flatten()

    #     cmap = colormaps['jet'] # Get desired colormap
    #     max_height = np.max(dz)   # get range of colorbars
    #     min_height = np.min(dz)

    #     # scale each z to [0,1], and get their rgb values
    #     rgba = [cmap((k-min_height)/max_height) for k in dz]
    #     ax.set_xticks( [i+1 for i in range(0, numOfCols)],
    #                 [ '$x_1$', '$x_2$', '$x_3$', '$x_4$',
    #                     '$x_5$', '$x_6$', '$x_7$', '$x_8$',
    #                     '$x_9$', '$x_{10}$', '$x_{11}$' ] )
    #     # ax.set_yticks( [i+1 for i in range(0, numOfRows)],
    #     #            [ '$x_1$', '$x_2$', '$x_3$', '$x_4$',
    #     #              '$x_5$', '$x_6$', '$x_7$', '$x_8$',
    #     #              '$x_9$', '$x_{10}$', '$x_{11}$' ] )
    #     ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')

    #     ax.set_xlabel( 'Row' )
    #     ax.set_ylabel( 'Column' )
    #     ax.set_zlabel( r'Normalized % change: $|\delta(min, max) \ / \ min|$' )

    #     plt.show()

# ==============================================================================
#   --- TEST CLASS
# ==============================================================================
if __name__ == '__main__':

    pass