import cubit
import os
import inspect

# if this fails to mesh, try importing the step into cubit,
# click the hammer button under geometry, then select volumes
# then heal -> autoheal and let that try to fix it, worked for me
# setting reheal to true will automate this

def makeUmesh(inName, ratio = 100, angle = 5, reheal=False):
	"""
	Attempts to mesh step file using coarse mesh settings for the surface,
	and tetmeshing the interior. This is particularly for thin volumes
	in which large, flat elements are desired.

	Export to exodus then attempts to mbconvert it to h5m.

	Deletes the exodus file automatically so watch out if you don't want that

	Arguments:
		inName (str): path to step file
		ratio (float): cubit coarse mesh setting
		angle (float): cubit coarse mesh setting
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

	cubit.cmd(f'set trimesher coarse on ratio {ratio} angle {angle}')
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