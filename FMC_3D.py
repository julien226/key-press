from odbAccess import *
from abaqusConstants import *
from odbMaterial import *
from odbSection import *
import numpy as np
from scipy.io import savemat


wd = "C:/Users/BASSIL/Documents/STAGE_2/SIMULATIONS/displacement_bc/all_elements_pulse_5MHz_16x4_elements/textfiles/"
workingDirectory = "C:/Users/BASSIL/Documents/STAGE_2/SIMULATIONS/displacement_bc/all_elements_pulse_5MHz_16x4_elements/abaqus_files/Job3D-PulseE"

# Nbelmt = 4
# for q in range(Nbelmt-1,Nbelmt):
#     R = [0]*Nbelmt
#     outFile = open('C:\\Users\\BASSIL\\Documents\\STAGE_2\\SIMULATIONS\\3D_Output_txt\\4%d.txt' %(q+1), 'w')
#     odb = openOdb(workingDirectory+str(q+1)+'.odb')
#
#     for k in odb.steps['Step-E4%d' %(q+1)].frames:
#         for i in range(Nbelmt-1, Nbelmt):
#             elemSet = odb.rootAssembly.instances['SOLID_FULL-1'].elementSets['SET-E4'+str(i+1)].elements
#             stressField = k.fieldOutputs['S']
#             lenSet = len(elemSet)
#             for elemidx in range(lenSet):
#                 elem = elemSet[elemidx]
#                 stress = stressField.getSubset(position=INTEGRATION_POINT, region=elem)
#                 s11 = stress.getScalarField(componentLabel="S11").values[0].data
#                 R[i] = (R[i]+s11)/lenSet
#         line = ' %g ' % k.frameValue
#
#         for l in range(0,Nbelmt):
#             line = line+ ' %g ' % R[l]
#         line = line + '\n'
#         outFile.write(line)
#         R = [0]*Nbelmt
#
#     outFile.close()

"""
Nbelmtx = 4
Nbelmty = 16
for xelemPulse in range(0,Nbelmtx):
    for yelemPulse in range(0,Nbelmty):
        odb = openOdb(workingDirectory+str(xelemPulse+1)+str(yelemPulse+1)+'.odb')
        lenFrames = len(odb.steps['Step-E'+str(xelemPulse+1)+str(yelemPulse+1)].frames)
        output = np.empty([lenFrames, 2])
        for yelem in range(0,Nbelmty):
            for frame in odb.steps['Step-E'+str(xelemPulse+1)+str(yelemPulse+1)].frames:
                output[frame, 0] = frame.frameValue
                elemSetReflec = odb.rootAssembly.instances['SOLID_FULL-1'].elementSets['SET-E'+str(xelemPulse+1)+str(yelem+1)].elements
                stressField = k.fieldOutputs['S']
                lenSet = len(elemSetReflec)
                s11 = 0
                for elemidx in range(lenSet):
                    elem = elemSetReflec[elemidx]
                    stress = stressField.getSubset(position=INTEGRATION_POINT, region=elem)
                    s11 = s11 + stress.getScalarField(componentLabel="S11").values[0].data/lenSet
                output[frame, 1] = s11
            np.savetxt(wd+str(xelemPulse)+str(yelemPulse)+str(yelem)+'.txt', output)
"""
Nbelmtx = 8
Nbelmty = 8
for xelemPulse in range(3,4):
    for yelemPulse in range(3,4):
        odb = openOdb(workingDirectory+str(xelemPulse+1)+str(yelemPulse+1)+'.odb')
        lenFrames = len(odb.steps['Step-E'+str(xelemPulse+1)+str(yelemPulse+1)].frames)
        output = np.empty([lenFrames, 2])
        for yelem in range(0,Nbelmty):
            elemSetReflec = odb.rootAssembly.instances['SOLID_FULL-1'].elementSets['SET-E'+str(xelemPulse+1)+str(yelem+1)].elements
            lenSet = len(elemSetReflec)
            count = 0
            for frame in odb.steps['Step-E'+str(xelemPulse+1)+str(yelemPulse+1)].frames:
                output[count, 0] = frame.frameValue
                stressField = frame.fieldOutputs['S']
                s11 = 0
                for elemidx in range(lenSet):
                    elem = elemSetReflec[elemidx]
                    stress = stressField.getSubset(position=INTEGRATION_POINT, region=elem)
                    s11 = s11 + stress.getScalarField(componentLabel="S11").values[0].data/lenSet
                # round(s11, 5)
                output[count, 1] = s11
                count = count + 1
                # if count == 3:
                #     break
            np.savetxt(wd+str(xelemPulse+1)+str(yelemPulse+1)+str(yelem+1)+'.txt', output, fmt='%.6e')
