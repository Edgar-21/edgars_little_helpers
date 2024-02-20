import cubit
from cad_to_h5m import cad_to_h5m
import os
import inspect
from pymoab import core, types

def makeUmesh(inName):
	"""
	attempts to make mesh 1 element thick
	inName : str of .step file
	outName : str desired name of .cub file
	size : int suggestion for cubit
	"""
	# Retrieve Cubit module directory
	cubit_dir = os.path.dirname(inspect.getfile(cubit))
	# Append plugins directory to Cubit module directory
	cubit_dir = cubit_dir + '/plugins/'
	# Initialize Cubit
	cubit.init([
	    'cubit',
	    '-nojournal',
	    '-nographics',
	    '-information', 'off',
	    '-warning', 'off',
	    '-commandplugindir',
	    cubit_dir
	])
	
	#import given step
	cubit.cmd('import step ' + inName + ' heal')
	
	#set meshing scheme and mesh
	cubit.cmd('volume 1 scheme tetmesh proximity layers on 1')
	cubit.cmd('mesh volume 1')
	
	cwd = os.getcwd()

	baseName = inName.rstrip('.step')
	outName = baseName+'.e'
	print('export mesh "' + cwd + '/' +outName + '"  overwrite ')

	cubit.cmd('export mesh "' + cwd + '/' +outName + '"  overwrite ')
	
	os.system('mbconvert ' + outName + ' ' + baseName + '.h5')
	
	os.remove(outName)

	
