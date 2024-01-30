import  numpy                           as      np

N_DEPTH = 3
N_ROWS  = 5
N_COLS  = 5

A = np.zeros( (N_DEPTH, N_ROWS, N_COLS), dtype=np.float32 )

A1 = np.ones( (N_ROWS, N_COLS) ) * 1; A1[0,0] = 10; A1[1,0] = -10
A2 = np.ones( (N_ROWS, N_COLS) ) * 2; A2[1,1] = 20; A2[2,1] = -20
A3 = np.ones( (N_ROWS, N_COLS) ) * 3; A3[2,2] = 30; A3[0,2] = -30
A_nom = np.zeros_like( A1 )

A[0] = A1; A[1] = A2; A[2] = A3

A_max = A.max(axis=0)
A_min = A.min(axis=0)

# Find percent error from nominal
def get_change(current, previous):
    if current == previous:
        return 0
    try:
        if(previous == 0): return 0
        else: return (abs(current - previous) / abs(previous)) * 100.0
    except ZeroDivisionError:
        # return float('inf')
        return 0

del_A = np.zeros_like( A_nom )
for ith_Row, ith_Col in np.ndindex(A_nom.shape):
    print( f'(ith_Row, ith_Col) = ({ith_Row}, {ith_Col})' )
    current = A_max[ith_Row, ith_Col]
    nominal = A_min[ith_Row, ith_Col]
    del_A[ith_Row, ith_Col] = get_change(current, nominal)

# Normalize values
A_final = del_A / np.amax(del_A)

# # ======================================
# # --- 3D BAR COLORMAP PLOTS (EXAMPLE)
# # See: https://coderslegacy.com/python/3d-bar-chart-matplotlib/
# # ======================================
# import  matplotlib.pyplot               as  plt
# import  matplotlib.cm                   as  cm          # Import colormap stuff!

# # xedges = np.array( [i for i in range(0, A.shape[1]+1)] )
# # yedges = np.array( [i for i in range(0, A.shape[0]+1)] )

# fig = plt.figure()
# ax = plt.axes(projection = "3d")
 
# countries = [" ","Australia", " ","Brazil", " ","Canada", " ","France"]
# # data = np.array([[1.8, 20.4, 2.1, 1.6],
# #                  [1.3, 18.1, 1.2, 2.3],
# #                  [0.8, 27.8, 1.4, 1.3]])
# data = np.array([[1.8, 20.4, 2.1, 1.6],
#                  [1.3, 18.1, 1.2, 2.3],
#                  [0.8, 27.8, 1.4, 1.3]])
# years = [None, None, 2005, None, 2010, None, 2015]
 
# numOfCols = 4
# numOfRows = 3
 
# xpos = np.arange(0, numOfCols, 1)
# ypos = np.arange(0, numOfRows, 1)
# xpos, ypos = np.meshgrid(xpos + 0.5, ypos + 0.5)
 
# xpos = xpos.flatten()
# ypos = ypos.flatten()
# zpos = np.zeros(numOfCols * numOfRows)
 
# dx = np.ones(numOfRows * numOfCols) * 0.5
# dy = np.ones(numOfCols * numOfRows) * 0.5
# dz = data.flatten()
 
# ax.bar3d(xpos, ypos, zpos, dx, dy, dz)
# ax.set_xticklabels(countries)
# ax.set_yticklabels(years)
 
# ax.set_xlabel('Countries')
# ax.set_ylabel('Over the years')
# ax.set_zlabel('Number of Homicide cases')

# plt.show()

# ======================================
# --- 3D BAR COLORMAP PLOTS
# ======================================
import  matplotlib.pyplot               as      plt
from    matplotlib                      import  colormaps # Import colormaps!

# xedges = np.array( [i for i in range(0, A.shape[1]+1)] )
# yedges = np.array( [i for i in range(0, A.shape[0]+1)] )

fig = plt.figure()
ax = plt.axes(projection = "3d")
 
countries = [" ","Australia", " ","Brazil", " ","Canada", " ","France"]

data = A_final
years = [None, None, 2005, None, 2010, None, 2015]
 
numOfCols = data.shape[0]
numOfRows = data.shape[1]
 
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
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=rgba, zsort='average')
# --- END
 
# ax.bar3d(xpos, ypos, zpos, dx, dy, dz)
# ax.set_xticklabels(countries)
# ax.set_yticklabels(years)

# plt.rc('text.latex', preamble=r'\usepackage{textgreek}')
# plt.rc('text', usetex=True)
ax.set_xlabel( 'Rows' )
ax.set_ylabel( 'Columns' )
ax.set_zlabel( r'Normalized % change: $|\delta(min, max) \ / \ min|$' )

plt.show()

pass