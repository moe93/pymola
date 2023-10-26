# Pymola
Python for Dymola

## Use Case
Sometimes it is required to sweep over design parameters, simulate, and gather data over and over again.

The use of Python with the Dymola API allows us to automate this process.

## Notes

If using VSCode, you can visualize the data within VSCode by first installing the Jupyter extension. You then need to add a breakpoint somewhere *after* the data you are interested in visualizing is processed by the Python interpreter. Now run the script in Debug mode and go to the debug menu, find the variable you are interested in visualizing and right-click on it, then choose ```'View value in Data Viewer'```.

You can read more on that [here](https://devblogs.microsoft.com/python/python-in-visual-studio-code-january-2021-release/#data-viewer-when-debugging). 


## Getting started

Be a good person and create a virtual environment[¹](https://realpython.com/python-virtual-environments-a-primer/) and then activate it.
People who don't, only want to watch the world burn.

```
$ python3 -m venv /path/to/new/virtual/environment
$ source /path/to/venv/bin/activate
```

Update pip and install ```pip-tools```[²](https://github.com/jazzband/pip-tools). I only say this because I care about you, complete random stranger.

```
(venv) $ pip install -U pip
(venv) $ pip install pip-tools
(venv) $ pip-sync
```

If you use Windows, first of all ew and shame on you, then you need to prefix your commands with ```python3 -m``` as follows,

```
(venv) PS> python3 -m pip install -U pip
```
etc...


## Using Conda
Make sure to add conda to the PATH variable. Open the Anaconda3 command prompt and type
```
where conda
```

Add the directories listed to PATH. Then in VSCode, open a terminal prompt and type ```conda init```. Once you create your conda environment, you should now be able to activate it.


If using macOS, don't bother with any of that. Simply use
```
brew install --cask anaconda
```

If you don't want the bloated Anaconda installation and don't mind being behind the driver seat, you can use micromamba instead
```
brew install micromamba
```

If using micromamba, it would be a good idea to add an alias to make your life easier. An example on how to do that if you are using macOS/Linux is as follows:
```
echo "alias conda='micromamba'" >> ~/.zshrc
```

Don't forget to create an environment and activate it.
```
conda create -n <env_name>
conda activate <env_name>
conda install -c conda-forge python=<MAJOR.MINOR.PATCH>
```
---

Using conda/micromamba allows you to easily install and use PyFMI from [Modelon](https://github.com/modelon-community/PyFMI). To install
```
conda install -c conda-forge pyfmi
```

In addition, it makes it easier to install FMPy from [CATIA (© Dassault Systèmes)](https://github.com/CATIA-Systems/FMPy)
```
conda install -c conda-forge fmpy
```

## FMU GUI
You can start the FMPy GUI with
```
python -m fmpy.gui
```

### Using the web app
The FMPy Web App is built with Dash and a great way to share your FMUs with anyone that has a web browser. To start it, run
```
python -m fmpy.webapp <model_name>.fmu
```