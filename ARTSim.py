# Author: Adam Corbier (@Ad2Am2)

import time
import nub_ctm as ctm

# Use name of model file instead of example_model
from example_model import model

import globalVar

import numpy as np




def prepareModel(model):


    model = ctm.flatten_model(model)
    print("Making nodes...")
    stepStart = time.time()
    globalVar.nodes = ctm.make_nodes(model)
    nodes = globalVar.nodes
    stepEnd = time.time()
    print("Step time: " + str(stepEnd-stepStart))
    print("Initializing matrices...")
    stepStart = time.time()
    globalVar.GMatrix = ctm.initialize_GC_matrix(nodes)   # Initilize the C matrix as a global variable so that any function can access it and modify it
    globalVar.CMatrix = ctm.initialize_GC_matrix(nodes)   # Initilize the C matrix as a global variable so that any function can access it and modify it
    globalVar.IVector = ctm.initialize_I_vector(nodes)
    stepEnd = time.time()
    print("Step time: " + str(stepEnd-stepStart))
    print("Making center resistances...")
    stepStart = time.time()
    ctm.populate_G_matrix(nodes, model)    
    ctm.populate_C_matrix(nodes, model)
    ctm.populate_I_vector(nodes, model)

    stepEnd = time.time()
    print("Model prepared! Step time: " + str(stepEnd-stepStart))

    globalVar.model = model

    globalVar.modelPrepared = True



# NOTE: make sure to call prepareModel before running the simulation
def runSteadyState(outputFile):

    if not globalVar.modelPrepared:
        raise Exception("Model not prepared. Please call prepareModel(model) before running the simulation")

    nodes = globalVar.nodes
    model = globalVar.model
    
    print("Solving steady state...")
    stepStart = time.time()

    ssTempVector = ctm.solve_steady_state()

    ssTempVector = [x + 318.5 for x in ssTempVector]

    stepEnd = time.time()
    print("Step time: " + str(stepEnd-stepStart))
    ctm.printInfo(ssTempVector, nodes, model, outputFile)
    



# NOTE: make sure to call prepareModel before running the simulation
def runTransient(stepDefinition, outputFile):

    if not globalVar.modelPrepared:
        raise Exception("Model not prepared. Please call prepareModel(model) before running the simulation")


    nodes = globalVar.nodes
    model = globalVar.model
    GMatrix = globalVar.GMatrix
    CMatrix = globalVar.CMatrix


    steps = len(stepDefinition)
    globalVar.IVectorVector = ctm.populate_I_vector_vector_transient(nodes, model, steps)

    # Make initTempVector
    initTempVector = []
    for i in range(len(nodes)):
        initTempVector.append(0)
    # NOTE: The above should NOT start at the ambient temperature. It should start at the initial temperature, where ambient is 0.
    


    ttemp = ctm.doBeuler(GMatrix, CMatrix, globalVar.IVectorVector, initTempVector, stepDefinition)

    for i in range(len(ttemp)):
        ttemp[i] = [x + 318.5 for x in ttemp[i]]


    ctm.saveTransientInfo(ttemp, stepDefinition, nodes, model, outputFile)

    



simStart = time.time()

# Mandatory run before any simulation
prepareModel(model)

# Runs steady state analysis on the model, result in given output file
runSteadyState("steadystate.txt")


# Transient simulation

# Definition of the transient steps
# Each element of the array must match an element of the power dissipation array of blocks. If power dissipation is a single value, the same value will be used for all timesteps.
# Each phase of the transient simulation may be subdivided into steps for accuracy and/or analysis. Each step is an equal subdivision of the timestep duration.
# Example stepDefinition:
stepDefinition = [{"duration": 0.001, "steps": 2}, {"duration": 0.009, "steps": 2}, {"duration": 0.09, "steps": 2}, {"duration": 0.9, "steps": 2}, {"duration": 1, "steps": 2}]

runTransient(stepDefinition, "transientResult.txt")



simEnd = time.time()
print("Done! Simulation ran in " + str(simEnd-simStart) + " seconds")