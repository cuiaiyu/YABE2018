"""
setting for read data to specify the blog
"""
from YABE.settings import PROJECT_ROOT
from os import path

"""
Path to user-self-defined data file (.xml file)
"""
#User's basic info file, like name, email and etc
BASIC_INFO_PATH=path.join(PROJECT_ROOT,"data/basic.xml").replace('\\', '/')

#User's project info file
PROJECT_INFO_PATH=path.join(PROJECT_ROOT,"data/projects.xml").replace('\\', '/')
