from pgmpy.models import DiscreteBayesianNetwork  
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


model = DiscreteBayesianNetwork([('Office', 'Light'), ('Office', 'Communicator')])

cpd_o = TabularCPD(variable='Office', variable_card=2, values=[[0.6], [0.4]])

cpd_l = TabularCPD(variable='Light', variable_card=2,
                   values=[[0.95, 0.5],
                           [0.05, 0.5]],
                   evidence=['Office'], evidence_card=[2])

cpd_c = TabularCPD(variable='Communicator', variable_card=2,
                   values=[[0.95, 0.2],
                           [0.05, 0.8]],
                   evidence=['Office'], evidence_card=[2])
model.add_cpds(cpd_o, cpd_l, cpd_c)

assert model.check_model()

inference = VariableElimination(model)
print(inference)
result = inference.query(variables=['Light'], evidence={'Communicator': 0})
print(result)