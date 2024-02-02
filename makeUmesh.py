from pymoab import core, types
import cubit
from cad_to_h5m import cad_to_h5m
import os
import inspect

def makeUMesh(inName, outName, size):
	"""
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
	
	cwd = os.getcwd()

	cubit.cmd('import step ' + inName + ' heal')

	inName = inName.rstrip('.step') + '.sat'

	cubit.cmd('export acis ' + inName + ' overwrite')


	cad_to_h5m(
	    files_with_tags=[
		{
		    'cad_filename':inName,
		    'material_tag':'m1',
		    'tet_mesh': 'size ' + str(size)
		}
	    ],
	    h5m_filename='dagmcFromScript.h5m',
	    cubit_path = '/filespace/e/epflug/research/Coreform-Cubit-2021.5/bin/',
	    cubit_filename = outName
	)
	

