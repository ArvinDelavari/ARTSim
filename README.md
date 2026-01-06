# ARTSim

Welcome to ARTSim, A Robust Thermal Simulator! For a description on the "why?" and "how?" of ARTSim, check out our published works:
- [ECTC 2023 paper](https://ieeexplore.ieee.org/document/10195756)
- [TCMPT paper](https://ieeexplore.ieee.org/document/10922775)

For questions on technical details of ARTSim, feel free to reach out to adam.corbier@mail.mcgill.ca.


## How ARTSim functions

ARTSim simulates models according to the following structure:
- The model is composed of one to many layers (e.g. an active layer, a heat sink, etc.), stacked on each other by the Z-axis
- Each layer is composed of one to many chiplets, that are thermally isolated on the sides. This facilitates the use of the tool for heterogeneous integration. If your layer does not contain chiplets, then define the whole layer as a single chiplet.
- Each chiplet is composed of functional blocks defined by the user

Functional blocks have the following properties:
- Starting coordinates (leftX, bottomY): the functional block's coordinates at the bottom-left corner. The system uses (0,0) as  the origin; going right increases X, going up increases Y. All distance measurements are in meters.
- Width (X-axis) and Height (Y-axis). Be sure to use meters for this (not microns!)
- Thickness (Z-axis). Usually will be the same throughout a layer.
- Power dissipation (W). Note this is not power density (Wm-3)!
- Material properties (Volumetric Heat Capacity and Conductivity). Default values for certain materials can be used from materials.py, or the user can input their own values.
- Resolution: In order to tailor simulation accuracy, the resolution for each block can be defined by the user. At runtime, this will subdivide the block into smaller blocks. The format for this is an array [X,Y], where X is the resolution on the X-axis, and Y is the resolution on the Y-axis. Therefore, the total number of "subblocks" at runtime will be X*Y. Note that large resolutions for many blocks at a time can quickly increase the simulation time.



## How to use ARTSim

In order to use ARTSim, first ensure you have Python3 installed, with NumPy and SciPy (using 'pip install numpy' and 'pip install scipy').

Make a copy of the example_model.py file and define your own model using the same template. What matters is that this file defines a "model" variable in the correct format to be passed to the simulator. **Change the import statement at the top of ARTSim.py from "example_model" to the name of your model file.**

The bottom of the ARTSim.py file runs the simulations. If running a transient simulation, ensure to define the stepDefinition and output file name to your liking. The steady state and transient simulation runs can be commented out if only interested in one type of simulation. The prepareModel() function must always be run before any simulation.

Once the model and simulation are set up, ARTSim can be run using 'python3 ARTSim.py'.

All results are in degrees Kelvin, with the baseline temperature assumed to be 318.15 (45 Celsius). The value for this baseline temperature can be modified in the runSteadyState and runTransient functions.

The output files specify the temperature at the center of each block's subdivision (according to the resolution given), using the order provided by the model input.

### Example

Input: [block1 (resolution=[2,2]), block2 (resolution=[1,1])]

Output: [b1temp1, b1temp2, b1temp3, b1temp4, b2temp]