# %%
import json
import os
import statistics
import re
import math

#CODE FOR GETTING THE RISK SCORE (OUT OF 100) FOR EACH PERSON AND RELEVANCE SCORE (OUT OF 10) FOR EACH RECOMMENDATION

folder_path = '/Users/vansh/Desktop/EightFoldAISubmission/Structured LORs'

all_files = os.listdir(folder_path)
risk_score = {}
relevance_score = {}

for i in range(1000):
    risk_score[i] = 0
    relevance_score[i] = {}
    files = [f for f in all_files if f'Resume_{i}_' in f and 'Recommendation_From_ID' in f and f.endswith('.json')]
    count = 0
    for file_name in files:
        recommender_id = re.search(r'_(\d+)\.json$', file_name).group(1)
        count += 1
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        fraud_score = data['output']['fraud_chance_level']
        risk_score[i] += (fraud_score-1)/4
        relevance_score[i][recommender_id] = data['output']['relevance_score']
    if count == 0:
        risk_score[i] = 0.01
        continue
    risk_score[i] = risk_score[i]/count
    risk_score[i] = round(risk_score[i]*100, 1)
print(risk_score)

average_risk_score = sum(risk_score.values()) / len(risk_score)

# Print top 5 max values
top_5_max_values = sorted(risk_score.values(), reverse=True)[:100]
print(f"Top 100 Max Values: {top_5_max_values}")
print(f"Average Risk Score: {average_risk_score:.2f}")

variance_risk_score = statistics.variance(risk_score.values())
print(f"Standard Deviation of Risk Scores: {math.sqrt(variance_risk_score):.2f}")

    
# Save the final DataFrame to a CSV file
# output_file_path = os.path.join(folder_path, 'output.csv')
# result_df.to_csv(output_file_path, index=False)

# print(f"Output saved to {output_file_path}")

# %%
# RUNNING EXAMPLES TO CROSS CHECK

risk_score_items = list(risk_score.items())

# Sort the list by the risk score in descending order
sorted_risk_scores = sorted(risk_score_items, key=lambda item: item[1], reverse=True)

# Select the top 100 tuples
top_100_risk_scores = sorted_risk_scores[:100]

# Extract the keys from these tuples
top_100_keys = [item[0] for item in top_100_risk_scores]

print(top_100_keys)

# %%
print(risk_score[514])

# %%
# IF SOMEONE GIVES RECOMMENDATIONS WHICH ARE FRAUD (WITH MORE THAN 3/5 RATING), THEN THAT PERSON'S (100 - RISK SCORE) INCREASES BY APPROXIMATELY 10% FOR EACH 
for i in range(1000):
    x = 0
    files = [f for f in all_files if f'Recommendation_From_ID_{i}.' in f and f.endswith('.json')]
    # Loop through each filtered file
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r') as file:
            data = json.load(file)
        if data['output']['fraud_chance_level'] > 3:
            x += data['output']['fraud_chance_level'] - 3
    risk_score[i] += (100 - risk_score[i]) * x / 10
    risk_score[i] = round(risk_score[i], 1)
#Printing some statistics to check the risk score
print(risk_score)

average_risk_score = sum(risk_score.values()) / len(risk_score)

top_5_max_values = sorted(risk_score.values(), reverse=True)[:100]
print(f"Top 100 Max Values: {top_5_max_values}")
print(f"Average Risk Score: {average_risk_score:.2f}")

variance_risk_score = statistics.variance(risk_score.values())
print(f"Standard Deviation of Risk Scores: {math.sqrt(variance_risk_score):.2f}")

    

# %%
#CODE FOR CYCLE DETECTION

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

csv_file_path = '/Users/vansh/Desktop/EightFoldAISubmission/Final_Persons_And_Recommenders.csv'  # Replace with your actual CSV file path
df = pd.read_csv(csv_file_path)

# Initialize the directed graph
G = nx.DiGraph()

# Iterate through the rows and add edges to the graph
for index, row in df.iterrows():
    recomendee = row['ID']
    recommenders = eval(row['Recommenders ID'])  # Convert the string list into an actual list
    for recommender in recommenders:
        G.add_edge(recommender, recomendee)
def function_1(target_id):
    if target_id not in G:
        # print(f"ID {target_id} does not exist in the graph.")
        return
    
    recommenders = list(G.predecessors(target_id))
    if not recommenders:
        # print(f"No recommenders found for ID {target_id}.")
        return None
        return
    
    # print(f"ID {target_id} is recommended by: {recommenders}")
    
    # To track discovered cycles
    discovered_cycles = []

    # Check for cycles involving the target_id and any of its recommenders
    for recommender in recommenders:
        # Start DFS from the target_id
        stack = [(target_id, [target_id])]
        visited = set([target_id])
        
        while stack:
            current_node, path = stack.pop()
            
            # Explore neighbors
            for neighbor in G.neighbors(current_node):
                if neighbor == recommender:
                    # Cycle found involving both target_id and recommender
                    cycle = path + [recommender]
                    if cycle not in discovered_cycles:
                        discovered_cycles.append(cycle)
                        # print(f"ID {target_id} forms a cycle with recommender ID {recommender}. Cycle: {cycle}")
                elif neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))
    
    if not discovered_cycles:
        return None
    return discovered_cycles

# %%
# BEING A PART OF A CYCLE OF LENGTH MORE THAN 7 IS CONSIDERED NORMAL AND UNAVOIDABLE IN THE SYSTEM. SO, THE RISK SCORE OF THE PERSON IS NOT AFFECTED BY IT. THIS IS SO BECAUSE IT BECOMES HARDER TO CORDINATE FRAUD CVS IN A CYCLE OF LENGTH MORE THAN 7. MOREOVER IN A NETWORK ECONOMY A CYCLE OF LENGTH MORE THAN 7 IS CONSIDERED NORMAL. 
# IF A PERSON IS A PART OF A CYCLE OF LENGTH 3, THEN THE RISK SCORE OF THE PERSON INCREASES BY 10%. 
# IF A PERSON IS A PART OF A CYCLE OF LENGTH 4, THEN THE RISK SCORE OF THE PERSON INCREASES BY 8%.
# IF A PERSON IS A PART OF A CYCLE OF LENGTH 5, THEN THE RISK SCORE OF THE PERSON INCREASES BY 6%.
# IF A PERSON IS A PART OF A CYCLE OF LENGTH 6, THEN THE RISK SCORE OF THE PERSON INCREASES BY 4%.

for i in range(1000):
    discovered_cycles = function_1(i)
    if discovered_cycles is None:
        continue
    for j in discovered_cycles:
        if len(j) == 3:
            risk_score[i] += (100 - risk_score[i])*0.1
        elif len(j) == 4:
            risk_score[i] += (100 - risk_score[i])*0.08
        elif len(j) == 5:
            risk_score[i] += (100 - risk_score[i])*0.06
        elif len(j) == 6:
            risk_score[i] += (100 - risk_score[i])*0.04
    risk_score[i] = round(risk_score[i], 1)

# PRINTING SOME STATISTICS TO CHECK HOW RISK SCORE HAS CHANGED.      

print(risk_score)

average_risk_score = sum(risk_score.values()) / len(risk_score)

top_5_max_values = sorted(risk_score.values(), reverse=True)[:100]
print(f"Top 100 Max Values: {top_5_max_values}")
print(f"Average Risk Score: {average_risk_score:.2f}")

variance_risk_score = statistics.variance(risk_score.values())
print(f"Standard Deviation of Risk Scores: {math.sqrt(variance_risk_score):.2f}")


# %%
# THE FUNCTION WHICH RETURNS THE INFLUENCE OF THE PERSON OUT OF 10.
def influence(i):
    folder_path = '/Users/vansh/Desktop/EightFoldAISubmission/Influence_evaluation'

    # List all files in the folder
    all_files = os.listdir(folder_path)

    file = [f for f in all_files if f'Resume_{i}.' in f and f.endswith('.json')]
    if file:
        # Loop through each filtered file
        file_path = os.path.join(folder_path, file[0])
        # Read the JSON file
        with open(file_path, 'r') as file_to_open:
            data = json.load(file_to_open)
    else:
        print(f"No file found for Resume_{i}.json")
    return data['output']['influence_factor_score']


# %%
influence(233)

# %%
# if influential people recommend a person and the recommendations are not fraud and are relevant,  then the person is likely to be a good hire.
# We define hiring score as the product of influence of the recommender, the relevance of the recommendation and 1 - risk score of the recommender. (Summed over all recommenders)
# the higher the value of the hiring score, the more the likelihood of the person being a good hire.

import os
import re

def hiring_score(i):
    answer = 0
    total_weight = 0
    folder_path = '/Users/vansh/Desktop/EightFoldAISubmission/Structured LORs'
    all_files = os.listdir(folder_path)

    # Filter files matching the pattern 'Resume_i_' and 'Recommendation_From_ID'
    files = [f for f in all_files if f'Resume_{i}_' in f and 'Recommendation_From_ID' in f and f.endswith('.json')]
    
    for file_name in files:
        # Extract recommender ID from the filename
        recommender_id = re.search(r'_(\d+)\.json$', file_name).group(1)
        recommender_id = int(recommender_id)
        # Calculate safety and weight based on risk score
        safety = 100 - risk_score[recommender_id]
        weight = (safety / 100) ** 2  # Square of the safety score
        
        # Add weighted relevance score to the total answer
        answer += (relevance_score[i][f'{recommender_id}'] / 10) * weight
        total_weight += weight
    
    # Handle the case where no recommendations are found
    if total_weight == 0:
        return 4.01
    
    # Calculate the weighted average
    x= round(((1 - risk_score[i]/100)**2) * answer * ((influence(recommender_id)/10) ** 1.5) / total_weight, 4)
    return round(100*x,2)


# %%
sum = 0
for i in range(1000):
    sum += influence(i)
print(sum/1000)

# %%
# It can be useful to employers to know the last job an applicant worked at. This can give an idea of the applicant's experience and the kind of work they have been doing recently.
def last_job(i):
    folder_path = '/Users/vansh/Desktop/EightFoldAISubmission/Structured Resume'

    # List all files in the folder
    all_files = os.listdir(folder_path)

    file = [f for f in all_files if f == f'{i}.json']
    if file:
        file_path = os.path.join(folder_path, file[0])
        # Read the JSON file
        with open(file_path, 'r') as file_to_open:
            data = json.load(file_to_open)
    else:
        print(f"No file found for Resume_{i}.json")
        return None  # Return None if no file is found
    return data['details']['job_history'][0]['role_name']

# %%
last_job(1)

# %%
def work_experience(i):
    folder_path = '/Users/vansh/Desktop/EightFoldAISubmission/Influence_evaluation'

    all_files = os.listdir(folder_path)

    file = [f for f in all_files if f'_{i}.' in f and f.endswith('.json')]

    if file:
        file_path = os.path.join(folder_path, file[0])
        
        with open(file_path, 'r') as file_to_open:
            data = json.load(file_to_open)
        
        return data['output']['working_experience']

    else:
        print(f"No file found for Resume_{i}.json")
        return None  # Return None if no file is found


# %%
def top_10_skills(i):
    folder_path = '/Users/vansh/Desktop/EightFoldAISubmission/Structured Resume'
    answer = []
    # List all files in the folder
    all_files = os.listdir(folder_path)

    file = [f for f in all_files if f == f'{i}.json']

    if file:
        # Loop through each filtered file
        file_path = os.path.join(folder_path, file[0])
        # Read the JSON file
        with open(file_path, 'r') as file_to_open:
            data = json.load(file_to_open)
        count = 0

        for skill in data['skills']['skills']:
            if skill['level']==5:
                count+=1
                answer.append(skill['name'])
                continue
            elif skill['level']==4 and count<10:
                count+=1
                answer.append(skill['name'])
                continue
            elif skill['level']==3 and count<10:
                count+=1
                answer.append(skill['name'])
                continue

        while count<10:
            count+=1
            answer.append('')
        return answer
            

    else:
        print(f"No file found for Resume_{i}.json")
        return None  # Return None if no file is found


# %%
import csv

# Sample dictionary creation (assuming last_job, influence, and hiring_score are defined functions and risk_score is a list or dict)
sample_dict = {}
for i in range(1000):
    sample_dict[i] = (i, last_job(i), influence(i), risk_score[i], hiring_score(i), work_experience(i), top_10_skills(i)[0], top_10_skills(i)[1], top_10_skills(i)[2], top_10_skills(i)[3], top_10_skills(i)[4], top_10_skills(i)[5], top_10_skills(i)[6], top_10_skills(i)[7], top_10_skills(i)[8], top_10_skills(i)[9])

# Convert dictionary to a list of lists for CSV writing
csv_data = [[k] + list(v) for k, v in sample_dict.items()]

# Define the path to the CSV file
csv_file_path = 'InfoAboutPerson.csv'

# Write the data to a CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    
    # Optionally, write headers if needed
    writer.writerow(['Index','ID', 'Last Job', 'Influence', 'Risk Score', 'Hiring Score', 'Work Experience', 'Skill 1', 'Skill 2','Skill 3','Skill 4','Skill 5','Skill 6','Skill 7','Skill 8','Skill 9','Skill 10'])
    
    # Write data rows
    writer.writerows(csv_data)

print(f"Data saved to {csv_file_path}")



