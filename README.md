# Assessing the impacts of urban golf courses on access to greenspace in the United States

This repository contains the  example materials for GEOG490. 

## Run the lecture notes interactively

The best way to get the materials (including homework) is the use [git](https://git-scm.com/) to [clone this repository](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository). If you don't have git already on you computer, it is easy to install on all platforms following [these instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

From the command line, run the command

```bash
git clone https://github.com/JohnnyRyan1/geospatial_data_science
```

If you are not a fan of the command line, there are plent of [graphical interfaces to git](https://git-scm.com/download/gui/linux) available.

Once you have the repository cloned, you can update it as new lectures come out by running

```bash
git pull origin master
```

If for some reason you can't get git working, the alternative is to use the link to the right to "Download Zip". The disadvantage here is that you will have to re-download every time the repo is updated.

In order to actually execute the code in the notebooks, you need to have the necessary python packages installed.
The recommended way to do this is to install the [anaconda python distribution](https://www.anaconda.com/download/) together with the [conda package management utility](https://conda.io/docs/).
For more depth, you can read my [detailed intstructions for installing python](https://rabernat.github.io/research_computing/python.html).

This repository includes an [environment file](https://github.com/JohnnyRyan1/geospatial_data_science/blob/environment.yml) which you can use to set up your python environment. To install this environment, type the following

```bash
cd geospatial_data_science
conda env create -f environment.yml
```

This will create a new environment called `geospatial_data_science`. To activate this environment, type

```bash
source activate geospatial_data_science
```

Now install the OSMnx, which is a python module we use to access OSM data.

```bash
pip install osmnx
```

The notebooks can be viewed and run using the [jupyter notebook](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html) application. To launch the notebook interface, just type

```bash
jupyter notebook
```

When you are done working with the notebooks, close the notebook app and, if you wish, deactive the environment by typing

```bash
source deactivate
```
