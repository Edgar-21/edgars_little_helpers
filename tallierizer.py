import openmc
import numpy as np

def calcDPAIron(power, material, volumes, dpaTally, mean = None, stddev = None):
	"""
	Input:
	dpaTally: Cell tally object with iron nuclide filter scoring damage energy eV/source
	power: float, power of source Watts
	material: material object where tally is scored
	volume: volume where tallly is scored
	if dpaTally is None:
	mean: mean damage energy at each mesh element (binned by nuclide)
	stdev: stdev of the same
	volumes: volume of each mesh element
	
	returns:
	if dpaTally given:
	DPAmean: sum of displacements per atom per fpy across all nuclides specified in filter
	DPAstddev: stdev of same
	else
	DPAmean: array of sum of DPA per FPY across all nuclides at each mesh element
	DPAstddev: stdev of same
	"""
    
	#calculate DPA per FPY based on the following constants
	Ed = 40 #eV, displacement energy in iron
	displacementEfficiency = 0.8
	energyPerFusion = 17.6e6 #eV
	eVtoJ = 1.60218e-19 #J/eV
	sourceNeutronsPerYear = power/(energyPerFusion*eVtoJ)*60*60*24*365.25

	#atom density
	FeDensity = 0
	for i in dpaTally.nuclides:
		FeDensity += material.get_nuclide_atom_densities()[i]
	FeDensity = FeDensity/(1e-24) #to atoms/cm3
		
	if mean is None:

		#damage energy stats
		damageEnergy = dpaTally.mean.sum() #eV/source
		stDev = dpaTally.std_dev.sum()

		#mean DPA
		displacementsPerSource = damageEnergy*displacementEfficiency/(2*Ed)
		displacementsPerFPY = displacementsPerSource*sourceNeutronsPerYear
		numFe = FeDensity*volumes
		DPAmean = displacementsPerFPY/numFe

		#std dev DPA
		DPAstDev = DPAmean/damageEnergy*stDev

		return DPAmean, DPAstDev
		
	else:
		#damage energy stats
		mean = mean[:,:,0]
		stdDev = stddev[:,:,0]
		damageEnergy = np.zeros(mean[:,0].shape)
		stdDevDamage = np.zeros(stdDev[:,0].shape)
		for i in range(len(damageEnergy)):
			damageEnergy[i] = np.sum(mean[i])
			stdDevDamage[i] = np.sum(stdDev[i])
			
			
		#mean DPA
		displacementsPerSource = damageEnergy*displacementEfficiency/(2*Ed)
		displacementsPerFPY = displacementsPerSource*sourceNeutronsPerYear
		numFe = FeDensity*volumes
		DPAmean = displacementsPerFPY/numFe
		
		#std dev DPA
		DPAstDev = DPAmean/damageEnergy*stdDevDamage
		
		return DPAmean, DPAstDev

def calcHeating(heatingMean, heatingStddev, power, volumes = None):
	"""
	heatingTally: openmcTally with 'heating' scored (ev/source)
	power: power of device, watts
	volume: array of volumes to normalize heating to (mesh.volume)
	
	returns:
	heatingMean heatingStddev: 1xN arrays, units W/cm3 if vol is not none
	heatingMean heatingStddev: float, units of W if vol is none
	"""
	
	#some constants
	energyPerFusion = 17.6e6 #eV
	eVtoJ = 1.60218e-19 #J/eV
	neutronsPerSecond = power/(energyPerFusion*eVtoJ)
	
	if volumes is not None:
		
		volumes = volumes.T.flatten()

		#convert units
		heatingMean = heatingMean*neutronsPerSecond*eVtoJ #w
		heatingStddev = heatingStddev*neutronsPerSecond*eVtoJ #w
		
		heatingMean = np.divide(heatingMean, volumes) #w/cm3
		heatingStddev = np.divide(heatingStddev, volumes) #w/cm3
		
		return heatingMean, heatingStddev
		
	else:
		heatingMean = heatingMean*neutronsPerSecond*eVtoJ #w
		heatingStddev = heatingStddev*neutronsPerSecond*eVtoJ #w
		
		return heatingMean, heatingStddev
		
