import cubit
import os
import inspect

# if this fails to mesh, try importing the step into cubit,
# click the hammer button under geometry, then select volumes
# then heal -> autoheal and let that try to fix it, worked for me
# setting reheal to true will automate this

def makeUmesh(inName, reheal=False):
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

	cubit.cmd('reset')
	
	#import given step
	cubit.cmd('import step ' + inName + ' heal')

	if reheal:
		cubit.cmd('healer autoheal volume 1 rebuild')
		cubit.cmd('compress')

	cubit.cmd('set trimesher coarse on ratio 100 angle 5')
	cubit.cmd('surface all scheme trimesh')
	
	#set meshing scheme and mesh
	cubit.cmd('volume 1 scheme tetmesh')
	cubit.cmd('mesh volume 1')
	
	cwd = os.getcwd()

	baseName = inName.rstrip('.step')
	outName = baseName+'.e'
	print('export mesh "' + cwd + '/' +outName + '"  overwrite ')

	cubit.cmd('export mesh "' + cwd + '/' +outName + '"  overwrite ')
	
	os.system('mbconvert ' + outName + ' ' + baseName + '.h5m')
	
	os.remove(outName)
	
	cubit.cmd('reset')