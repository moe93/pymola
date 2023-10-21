# Pymola
Python for Dymola

## Use Case
Sometimes it is required to sweep over design parameters, simulate, and gather data over and over again.

The use of Python with the Dymola API allows us to automate this process.

## Notes

If using VSCode, you can visualize the data within VSCode by first installing the Jupyter extension. You then need to add a breakpoint somewhere *after* the data you are interested in visualizing is processed by the Python interpreter. Now run the script in Debug mode and go to the debug menu, find the variable you are interested in visualizing and right-click on it, then choose ```'View value in Data Viewer'```.

You can read more on that [here](https://devblogs.microsoft.com/python/python-in-visual-studio-code-january-2021-release/#data-viewer-when-debugging). 
