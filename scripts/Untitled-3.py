# %%
import os
import openai
import json
import time
import concurrent.futures
from itertools import cycle
from threading import Lock
from datetime import datetime


# API_KEY = "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"
API_KEYS = [
    "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",
    "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",
    "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",
    "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",
    "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",
    # "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",
    # "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",
    # "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",
    # "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",
    # "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"
]

# Settings for API limits
MAX_OPS_PER_SECOND = 30  # Max operations per second per API key
MAX_GLOBAL_OPS_PER_SECOND = 100  # Max global operations per second across all keys

# Shared resources for managing API keys and rate limiting
api_key_cycle = cycle(API_KEYS)  # Cycle through API keys
key_usage_counter = {key: 0 for key in API_KEYS}  # Track API key usage
lock = Lock()  # Ensure thread-safe access to shared resources

# OpenAI Client setup function
def get_openai_client(api_key):
    openai.api_key = api_key
    return openai.OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)

# %%
def llm_invoke(system_prompt, msg, api_key):
    """Invoke the LLM model using the provided API key with rate limiting."""
    max_retries = 5
    retry_delay = 5  # Base delay for retry (can be adjusted dynamically)
    
    for attempt in range(max_retries):
        try:
            # Apply rate-limiting logic
            with lock:
                # Ensure we don't exceed per-key and global limits
                while sum(key_usage_counter.values()) >= MAX_GLOBAL_OPS_PER_SECOND or key_usage_counter[api_key] >= MAX_OPS_PER_SECOND:
                    time.sleep(1)  # Wait 1 second and check again
                
                # Increment usage count for this key
                key_usage_counter[api_key] += 1
            
            client = get_openai_client(api_key)
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": msg,
                    }
                ],
                model="llama-3.1-70b-versatile",
                temperature=0
            )
            
            return chat_completion.choices[0].message.content
        
        except openai.error.RateLimitError as e:
            if "Please try again in" in str(e):
                wait_time = int(e.response.json()['error']['message'].split('in')[1].split('s')[0].strip())
                print(f"Rate limit exceeded for API key: {api_key}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Rate limit error: {e}. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
        
        except Exception as e:
            print(f"Failed to invoke LLM with key {api_key}. Attempt {attempt + 1}/{max_retries}. Error: {e}")
            if attempt + 1 == max_retries:
                raise
            time.sleep(retry_delay)
        
        finally:
            with lock:
                # Reset the key usage after each request
                key_usage_counter[api_key] = max(0, key_usage_counter[api_key] - 1)

# %%
sys_msg = '''
You are given a resume and a recommendation letter. Your task is to evaluate the recommendation in relation to the resume and provide a JSON output based on the following criteria:

1. **Relevance Score (1-10)**:
   - 1-3 (Low): The recommendation is barely relevant to the resume, with little or no connection between the skills, experience, or roles mentioned.
   - 4-6 (Moderate): The recommendation mentions some skills or experiences from the resume but lacks substantial detail or alignment with the key areas of expertise.
   - 7-9 (High): The recommendation covers many of the key skills, roles, or accomplishments from the resume, with strong alignment and relevant details.
   - 10 (Exceptional): The recommendation is highly relevant, fully aligning with all key skills, experiences, and roles from the resume, providing strong support for the candidate's qualifications.

2. **Fraud Chance Level (1-5)**:
   - 1 (Low): The recommendation seems genuine and well-supported by the resume. No informal language, statistically improbable data, or red flags.
   - 2 (Moderate): Some minor inconsistencies or exaggerated claims are present, but the recommendation remains largely credible.
   - 3 (Concerning): Multiple claims seem exaggerated or unsupported, with a lack of concrete examples or evidence from the resume.
   - 4 (High): Several aspects of the recommendation are unrealistic, with improper language or statistically improbable claims.
   - 5 (Very High): The majority of the recommendation seems fraudulent, with obvious signs of exaggeration, improper language, or contradictory data.

3. **Recommendation Verification of Skills**:
   - Identify which specific skills mentioned in the resume are validated or referenced by the recommendation.
   - List these skills in an array.

4. **Source of Recommendation**:
   - Identify the relationship of the person giving the recommendation:
     - **Boss/Supervisor**: Directly overseeing or managing the candidate.
     - **Peer**: Colleague or coworker at the same level.
     - **Unknown**: The source of the recommendation is unclear or not specified.

5. **Additional Criteria for Fraud Detection**:
   - **Informal Language**: Check for the use of casual or informal language inappropriate for a formal recommendation. If found, increase the fraud chance level by 1.
   - **Statistically Improbable Claims**: Analyze whether the claims made in the recommendation seem unrealistic given the candidate’s domain, experience level, or position. If such claims are present, set the fraud chance level to 5 and provide reasoning.

**Input Example:**
<Input>
{
    "details": {
        "job_history": [
            {
                "role_name": "Bilingual Language Arts Sixth Grade Teacher",
                "work_description": "Developed and implemented interactive learning mediums to increase student understanding of course materials.",
                "company_level": "Mid-level",
                "start_date": "08/2014",
                "end_date": "Current"
            }
        ],
        "skills": {
            "skills": [
                {
                    "name": "Teaching",
                    "level": 5
                },
                {
                    "name": "Curriculum Development",
                    "level": 4
                }
            ]
        }
    }
}

Recommendation:
"The Bilingual Language Arts Teacher has demonstrated a strong ability to engage students with innovative teaching methods, effectively increasing student learning. Their experience in creating interactive lesson plans and fostering a collaborative classroom environment stands out."
</Input>
**Expected Output:**
<Output>
{
  "relevance_score": 9,
  "fraud_chance_level": 1,
  "fraud_reason": "No red flags or statistically improbable claims detected. Language is formal.",
  "verified_skills": ["Teaching", "Curriculum Development"],
  "recommendation_source": "Unknown",
  "notes" : "The recommendation aligns well with the candidate's skills and experience, providing specific examples of their teaching methods and classroom environment."
}
</Output>
'''

# %%
def extract_text_with_keys(data, indent=0):
    """Recursively extract text from a JSON object, including keys."""
    text = ""
    if isinstance(data, dict):
        for key, value in data.items():
            text += '    ' * indent + f"{key}:\n"  # Indent for structure
            text += extract_text_with_keys(value, indent + 1)  # Recursively process value
    elif isinstance(data, list):
        for item in data:
            text += extract_text_with_keys(item, indent)
    elif isinstance(data, str):
        text += '    ' * indent + f"{data}\n"  # Indent for structure
    else:
        text += '    ' * indent + f"{data}\n"
    return text


def read_json_file(file_path):
    """Read a JSON file and return the extracted text with keys."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return extract_text_with_keys(data).strip()  # Strip to remove extra newline at the end


def read_text_file(file_path):
    """Read a text file and return its content as a string, handling encoding issues."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        # Try a different encoding if UTF-8 fails
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            content = file.read()
    return content


# %%
def process_resume_and_recommendation(resume_file_path, recommendation_file_path, output_file_path, sys_msg):
    """Process a single resume and recommendation pair."""
    try:
        resume_content = read_json_file(resume_file_path)
        recommendation_content = read_text_file(recommendation_file_path)

        msg = f"Resume {resume_content} Recommendation {recommendation_content}"

        # Get an API key for this thread
        api_key = next(api_key_cycle)

        # Invoke the model and get the result
        raw_output = llm_invoke(sys_msg, msg, api_key)

        # Extract the JSON part of the output
        start_idx = raw_output.find("{")
        end_idx = raw_output.rfind("}") + 1
        json_output = raw_output[start_idx:end_idx]

        # Parse JSON safely
        parsed_output = json.loads(json_output)

        # Store the result in a unique JSON file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump({
                "resume_file": os.path.basename(resume_file_path),
                "recommendation_file": os.path.basename(recommendation_file_path),
                "output": parsed_output
            }, f, ensure_ascii=False, indent=4)

        print(f"Processed {os.path.basename(resume_file_path)} and {os.path.basename(recommendation_file_path)}")

    except Exception as e:
        print(f"Error processing {os.path.basename(resume_file_path)} and {os.path.basename(recommendation_file_path)}: {e}")


def process_all_resumes_multithreaded(resume_directory, recommendation_directory_base, output_directory, sys_msg):
    os.makedirs(output_directory, exist_ok=True)

    tasks = []

    # Iterate over resume and recommendation files
    for i in range(1000):
        resume_file_path = os.path.join(resume_directory, f"{i}.json")
        recommendation_folder = os.path.join(recommendation_directory_base, f"Recommendation_Letters_of_ID_{i}")

        if not os.path.exists(resume_file_path):
            print(f"Resume file {i}.json not found.")
            continue

        if os.path.exists(recommendation_folder):
            for recommendation_file in os.listdir(recommendation_folder):
                recommendation_file_path = os.path.join(recommendation_folder, recommendation_file)

                if recommendation_file.endswith('.txt'):
                    recommendation_file_base = os.path.splitext(recommendation_file)[0]
                    output_file_path = os.path.join(output_directory, f"Resume_{i}_Recommendation_{recommendation_file_base}.json")

                    if os.path.exists(output_file_path):
                        print(f"Already processed Resume {i}, Recommendation: {recommendation_file}. Skipping.")
                        continue

                    # Add task to the list
                    tasks.append((resume_file_path, recommendation_file_path, output_file_path, sys_msg))

    # Use ThreadPoolExecutor to process the tasks in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_resume_and_recommendation, task[0], task[1], task[2], task[3]) for task in tasks]
        concurrent.futures.wait(futures)

    print("All evaluations completed.")

# %%
# Directory paths
resume_directory = r"C:\Users\akshi\coding\projects\Hackathon innov8 2.0 final round\str_data_resumes\str_data_resumes"
recommendation_directory_base = r"C:\Users\akshi\coding\projects\Hackathon innov8 2.0 final round\Dataset\Final_Recommendation_Letters"
output_directory = r"C:\Users\akshi\coding\projects\Hackathon innov8 2.0 final round\Evaluations"  # Root folder for storing evaluation results




# %%
# Run the processing with multithreading and retry mechanism
process_all_resumes_multithreaded(resume_directory, recommendation_directory_base, output_directory, sys_msg)


