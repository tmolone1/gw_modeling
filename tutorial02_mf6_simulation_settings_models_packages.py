import flopy

# set up simulation and basic packages
name = "tutorial02_mf6"
sim = flopy.mf6.MFSimulation(sim_name=name, sim_ws=".")
flopy.mf6.ModflowTdis(
    sim, nper=10, perioddata=[[365.0, 1, 1.0] for _ in range(10)]
)
flopy.mf6.ModflowIms(sim)
gwf = flopy.mf6.ModflowGwf(sim, modelname=name, save_flows=True)
flopy.mf6.ModflowGwfdis(gwf, nlay=3, nrow=4, ncol=5)
flopy.mf6.ModflowGwfic(gwf)
flopy.mf6.ModflowGwfnpf(gwf, save_specific_discharge=True)
flopy.mf6.ModflowGwfchd(
    gwf, stress_period_data=[[(0, 0, 0), 1.0], [(2, 3, 4), 0.0]]
)
budget_file = f"{name}.bud"
head_file = f"{name}.hds"
flopy.mf6.ModflowGwfoc(
    gwf,
    budget_filerecord=budget_file,
    head_filerecord=head_file,
    saverecord=[("HEAD", "ALL"), ("BUDGET", "ALL")],
)
print("Done creating simulation.")

# Accessing Simulation-Level Settings

#The verbosity level determines how much FloPy writes to command line output. The options are 1 for quiet, 2 for normal, and 3 for verbose.
sim.simulation_data.verbosity_level = 3
# number of spaces to indent data when writing package files
sim.simulation_data.indent_string = "    "
# precision and number of characters written for floating point variables
sim.float_precision = 8
sim.float_characters = 15
# disable verify_data and auto_set_sizes for faster performance.
# FloPy will not do any checking or autocorrecting of your data.
sim.verify_data = False
sim.auto_set_sizes = False


## Accessing models and packages
#Once a MODFLOW 6 simulation is available in memory, the contents of the simulation object can be listed using a simple print command.
print(sim)

# Get TDIS package and print the contents
tdis = sim.tdis
print(tdis)

# Get Iterative Model Solution (IMS) object
ims = sim.get_package("ims_-1")
print(ims)
# Or because there is only one IMS object for this simulation, we can access it as
ims = sim.get_package("ims")
print(ims)

nam = sim.get_package("nam")
print(nam)

# see the models that are contained within the simulation
print(sim.model_names)
# convert names to a list and then print
model_names = list(sim.model_names)
for mname in model_names:
    print(mname)

#go through all the models in the simulation and print the model name and the model type:
model_names = list(sim.model_names)
for mname in model_names:
    m = sim.get_model(mname)
    print(m.name, m.model_type)
    
gwf = sim.get_model("tutorial02_mf6")
print(gwf)

# One of the most common operations on a model is to see what packages are in it and then get packages of interest. A list of packages in a model can obtained as
package_list = gwf.get_package_list()
print(package_list)

# access each package in this list with gwf.get_package()
# obtain and print the contents of the DIS Package
dis = gwf.get_package("dis")
print(dis)

#The Python type for this dis package is simply
print(type(dis))
