import os
import errno
import unpack_tar_file as utar
import table_parser as tp
import subprocess
import shutil
import xml.etree.ElementTree as ET

''' Take the tar.gz file and extract it to a specific place '''
# TODO: The tar.gz file should be selected by user
fname = 'D:/EricDantas/Thyssenkrupp/PolySpace_3.18.33.0_RC1_2018_09_06-17_59_18.tar.gz'

# TODO: The destination path should be selected by user
path = 'D:/EricDantas/Thyssenkrupp/Temp'

# TODO: Verify if it was already extracted or if the user would like to overwrite all
# unpack_file = utar.UnpackTarFile(fname, path)

''' Find the html report and extract its component table to get the TAG and ID of the component '''
fhtml = open(path + '/DailyBuild/report/index.html')
xhtml = fhtml.read().decode('utf-8')
fhtml.close()

# TODO: The component should be selected by user
component = 'ActuatorSupervisor'
list_components = [component, 'Gen_R10_'+component]
tag = ''
id = ''

p = tp.TableParser()
p.feed(xhtml)
for i in p.tables[2]:  # 2nd table contains the list of components and its info
    if any(x in list_components for x in i):
        # if 'Gen_R10_'+component in i:
        tag = i[3]
        id = i[4]
        print 'Component: ', component
        print 'TAG: ', tag
        print 'ID: ', id

''' Create/update first infrastructure folder (M:\Polyspace\ComponentName) '''
# TODO: normally, it will be in M drive, but it should be choose by user
# TODO: Create a def or put it in a separeted file
directory = 'D:/EricDantas/Thyssenkrupp/Temp/Polyspace/'+component
try:
    os.makedirs(directory)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

''' Checkout SVN: ModuleTest, Polyspace and Source (by Trunk or by specific tag) '''
# TODO: Create a def or put it in a separeted file
# svn = subprocess.Popen("svn info svn://xx.xx.xx.xx/project/trunk | grep \"Revision\" | awk '{print $2}'", stdout=subprocess.PIPE, shell=True)
# (output, err) = svn.communicate()
# print "Revision is", output

''' Copy files and folders from the ID component to SVN Checkout folder '''
# TODO: Create a def or put it in a separeted file
from distutils.dir_util import copy_tree
import distutils
try:
    copy_tree(path + '/SwCs/CID_' + id, directory)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

''' Duplicate the proj file according to variants '''
# TODO: Create a def or put it in a separeted file
directory += '/PolySpace'
dirlist = [item for item in os.listdir(directory) if os.path.isdir(os.path.join(directory, item))]
# Getting the proj file name
# TODO: To refactor this part
file_psprj = directory+'/'+component+'.psprj'
if not os.path.isfile(directory+'/'+component+'.psprj'):
    for f in os.listdir(directory):
        if f.endswith(".psprj"):
            file_psprj = directory+'/'+f

if dirlist > 1:
    for i in dirlist:
        source = directory+'/'+component+'.psprj'
        destination = directory+'/'+component+'_'+i+'.psprj'
        shutil.copy2(source, destination)
        ''' For each proj file, change the path info '''
        tree = ET.parse(destination)
        root = tree.getroot()
        print root.attrib
        print root.attrib.get('path')
