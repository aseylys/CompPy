import json
from collections import OrderedDict


################################
#Function: StageOpen
#Opens Saved Compressor Json File
#Inputs: 
#file: path to file (str)
#Returns:
#data: full compressor params (dict)
################################
def StageOpen(file):
    with open(file) as dataFile:
        data = json.load(dataFile, object_pairs_hook = OrderedDict)
        
        for stage in data:
            yield data[stage]['Stage'], data[stage]['Rotor'], data[stage]['Stator']
            

################################
#Function: StageSave
#Saves Compressor Params Json File
#Inputs: 
#file: path to file (str)
#common: common vars (dict)
#rotor: rotor vars (dict)
#stator: stator vars (dict)
#Returns:
#None
################################
def StageSave(file, common, rotor, stator):
    with open(file , 'w') as dataFile:
        stages = {}
        
        for stage in range(1, len(common) + 1):
            stages['Stage ' + str(stage)] = {'Stage': common[stage - 1], 'Rotor': rotor[stage - 1], 'Stator': stator[stage - 1]}
            
        json.dump(stages, dataFile, indent = 4, sort_keys = True, ensure_ascii=True)