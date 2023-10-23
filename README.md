# Pymola
Python for Dymola

## Use Case
Sometimes it is required to sweep over design parameters, simulate, and gather data over and over again.

The use of Python with the Dymola API allows us to automate this process.

## Notes

If using VSCode, you can visualize the data within VSCode by first installing the Jupyter extension. You then need to add a breakpoint somewhere *after* the data you are interested in visualizing is processed by the Python interpreter. Now run the script in Debug mode and go to the debug menu, find the variable you are interested in visualizing and right-click on it, then choose ```'View value in Data Viewer'```.

You can read more on that [here](https://devblogs.microsoft.com/python/python-in-visual-studio-code-january-2021-release/#data-viewer-when-debugging). 


## Using Conda
Make sure to add conda to the PATH variable. Open the Anaconda3 command prompt and type
```
where conda
```

Add the directories listed to PATH. The in VSCode, open a terminal prompt and type ```conda init```. Once you create your conda environment, you should now be able to activate it.

Using conda allows you to utilize PyFMI. To install
```
conda install -c conda-forge pyfmi
```

## FMU Support
You can start the FMPy GUI with
```
python -m fmpy.gui
```

### Using the web app
The FMPy Web App is built with Dash and a great way to share your FMUs with anyone that has a web browser. To start it, run
```
python -m fmpy.webapp <model_name>.fmu
```