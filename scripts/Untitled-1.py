# %%
import os
import openai
import json
import time
import concurrent.futures
from itertools import cycle
from threading import Lock

API_KEYS = [
"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"
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
You are given a resume, and an influence factor scoring system. Your task is to evaluate the resume based on the influence factor and provide a JSON output that includes the following:

1. **Influence Factor Score (1-10)**:
   - Evaluate the candidate's influence level based on the criteria below and provide a detailed breakdown of how the score was calculated:

**Scoring Criteria:**

   - **Job Role Level (Score: 1-5)**:
     - Executive Leadership (5 points): Roles like CEO, CFO, COO, CTO, President, Vice President.
     - Senior Management (4 points): Roles like Director, Senior Manager, Head of Department.
     - Middle Management (3 points): Roles like Manager, Team Lead, Supervisor.
     - Professional Staff (2 points): Roles like Senior Engineer, Senior Analyst, Specialist.
     - Entry-Level Positions (1 point): Roles like Junior Engineer, Assistant, Associate.

   - **Company Size and Influence (Score: 1-3)**:
     - Large Multinational Corporations or Highly Influential Organizations (3 points): Fortune 500 companies, major global brands, top-tier consultancies.
     - Medium-Sized Companies or Well-Known Organizations (2 points): Regional leaders, established mid-sized companies, recognized NGOs.
     - Small Companies or Lesser-Known Organizations (1 point): Startups, local businesses, small nonprofits.

   - **Experience and Tenure (Score: 0-2)**:
     - Extensive Experience (2 points): Over 10 years in their field or role.
     - Moderate Experience (1 point): 3 to 10 years in their field or role.
     - Limited Experience (0 points): Less than 3 years in their field or role.

2. **Calculation**:
   - Add up the points from each category to get the total Influence Factor Score out of 10.

3. Also mention the number of years of experience, if end date is present, current then take "2024" as the present year.
  - If not able to find the working experience store NaN

**Input Example:**
<Input>
{
    "details": {
        "job_history": [
            {
                "role_name": "Senior Project Manager",
                "company_level": "Large Corporation",
                "start_date": "01/2012",
                "end_date": "Present"
            }
        ],
        "education": [
            {
                "university": "XYZ University",
                "start_date": "09/2005",
                "end_date": "06/2009",
                "domain": "Business Administration",
                "level": "Bachelor's"
            }
        ]
    }
}
</Input>

**Expected Output:**
<Output>
{
  "working_experience" : 12
  "influence_factor_score": 9,
  "influence_factor_breakdown": {
    "job_role_level": 4,
    "company_size_and_influence": 3,
    "experience_and_tenure": 2
  },
  "notes": "The candidate's role as a Senior Project Manager at a large corporation, with over 10 years of experience, results in a high influence factor score."
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

# %%
def process_resume(resume_file_path, output_file_path, sys_msg):
    try:
        resume_content = read_json_file(resume_file_path)
        msg = f"Resume {resume_content}"

        api_key = next(api_key_cycle)
        raw_output = llm_invoke(sys_msg, msg, api_key)

        start_idx = raw_output.find("{")
        end_idx = raw_output.rfind("}") + 1
        json_output = raw_output[start_idx:end_idx]

        parsed_output = json.loads(json_output)

        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump({"resume_file": os.path.basename(resume_file_path), "output": parsed_output}, f, ensure_ascii=False, indent=4)

        print(f"Processed {os.path.basename(resume_file_path)}")

    except Exception as e:
        print(f"Error processing {os.path.basename(resume_file_path)}: {e}")

# Multithreading function to process all resumes
def process_all_resumes_multithreaded(resume_directory, output_directory, sys_msg):
    os.makedirs(output_directory, exist_ok=True)
    tasks = []

    for i in range(1000):
        resume_file_path = os.path.join(resume_directory, f"{i}.json")
        
        if not os.path.exists(resume_file_path):
            print(f"Resume file {i}.json not found.")
            continue

        output_file_path = os.path.join(output_directory, f"Processed_Resume_{i}.json")

        if os.path.exists(output_file_path):
            print(f"Already processed Resume {i}. Skipping.")
            continue

        tasks.append((resume_file_path, output_file_path, sys_msg))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_resume, task[0], task[1], task[2]) for task in tasks]
        concurrent.futures.wait(futures)

    print("All evaluations completed.")

# %%
output_directory = "C:/Users/kesha/coding/c/ShitGettingReal"  # Change to your desired output path
resume_directory = "C:/Users/kesha/coding/c/str_data_resumes/str_data_resumes"

# %%
process_all_resumes_multithreaded(resume_directory, output_directory, sys_msg)


