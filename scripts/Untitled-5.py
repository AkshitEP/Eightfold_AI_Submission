# %%
import os
import openai

API_KEY = "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"

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=API_KEY
)

# %%
def llm_invoke(system_prompt,msg):
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
        temperature=0.3
    )

    return (chat_completion.choices[0].message.content)

# %%
system_message_1 = '''
"You are a CV parsing system. Given a CV of 2-3 pages, extract and organize the following information into a structured JSON format.
Pay close attention to the following categories:

Job History (Multiple Entries):
- Role Name: The title of the position held.
- Work Description: The tasks and responsibilities, starting after action words like 'managed', 'developed', 'led', etc.
- Company Level: Whether the company is a startup, mid-level, or large corporation.
- Start Date: The start date of the role in the format 'mm/yyyy'. If only the year is mentioned, assume '01/yyyy'.
- End Date: The end date of the role in the format 'mm/yyyy' or 'Present'. If only the year is mentioned, assume '12/yyyy'.

Education (Multiple Entries):
- University: The institution's name.
- Start Date: The start date of education in the format 'mm/yyyy'. If only the year is mentioned, assume '01/yyyy'.
- End Date: The end date of education in the format 'mm/yyyy' or 'Present'. If only the year is mentioned, assume '12/yyyy'.
- Domain: The field or major of study.
- Level: The degree or qualification obtained (e.g., Bachelor's, Master's).

Projects (Multiple Entries):
- Domain: The field or industry the project relates to.
- Description: A brief description of the project.
- Skills: An array of specific skills used or developed during the project (for HR filtering purposes).

Interests:
- Interests: An array of interests listed by the applicant."

Example Input: The system prompt will guide the parsing of a sample CV input, which might look something like this:

<Input>
Software Engineer at XYZ Corp
2021 - Present

Developed and led a team to build a real-time data analytics platform.
Managed cloud infrastructure and deployed scalable services.
Collaborated with cross-functional teams to optimize performance.
Education
IIT Delhi
2017-2021

Bachelor of Technology in Computer Science
Project: Legal Tech Solution

Developed a legal research tool to streamline case law searches.
Technologies: Python, Flask, React, Machine Learning
</Input>

Expected JSON Output:

<Output/>
{
  "job_history": [
    {
      "role_name": "Software Engineer",
      "work_description": "Developed and led a team to build a real-time data analytics platform. Managed cloud infrastructure and deployed scalable services. Collaborated with cross-functional teams to optimize performance.",
      "company_level": "Mid-level",
      "start_date": "01/2021",
      "end_date": "Present"
    }
  ],
  "education": [
    {
      "university": "IIT Delhi",
      "start_date": "01/2017",
      "end_date": "12/2021",
      "domain": "Computer Science",
      "level": "Bachelor's"
    }
  ],
  "projects": [
    {
      "domain": "Legal Tech",
      "description": "Developed a legal research tool to streamline case law searches.",
      "skills": ["Python", "Flask", "React", "Machine Learning"]
    }
  ],
  "interests": []
}
</Output>
'''

# %%
system_message_2 = '''
"You are a system that evaluates skills and provides skill levels based on job history, education, and projects from a CV's JSON summary. Your tasks are as follows:

**Skills and Skill Level Extraction**:
   - Identify specific skills from the work descriptions, education, and projects.
   - For each skill, assign a skill level (on a scale from 1 to 5):
        1: Basic familiarity – The person has been exposed to the skill, but usage has been limited to beginner tasks or minimal exposure in their role.
        2: Some practical experience – The person has used the skill in a few practical situations but still lacks deep understanding or significant work with it.
        3: Solid working proficiency – The person can work with the skill regularly and efficiently with minimal supervision, demonstrating a good command of the skill.
        4: Strong proficiency with extensive practical experience – The person uses the skill extensively, handles complex tasks related to it, and may mentor others.
        5: Expert level – The person has mastered the skill, having led major projects or teams where the skill was central. They are seen as a go-to resource for this skill.

    - If someone, mentiones some skills in skill section, but their is no backing, put it 0.

     
   **Example Skills**: Accounting, Financial Reconciliation, Budgeting, Leadership, Data Analysis, Project Management, Microsoft Excel, Payroll Management, etc.

Example Input:
<Input>
{
  "job_history": [
    {
      "role_name": "Staff Accountant",
      "work_description": "Complete the monthly financials for seven different medical groups. Reconcile all the bank statements for these groups which include ZBA accounts. Record all the general entries, payroll entries, transaction entries, month end and year end entries, reconcile the balance sheet and income statement accounts, and record the fixed assets and depreciation.",
      "company_level": "Mid-level",
      "start_date": "09/2010",
      "end_date": "Present"
    },
    {
      "role_name": "Administrative Assistant",
      "work_description": "Directed staff of three and managed accounting, budgeting, HR, and administrative responsibilities at state-operated military academy providing education and life skills for at-risk youth.",
      "company_level": "Government",
      "start_date": "07/2008",
      "end_date": "10/2009"
    }
  ],
  "education": [
    {
      "university": "University of Anchorage Alaska",
      "start_date": "01/2009",
      "end_date": "12/2009",
      "domain": "Business Administration/Accounting",
      "level": "Bachelor's"
    }
  ],
  "projects": [],
  "interests": []
}
</Input>

Expected Output:

<Output>
{ 
"skills": [
    {
      "name": "Financial Reconciliation",
      "level": 4,
      "explanation": "Has extensive experience handling monthly financials and reconciling bank statements across multiple medical groups, showing strong proficiency."
    },
    {
      "name": "General Accounting",
      "level": 5,
      "explanation": "Over a decade of experience with all aspects of accounting including payroll, general entries, and asset management, indicating expert-level mastery."
    },
    {
      "name": "Payroll Management",
      "level": 4,
      "explanation": "Handled payroll entries consistently for several years, suggesting a strong proficiency in payroll management."
    },
    {
      "name": "Budgeting",
      "level": 3,
      "explanation": "Managed budgeting responsibilities as an administrative assistant, showing a solid working proficiency."
    },
    {
      "name": "Leadership",
      "level": 3,
      "explanation": "Led a small team in an administrative role, which indicates a solid level of proficiency in leadership."
    },
    {
      "name": "Microsoft Excel",
      "level": 4,
      "explanation": "Likely used extensively for managing financial records and payroll, suggesting strong proficiency."
    }
  ]
}
</Output>
'''



# %%
import json
import os
from PyPDF2 import PdfReader
import time

# Function to process a single resume and save extracted JSON data
def process_resume(i):
    # Path to the PDF
    resume_path = f"./Final_Resumes/Resume_of_ID_{i}.pdf"
    
    # Check if the PDF exists
    if not os.path.exists(resume_path):
        print(f"Resume not found: {resume_path}")
        return

    # Path to save the JSON file
    json_output_path = f"./str_data_resumes/{i}.json"

    # Check if the JSON file already exists
    if os.path.exists(json_output_path):
        print(f"Already processed: {json_output_path}")
        return

    # Retry logic
    for attempt in range(5):
        try:
            # Reading the PDF
            reader = PdfReader(resume_path)
            pdf_text = ""

            # Extracting text from each page
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                pdf_text += page.extract_text() if page.extract_text() else ""

            # Step 1: Invoke the LLM to get initial details
            details = llm_invoke(system_message_1, pdf_text)

            # Step 2: Extract the JSON part from the details
            start_index = details.find("{")
            end_index = details.rfind("}") + 1
            json_part = details[start_index:end_index]

            # Step 3: Parse the extracted JSON part
            parsed_data = json.loads(json_part)

            # Step 4: Invoke the LLM again to get skills information based on the parsed data
            skills = llm_invoke(system_message_2, json_part)

            # Step 5: Extract the JSON part from the skills response
            start_index = skills.find("{")
            end_index = skills.rfind("}") + 1
            json_part_skills = skills[start_index:end_index]

            # Step 6: Parse the skills JSON part
            skills_parsed = json.loads(json_part_skills)

            # Step 7: Assign parsed data to respective variables for clarity
            details = parsed_data
            skills = skills_parsed

            # Prepare the final JSON output
            output_data = {
                "details": details,
                "skills": skills
            }

            # Ensure the output directory exists
            os.makedirs(os.path.dirname(json_output_path), exist_ok=True)

            # Save the output data to a JSON file
            with open(json_output_path, 'w') as json_file:
                json.dump(output_data, json_file, indent=4)

            print(f"Saved: {json_output_path}")
            return  # Exit the function if processing was successful

        except Exception as e:
            print(f"Attempt {attempt + 1} failed for ID {i}: {e}")
            time.sleep(1)  # Sleep for a second before retrying
    print(f"Failed to process ID {i} after 5 attempts.")


# %%
for i in range(1000):
    process_resume(i)

# %%



