import os
import json
import re

def merge_recommendations(folder_path):
    # Dictionary to hold recommendations for each target ID
    merged_recommendations = {}

    # List all files in the folder
    all_files = os.listdir(folder_path)

    # Loop through each file
    for file_name in all_files:
        # Match the pattern to extract the target ID and recommender ID
        match = re.match(r'Resume_(\d+)_Recommendation_Recommendation_From_ID_(\d+)\.json$', file_name)
        if match:
            target_id = match.group(1)  # The ID the recommendation is for
            recommender_id = match.group(2)  # The ID of the recommender
            
            # Get the full path of the JSON file
            file_path = os.path.join(folder_path, file_name)
            
            # Read the JSON file
            with open(file_path, 'r') as file_to_open:
                data = json.load(file_to_open)
            
            # Ensure the target ID is in the merged recommendations
            if target_id not in merged_recommendations:
                merged_recommendations[target_id] = {
                    'recommendations': []  # To store recommendations for this target ID
                }

            # Append the recommendation along with a clear declaration of who it's from
            merged_recommendations[target_id]['recommendations'].append({
                'recommender_id': recommender_id,
                'recommendation': data  # Assuming data is the recommendation content
            })

    # Create a new directory for merged files if it doesn't exist
    output_folder = '/Users/vansh/Desktop/EightFoldAISubmission/Merged LORs'
    os.makedirs(output_folder, exist_ok=True)

    # Write merged recommendations to separate JSON files for each target ID
    for target_id, content in merged_recommendations.items():
        output_file_path = os.path.join(output_folder, f'Merged_Recommendations_for_Resume_{target_id}.json')
        
        # Check if the output file already exists
        if os.path.exists(output_file_path):
            print(f"File for ID {target_id} already exists. Skipping...")
            continue  # Skip to the next target ID if the file exists
        
        # Prepare the content to write
        output_content = {
            'target_id': target_id,
            'recommendations': content['recommendations']
        }
        
        with open(output_file_path, 'w') as output_file:
            json.dump(output_content, output_file, indent=4)
        
        print(f"Merged recommendations saved for ID {target_id} in {output_file_path}")

# Usage
folder_path = '/Users/vansh/Desktop/EightFoldAISubmission/Structured LORs'  # Update this to your folder path
merge_recommendations(folder_path)
