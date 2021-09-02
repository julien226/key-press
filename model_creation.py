# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
# import main
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import optimization
import step
import interaction
import load
import mesh
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import math

# Substrate geometry parameters
Solidwidth = 0.015
Solidlength = 0.01
Solidextrude = 0.01
Boundarysize = 0.0005
EffSolidwidth = Solidwidth - 2*Boundarysize
EffSolidlength = Solidlength - 2*Boundarysize

# Defect geometry parameters
Defectdepth = 0.0002
Defectlength = 0.006
Defectwidth = 0.006
# Defectpy = 0.0005
# Defectspacing = 0.00025
# Defectcount = int((Solidwidth-2*Defectpy)/(Defectwidth+Defectspacing))
Defectspacing = 0
Defectcountx = 1
Defectcounty = 1
Defectpx = (Solidlength - Defectcountx*Defectlength - Defectcountx*Defectspacing)/2
Defectpy = (Solidwidth - Defectcounty*Defectwidth - Defectcounty*Defectspacing)/2

# Parameter conversion from float to string
swidth = str(Solidwidth)
slength = str(Solidlength)
sdepth = str(Solidextrude)
defdepth = str(Defectdepth)
defwidth = str(Defectwidth)
defpx = str(Defectpx)
defpy = str(Defectpy)

# Transmitter elements geometry
Nbelmtx = 6
Nbelmty = 6
Elmtwidth = 0.8e-3
Elmtlength = 0.8e-3
Elmtpitchx = 1e-3
Elmtpitchy = 1e-3
Elmtpx = ((EffSolidlength - Nbelmtx*Elmtlength - (Nbelmtx-1)*
	(Elmtpitchx-Elmtlength))/2 + Boundarysize)
Elmtpy = ((EffSolidwidth - Nbelmty*Elmtwidth - (Nbelmty-1)*
	(Elmtpitchy-Elmtwidth))/2 + Boundarysize)

# Mesh size
msize = 70e-6

# Step time parameters
simulationTime = 4E-6

# Signal amplitude parameters
frequency = 5E6
N = 5
t_pulse = N/frequency

# Sampling rate
# sample_rate = 150E6
# sample_period = 1/sample_rate
sample_period = 1.5e-8




# Creating the solid geometry
s = mdb.models['Model-1'].ConstrainedSketch(name='_profile_', sheetSize=0.1)
s.sketchOptions.setValues(decimalPlaces=3)
s.rectangle(point1=(0,0), point2=(Solidlength, Solidwidth))
v = s.vertices
s.FixedConstraint(entity=v[0])
s.ObliqueDimension(vertex1=v[0], vertex2=v[1], textPoint=(-0.0111406221985817,
	0.00642482563853264), value=Solidlength)
s.ObliqueDimension(vertex1=v[1], vertex2=v[2], textPoint=(0.00852133240550756,
	0.024478180333972), value=Solidwidth)
s=mdb.models['Model-1'].sketches['_profile_']
s.Parameter(name='Width', path='dimensions[0]', expression=swidth)
s.Parameter(name='Length', path='dimensions[1]', expression=slength,
	previousParameter='Width')
p = mdb.models['Model-1'].Part(name='Solid_full', dimensionality=THREE_D,
	type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s, depth=Solidextrude)
del mdb.models['Model-1'].sketches['_profile_']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
upEdge = p.edges[0]
extrudeFace = p.faces[-2]




# Generate partitionning of the elements
for i in range(0, Nbelmtx):
	for j in range(0, Nbelmty):
		Elmtpxnew = Elmtpx + i*Elmtpitchx
		Elmtpynew = Elmtpy + j*Elmtpitchy
		p = mdb.models['Model-1'].parts['Solid_full']
		f = p.faces
		frontFace = f.findAt(((Solidlength*0.01,
			Solidwidth*0.01,0), ),)
		s = mdb.models['Model-1'].ConstrainedSketch(name='element',
			sheetSize=0.1)
		s.sketchOptions.setValues(decimalPlaces=5)
		s.rectangle(point1=(Elmtpxnew, Elmtpynew),
			point2=(Elmtpxnew+Elmtlength, Elmtpynew+Elmtwidth))
		p.PartitionFaceBySketch(faces=frontFace, sketch=s)
		elmtFace = f.findAt(((Elmtpxnew+(Elmtlength)/2,
			Elmtpynew+(Elmtwidth)/2,0), ),)
		p.Set(faces=elmtFace, name='Set-E'+str(i+1)+str(j+1))
		p.Surface(side1Faces=elmtFace, name='Surf_E'+str(i+1)+str(j+1))
# p = mdb.models['Model-1'].parts['Solid_full']
# p.Set(faces=elmtFaces, name='Set-R')


# # Create Set-R for outputs
# p = mdb.models['Model-1'].parts['Solid_full']
# f = p.faces
# frontFace = f.findAt(((Solidlength-2.5*Boundarysize,
# 	Solidwidth-2.5*Boundarysize,0), ),)
# p.Set(faces=frontFace, name='Set-R')



# Creating the array of defects
p = mdb.models['Model-1'].parts['Solid_full']
d = p.datums
e = p.edges
defPlane = p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE,
	offset=Solidextrude/2)
# upEdge = p.DatumAxisByPrincipalAxis(principalAxis=YAXIS)
mdb.models['Model-1'].ConstrainedSketch(gridSpacing=0.0008, name='_profile_',
    sheetSize=0.0337, transform=
    mdb.models['Model-1'].parts['Solid_full'].MakeSketchTransform(
    sketchPlane=mdb.models['Model-1'].parts['Solid_full'].datums[p.datums.keys()[0]],
    sketchPlaneSide=SIDE1,
    sketchUpEdge=upEdge,
    sketchOrientation=RIGHT, origin=(0, 0, Solidextrude/2)))
mdb.models['Model-1'].sketches['_profile_'].sketchOptions.setValues(
    decimalPlaces=5)
mdb.models['Model-1'].parts['Solid_full'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['_profile_'])
mdb.models['Model-1'].sketches['_profile_'].rectangle(point1=(Defectpx, Defectpy),
	point2=(Defectpx+Defectlength,Defectpy+Defectwidth))
g = mdb.models['Model-1'].sketches['_profile_'].geometry
# mdb.models['Model-1'].sketches['_profile_'].linearPattern(number1=Defectcountx,
# 	spacing1=Defectlength+Defectspacing,
# 	angle1=0, number2=Defectcounty, spacing2=Defectwidth+Defectspacing,
# 	angle2=90, geomList=[g[2], g[3], g[4], g[5]])
mdb.models['Model-1'].parts['Solid_full'].CutExtrude(depth=Defectdepth,
    flipExtrudeDirection=OFF, sketch=
    mdb.models['Model-1'].sketches['_profile_'], sketchOrientation=RIGHT,
    sketchPlane=mdb.models['Model-1'].parts['Solid_full'].datums[p.datums.keys()[0]],
    sketchPlaneSide=SIDE1, sketchUpEdge=upEdge)
del mdb.models['Model-1'].sketches['_profile_']




# Creating the Boundary Regions
mdb.models['Model-1'].parts['Solid_full'].DatumPlaneByPrincipalPlane(principalPlane=XYPLANE,
offset=Solidextrude)
s = mdb.models['Model-1'].ConstrainedSketch(gridSpacing=0.0008, name='_profile_',
    sheetSize=0.0337, transform=
    mdb.models['Model-1'].parts['Solid_full'].MakeSketchTransform(
    sketchPlane=mdb.models['Model-1'].parts['Solid_full'].datums[p.datums.keys()[1]],
    sketchPlaneSide=SIDE1,
	sketchUpEdge=upEdge,
    sketchOrientation=RIGHT, origin=(0, 0, Solidextrude)))
mdb.models['Model-1'].sketches['_profile_'].sketchOptions.setValues(
    decimalPlaces=5)
s.rectangle(point1=(0,0), point2=(Boundarysize,Boundarysize))
s.rectangle(point1=(0,Solidwidth), point2=(Boundarysize,Solidwidth-Boundarysize))
s.rectangle(point1=(Solidlength,Solidwidth),
	point2=(Solidlength-Boundarysize,Solidwidth-Boundarysize))
s.rectangle(point1=(Solidlength,0),
	point2=(Solidlength-Boundarysize,Boundarysize))
mdb.models['Model-1'].parts['Solid_full'].CutExtrude(flipExtrudeDirection=OFF,
	sketch=mdb.models['Model-1'].sketches['_profile_'],
	sketchOrientation=RIGHT,
    sketchPlane=mdb.models['Model-1'].parts['Solid_full'].datums[p.datums.keys()[1]],
    sketchPlaneSide=SIDE1, sketchUpEdge=upEdge)
session.viewports['Viewport: 1'].setValues(displayedObject=s)
mdb.models['Model-1'].parts['Solid_full'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['_profile_'])
s.rectangle(point1=(Boundarysize,Boundarysize), point2=(Solidlength-Boundarysize,
	Solidwidth-Boundarysize))
s.rectangle(point1=(Boundarysize*2, Boundarysize*2)
    , point2=(Solidlength-Boundarysize*2, Solidwidth-Boundarysize*2))
session.viewports['Viewport: 1'].setValues(displayedObject=s)
extrudeFace = p.faces.findAt(((Solidlength/2, Solidwidth/2, Solidextrude),),)
mdb.models['Model-1'].parts['Solid_full'].PartitionFaceBySketch(sketch=s,
	faces=extrudeFace)
del mdb.models['Model-1'].sketches['_profile_']
session.viewports['Viewport: 1'].setValues(displayedObject=p)


# Partitioning the Boundary Regions
# s = mdb.models['Model-1'].ConstrainedSketch(gridSpacing=0.0008, name='__profile__',
#     sheetSize=0.0337, transform=
#     mdb.models['Model-1'].parts['Solid_full'].MakeSketchTransform(
#     sketchPlane=mdb.models['Model-1'].parts['Solid_full'].datums[p.datums.keys()[1]],
#     sketchPlaneSide=SIDE1,
# 	sketchUpEdge=upEdge,
#     sketchOrientation=RIGHT, origin=(0, 0, Solidextrude)))
# s.rectangle(point1=(Boundarysize*2, Boundarysize*2)
#     , point2=(Solidlength-Boundarysize*2, Solidwidth-Boundarysize*2))
# session.viewports['Viewport: 1'].setValues(displayedObject=s)
# extrudeFace = p.faces.findAt(((Solidlength/2, Solidwidth/2, Solidextrude),),)
# p.PartitionFaceBySketch(faces=extrudeFace, sketch=s)
edgeA = mdb.models['Model-1'].parts['Solid_full'].edges.findAt(
	((Solidlength/2, Boundarysize*2, Solidextrude)))
edgeB = mdb.models['Model-1'].parts['Solid_full'].edges.findAt(
	((Boundarysize*2, Solidwidth/2, Solidextrude)))
edgeC = mdb.models['Model-1'].parts['Solid_full'].edges.findAt(
	((Solidlength/2, Solidwidth-Boundarysize*2, Solidextrude)))
edgeD = mdb.models['Model-1'].parts['Solid_full'].edges.findAt(
	((Solidlength-Boundarysize*2, Solidwidth/2, Solidextrude)))
# boundaryEdgesA = (edgeA, edgeB, edgeC, edgeD)
# sweepEdgeA = mdb.models['Model-1'].parts['Solid_full'].edges.findAt((
# 	Solidlength, Solidwidth-Boundarysize, Solidextrude/2))
# cell = mdb.models['Model-1'].parts['Solid_full'].cells.findAt(
# 	((Solidlength-Boundarysize*2.5, Boundarysize*2.5, Solidextrude*0.8)))
# mdb.models['Model-1'].parts['Solid_full'].PartitionCellBySweepEdge(cells=
#     cell, edges=boundaryEdgesA, sweepPath=sweepEdgeA)

edge1 = mdb.models['Model-1'].parts['Solid_full'].edges.findAt(
	((Solidlength/2, Boundarysize, Solidextrude)))
edge2 = mdb.models['Model-1'].parts['Solid_full'].edges.findAt(
	((Boundarysize, Solidwidth/2, Solidextrude)))
edge3 = mdb.models['Model-1'].parts['Solid_full'].edges.findAt(
	((Solidlength/2, Solidwidth-Boundarysize, Solidextrude)))
edge4 = mdb.models['Model-1'].parts['Solid_full'].edges.findAt(
	((Solidlength-Boundarysize, Solidwidth/2, Solidextrude)))
boundaryEdges = (edge1, edge2, edge3, edge4, edgeA, edgeB, edgeC, edgeD)
sweepEdge = mdb.models['Model-1'].parts['Solid_full'].edges.findAt((
	Solidlength, Solidwidth-Boundarysize, Solidextrude/2))
mdb.models['Model-1'].parts['Solid_full'].PartitionCellBySweepEdge(cells=
    mdb.models['Model-1'].parts['Solid_full'].cells.getSequenceFromMask((
    '[#1 ]', ), ), edges=boundaryEdges, sweepPath=sweepEdge)



# Create materials and sections
m = mdb.models['Model-1'].Material(name=('Aluminum'))
m.Density(table=((2700,),))
m.Elastic(table=((69E+9, 0.33), ))
mdb.models['Model-1'].HomogeneousSolidSection(name=('Section-Alu'),
	material='Aluminum')
p = mdb.models['Model-1'].parts['Solid_full']
c = p.cells
region = regionToolset.Region(cells=c)
p = mdb.models['Model-1'].parts['Solid_full']
p.SectionAssignment(region=region, sectionName='Section-Alu', offset=0.0,
	offsetType=MIDDLE_SURFACE, offsetField='',
	thicknessAssignment=FROM_SECTION)



#Import instance in assembly
a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Solid_full']
a.Instance(name='Solid_full-1', part=p, dependent=ON)
a.regenerate()


#Generating the mesh
p = mdb.models['Model-1'].parts['Solid_full']
p.setMeshControls(regions=p.cells, elemShape=TET, technique=FREE)
p.seedPart(size=msize, deviationFactor=0.1, minSizeFactor=0.1)
elemType1 = mesh.ElemType(elemCode=C3D8R, elemLibrary=EXPLICIT,
	secondOrderAccuracy=OFF, hourglassControl=DEFAULT,
	distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)
p.setElementType(regions=(p.cells, ), elemTypes=(elemType1, elemType2))
bufferCell = mdb.models['Model-1'].parts['Solid_full'].cells.findAt(
	((Solidlength-Boundarysize*1.5, Boundarysize*1.5, Solidextrude*0.8)))
bufferRegion = (bufferCell,)
p.setMeshControls(regions=bufferRegion, elemShape=HEX, technique=SWEEP)
p.setElementType(elemTypes=(mesh.ElemType(
    elemCode=C3D8R, elemLibrary=EXPLICIT), mesh.ElemType(elemCode=C3D6,
    elemLibrary=EXPLICIT), mesh.ElemType(elemCode=C3D6, elemLibrary=EXPLICIT)),
	regions = bufferRegion)

boundaryBottom = p.cells.findAt((Solidlength/2, Boundarysize/2, Solidextrude/2),)
boundaryTop = p.cells.findAt((Solidlength/2, Solidwidth-Boundarysize/2, Solidextrude/2),)
boundaryRight = p.cells.findAt((Solidlength-Boundarysize/2, Solidwidth/2, Solidextrude/2),)
boundaryLeft = p.cells.findAt((Boundarysize/2, Solidwidth/2, Solidextrude/2),)
boundaryCells = (boundaryTop, boundaryBottom, boundaryLeft, boundaryRight)
p.setElementType(elemTypes=(mesh.ElemType(
    elemCode=AC3D8R, elemLibrary=EXPLICIT), mesh.ElemType(elemCode=AC3D6,
    elemLibrary=EXPLICIT), mesh.ElemType(elemCode=AC3D4, elemLibrary=EXPLICIT)),
	regions = boundaryCells)
# p.setMeshControls(regions=boundaryCells, elemShape=HEX, technique=STRUCTURED)
# Stack direction assignment for top cell
p.setMeshControls(regions=(boundaryTop,), elemShape=HEX, technique=SWEEP)
sweepFace = p.faces.findAt((Solidlength/2, Solidwidth, Solidextrude/2))
sweepEdge = p.edges.findAt((Boundarysize, Solidwidth-Boundarysize/2, 0),)
p.assignStackDirection(cells=(boundaryTop,), referenceRegion=sweepFace)
# Stack direction assignment for right cell
p.setMeshControls(regions=(boundaryRight,), elemShape=HEX, technique=SWEEP)
sweepFace = p.faces.findAt((Solidlength, Solidwidth/2, Solidextrude/2))
sweepEdge = p.edges.findAt((Boundarysize, Solidwidth-Boundarysize/2, 0),)
p.assignStackDirection(cells=(boundaryRight,), referenceRegion=sweepFace)
# Stack direction assignment for bottom cell
p.setMeshControls(regions=(boundaryBottom,), elemShape=HEX, technique=SWEEP)
sweepFace = p.faces.findAt((Solidlength/2, 0, Solidextrude/2))
sweepEdge = p.edges.findAt((Boundarysize, Solidwidth-Boundarysize/2, 0),)
p.assignStackDirection(cells=(boundaryBottom,), referenceRegion=sweepFace)
# Stack direction assignment for left cell
p.setMeshControls(regions=(boundaryLeft,), elemShape=HEX, technique=SWEEP)
sweepFace = p.faces.findAt((0, Solidwidth/2, Solidextrude/2))
sweepEdge = p.edges.findAt((Boundarysize, Solidwidth-Boundarysize/2, 0),)
p.assignStackDirection(cells=(boundaryLeft,), referenceRegion=sweepFace)
# Seeding the edges that need single elements
edge1 = p.edges.findAt((Boundarysize, Boundarysize/2, 0))
edge2 = p.edges.findAt((Boundarysize/2, Boundarysize, 0))
edge3 = p.edges.findAt((Solidlength-Boundarysize/2, Boundarysize, 0))
edge4 = p.edges.findAt((Solidlength-Boundarysize, Boundarysize/2, 0))
edge5 = p.edges.findAt((Boundarysize/2, Solidwidth-Boundarysize, 0))
edge6 = p.edges.findAt((Boundarysize, Solidwidth-Boundarysize/2, 0))
edge7 = p.edges.findAt((Solidlength-Boundarysize, Solidwidth-Boundarysize/2, 0))
edge8 = p.edges.findAt((Solidlength-Boundarysize/2, Solidwidth-Boundarysize, 0))
edge9 = p.edges.findAt((Boundarysize, Boundarysize/2, Solidextrude))
edge10 = p.edges.findAt((Boundarysize/2, Boundarysize, Solidextrude))
edge11 = p.edges.findAt((Solidlength-Boundarysize/2, Boundarysize, Solidextrude))
edge12 = p.edges.findAt((Solidlength-Boundarysize, Boundarysize/2, Solidextrude))
edge13 = p.edges.findAt((Boundarysize/2, Solidwidth-Boundarysize, Solidextrude))
edge14 = p.edges.findAt((Boundarysize, Solidwidth-Boundarysize/2, Solidextrude))
edge15 = p.edges.findAt((Solidlength-Boundarysize, Solidwidth-Boundarysize/2, Solidextrude))
edge16 = p.edges.findAt((Solidlength-Boundarysize/2, Solidwidth-Boundarysize, Solidextrude))
boundaryEdges = (edge1, edge2, edge3, edge4, edge5, edge6, edge7, edge8, edge9, edge10,
	edge11, edge12, edge13, edge14, edge15, edge16)
p.seedEdgeByNumber(edges=boundaryEdges, number=1)
# p.generateMesh()
mdb.models['Model-1'].rootAssembly.regenerate()


# Create Tabular Amplitude for loads
t = t_pulse/100
amp_matrix = (0.0, 0.0),
while t <= t_pulse:
	temp_amp = (0.5*(1 - math.cos(2*math.pi*frequency*t/N))*
		math.sin(2*math.pi*frequency*t))
	temp_matrix = (t, temp_amp),
	amp_matrix = amp_matrix + temp_matrix
	t = t + t_pulse/100
extendAmp = (simulationTime, 0),
amp_matrix = amp_matrix + extendAmp
amp = mdb.models['Model-1'].TabularAmplitude(name=('amp-1'), data=amp_matrix)




for i in range(0, 1):
	for j in range(0, Nbelmty):
		# Creating the new model
		mdb.Model(name='Model-PulseE'+str(i+1)+str(j+1), objectToCopy=mdb.models['Model-1'])

		# Creating the Dynamic Explicit Steps
		mdb.models['Model-PulseE'+str(i+1)+str(j+1)].ExplicitDynamicsStep(
			name='Step-E'+str(i+1)+str(j+1),
			previous='Initial', timePeriod=simulationTime)

		# Creating loads at all load surfaces
		a = mdb.models['Model-PulseE'+str(i+1)+str(j+1)].rootAssembly
		s = a.instances['Solid_full-1'].surfaces
		mdb.models['Model-PulseE'+str(i+1)+str(j+1)].Pressure(amplitude='amp-1',
			createStepName='Step-E'+str(i+1)+str(j+1),
			distributionType=UNIFORM, field='amp',
			magnitude=100e6, name='Load-E'+str(i+1)+str(j+1),
			region=s['Surf_E'+str(i+1)+str(j+1)])

		# Creating the field output request
		for ii in range(0, 1):
			for jj in range(0, Nbelmty):
				a = mdb.models['Model-PulseE'+str(i+1)+str(j+1)].rootAssembly
				mdb.models['Model-PulseE'+str(i+1)+str(j+1)].FieldOutputRequest(
					name='F-Output-E'+str(ii+1)+str(jj+1),
					createStepName='Step-E'+str(i+1)+str(j+1), timeInterval=sample_period,
					variables=('U',),
					region=a.allInstances['Solid_full-1'].sets['Set-E'+str(ii+1)+str(jj+1)])

		mdb.models['Model-PulseE'+str(i+1)+str(j+1)].HistoryOutputRequest(
			name='H-Output-E'+str(i+1)+str(j+1),
			createStepName='Step-E'+str(i+1)+str(j+1), numIntervals=20)

		# Creating the job and writing the .inp file
		mdb.models['Model-PulseE'+str(i+1)+str(j+1)].rootAssembly.regenerate()
		mdb.Job(contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=
			SINGLE, historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE, model=
			'Model-PulseE'+str(i+1)+str(j+1), modelPrint=OFF,
			multiprocessingMode=DEFAULT, name='Job3D-PulseE'+str(i+1)+str(j+1),
			nodalOutputPrecision=SINGLE, numCpus=12, numDomains=12,
			parallelizationMethodExplicit=DOMAIN, scratch='', type=ANALYSIS,
			userSubroutine='')
		mdb.jobs['Job3D-PulseE'+str(i+1)+str(j+1)].writeInput()

		# Replacing element type in .inp file
		inpFile = open('Job3D-PulseE'+str(i+1)+str(j+1)+'.inp', 'rt')
		data = inpFile.read()
		data = data.replace('AC3D8R', 'CIN3D8')
		inpFile.close()
		inpFile = open('Job3D-PulseE'+str(i+1)+str(j+1)+'.inp', 'wt')
		inpFile.write(data)
		inpFile.close()

		# Importing the new .inp file as a new model
		mdb.ModelFromInputFile(name='INF_Model-PulseE'+str(i+1)+str(j+1),
			inputFileName='C:/Users/BASSIL/Documents/STAGE_2/SIMULATIONS/3D/Job3d-PulseE'+str(i+1)+str(j+1)+'.inp')

		# Overwriting the Jobs with the final Jobs with inf. elem. BC
		mdb.Job(contactPrint=OFF, description='', echoPrint=OFF, explicitPrecision=
			SINGLE, historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE, model=
			'INF_Model-PulseE'+str(i+1)+str(j+1), modelPrint=OFF,
			multiprocessingMode=DEFAULT, name='Job3D-PulseE'+str(i+1)+str(j+1),
			nodalOutputPrecision=SINGLE, numCpus=12, numDomains=12,
			parallelizationMethodExplicit=DOMAIN, scratch='', type=ANALYSIS,
			userSubroutine='')
