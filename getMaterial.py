import openmc

def getMaterial(materials, material):
	for mat in materials:
		if mat.name == material:
			return mat
			break
