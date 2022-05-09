import reaktoro as rkt 
import numpy as np

# load thermodynamic database
db = rkt.ThermoFunDatabase("mines16")


# create chemical system
phases = rkt.Phases(db)

aqueous_phase = rkt.AqueousPhase(["H2O@", "O2@", "H2@", "H+", "OH-", "Fe+2"])
phases.add(aqueous_phase)

mineral_phases = rkt.MineralPhases(["Magnetite", "Hematite"])
phases.add(mineral_phases)

gaseous_phase = rkt.GaseousPhase(["H2O", "O2", "H2"])
phases.add(gaseous_phase)

system = rkt.ChemicalSystem(phases)


# set values for physicochemical parameters to be constrained
T = 210 + 273.15 # [K]
P = rkt.waterSaturationPressureWagnerPruss(T)[0] # [Pa]
pH = 2.408163265306123
fO2 = 10*-49.38775510204081


# create equilibrium calculation constraints
specs = rkt.EquilibriumSpecs(system)
specs.temperature()   
specs.pressure()
specs.fugacity("O2(g)")
specs.pH()


# create solver and set constraints
solver = rkt.EquilibriumSolver(specs)
conditions = rkt.EquilibriumConditions(specs)

conditions.temperature(      T,   "kelvin")
conditions.pressure(         P,   "Pa"    )
conditions.fugacity("O2(g)", fO2          )
conditions.pH(               pH           )


# initialize equilibrium calculation
state = rkt.ChemicalState(system)
state.add("H2O@",      1, "kg" )
state.add("Magnetite", 1, "mol")


# solve equilibrium calculation
result = solver.solve(state, conditions)
print(result.optima.succeeded)
