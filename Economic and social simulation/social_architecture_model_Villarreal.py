import pandas as pd
import numpy as np
from random import sample, choices

###################################################################################################
#                                    SOCIAL ARCHITECTURA MODEL                                    #
# This code is a Python adaptation of the original model from Nicolas D Villarreal                #
# https://github.com/nicosims/SA-Model-with-Constant-Capital/blob/main/SA%20Model%20v3%20cleaned  #
###################################################################################################

def set_df_ids(agent_df, str_id):
    if str_id == None:
        id_vector = np.arange(1, agent_df.shape[0] + 1)
        agent_df['ID'] = id_vector
    else:
        id_vector = [str_id + str(n) for n in agent_df.index.tolist()]
        agent_df['ID'] = id_vector

def set_df_money(agent_df, money):
    agent_df['money'] = money




#########################################################
####                                                 ####
####                    Init vars                    ####
####                                                 ####
#########################################################
print('********************************')
print('Loading init vars...')

#Agent vars
n_agents = 1000                #Número de agentes
init_money = 100               #Dinero inicial de cada agente
init_wage_level = 0
init_wage_expectation = 25     #Salario esperado por el agente cuando busca trabajo
init_constant_capital = 0      #Capital constante del agente
init_employ_ind = 0            #ID del empleador

#Model vars
n_iterations = 3000             #Iteraciones del modelo
depreciation_rate = 15 * 12     #Tasa de depreciación del capital constante por mes
saving_rate_cap = 0.5           #Tasa de ahorro de los capitalistas
cperWR = 0.4                    #Límite capital fijo respecto salarios

#### Init agents
print('********************************')
print('Initializing agents...')

# ID | money | ID_employer | wage_level | wage_expectation | revenue | const_cap | var_cap | revenue | n_employees |
n_values = np.arange(start=0, stop=n_agents)
agents_cols = ['ID', 'money', 'ID_employer', 'wage_level',
               'wage_expectation', 'revenue', 'con_cap',
               'var_cap', 'revenue', 'n_employees',
               'employ_ind']

agents_df = pd.DataFrame(np.nan, index=n_values, columns=agents_cols)
set_df_ids(agents_df, None)
agents_df['money'] = init_money
agents_df['wage_level'] = init_wage_level
agents_df['wage_expectation'] = init_wage_expectation
agents_df['const_cap'] = init_constant_capital
agents_df['employ_ind'] = init_employ_ind
print('___')
print('Agents Dataframe in memory:')
print(agents_df.memory_usage())
print('___')

historical_cols = ['employees', 'avg_work_revenue', 'avg_cap_revenue']
n_values_cap = np.arange(start=0, stop=n_iterations)
historical_df = pd.DataFrame(np.nan, index=n_values_cap, columns=historical_cols)


#########################################################
####                                                 ####
####                    Simulation                   ####
####                                                 ####
#########################################################
print('********************************')
print('Starting simulation...')
iter_i = 0
while iter_i < n_iterations:

    # Step 1: DEPRECIATION. Depreciate constant capital in capitalist counts
    agents_df['con_cap'] = agents_df['con_cap']-(agents_df['con_cap']/depreciation_rate)

    # Step 2: Turn Order Determination
    agents_list = agents_df['ID'].tolist()
    sel_agents = sample(agents_list, n_agents)

    for agent_id in sel_agents:
        if agents_df[agents_df['ID'] == agent_id]['employ_ind'].values[0] >= 0:
            # Step 3: Hiring
            # Possible employers
            possible_employers = agents_df[(agents_df['ID'] != agent_id) & (agents_df['employ_ind'] <= 0) & (agents_df['money'] > 0)][['ID','money']].values.astype(float)
            # Select the employer
            employers_total_money = possible_employers[:, 1].sum()
            possible_employers[:, 1] = possible_employers[:, 1] / employers_total_money
            employer_id = np.random.choice(possible_employers[:, 0], size=1, p=possible_employers[:, 1])[0].astype(int)
            #Calculate wage offer
            wage_offer = (agents_df[(agents_df['ID'] == agent_id)]['wage_expectation'].values * (1 + cperWR / 10))[0]


