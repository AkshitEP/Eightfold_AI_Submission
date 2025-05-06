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
        temperature=0
    )

    return (chat_completion.choices[0].message.content)
    

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
resume_118 = '''
{
    "details": {
        "job_history": [
            {
                "role_name": "Lead Administrator",
                "work_description": "Compose, distribute, and file contracts; design and create operations manuals to guide participants through app use; and follow up with contributing artists or curators through email to ensure that information is clearly understood. Build contact profiles and update contact list information in Salesforce to support organization email lists. Reconfigured/restructured/redesigned the filing system for streamlined use, making projects easier to both archive and find. Anticipate and resolve questions through regular and clear communication with artists and curators about their projects, researching solutions for answers that are otherwise not readily available. Initiate and facilitate the timely payment of artists, verify with executive director that they receive their payment, and update relevant financial records.",
                "company_level": "Mid-level",
                "start_date": "11/2015",
                "end_date": "Present"
            },
            {
                "role_name": "Chaplain Intern",
                "work_description": "Assessed spiritual, emotional, physical needs of people going through crisis within a hospital setting to provide emotional and spiritual support through active listening, advocacy, empathy, or prayer based on the needs of the individual.",
                "company_level": "Mid-level",
                "start_date": "03/2015",
                "end_date": "06/2015"
            },
            {
                "role_name": "Festival Coordinator",
                "work_description": "Enhanced the school's annual week-long arts festival by integrating it with the annual All Nations Banquet, rebranding the All Nations Banquet as the All Nations Food and Art Festival, advocating for the inclusion of the artistic Master's Thesis Capstone Cohort, coordinating student group involvement, and safeguarding event cohesion through brainstorming and development of a festival theme. Supported efforts for contracting poet Scott Cairns for a reading by recruiting academically informed panelists for discussion, planning a book signing, and coordinating a book sales table with artist's book publisher and a local book store. Conceptualized creative problem solving to cut expenses, secured department financial support, targeted allocation of funds, recruited volunteers, and tracked receipts in order to stay under budget and resolve all expenses at the conclusion of the festival.",
                "company_level": "Mid-level",
                "start_date": "01/2015",
                "end_date": "06/2015"
            },
            {
                "role_name": "Master's Thesis Art Project",
                "work_description": "Originated concept, then recruited and collaborated with fifteen volunteer artists of varying genres to produce a high-quality, multi-media artistic project. Utilized correspondence and verbal conversations with volunteers to develop clear project expectations, scheduled and confirmed meetings via Google Calendar, uploaded artistic media to Google Drive, and transferred information within agreed upon deadlines. Hospitality through provision of refreshments and expressed appreciation to ensure artist volunteers felt valued. Secured last-minute travel arrangements for an artist traveling from out of town when her own travel plans fell through.",
                "company_level": "Mid-level",
                "start_date": "09/2014",
                "end_date": "06/2015"
            },
            {
                "role_name": "Co-Chair of Fuller Arts Collective (FAC)",
                "work_description": "Established two FAC events every ten weeks through calendar event planning, coordinating space, catering, and advertising to provide student empowerment through connection and performance opportunities. Composed group news emails and scheduled social media posts to create a strong brand presence for FAC.",
                "company_level": "Mid-level",
                "start_date": "06/2014",
                "end_date": "06/2015"
            },
            {
                "role_name": "Worship Arts Intern",
                "work_description": "Expanded the role of the Worship Arts Department in engaging with various genres of art, designed an online form to streamline registration for a yearly artist showcase, and created a semi-permanent gallery. Initiated team meetings to ensure sensitivity and respect to church tradition in potentially controversial exploration of art and liturgy. Networked with and coordinated volunteer artists in curating their works for various art exhibits within the church. Mediated between the Worship Arts Department and various church departments to ensure a clear communication of ideas and to provide professionalism regarding church engagement with artists.",
                "company_level": "Mid-level",
                "start_date": "09/2013",
                "end_date": "06/2014"
            },
            {
                "role_name": "Barista",
                "work_description": "Served as integral member of a team that produced high-quality products under tight time constraints, with a focus on customer satisfaction; trained new team members to ensure they can perform necessary tasks at expected standards of service; inventoried and organized raw materials.",
                "company_level": "Mid-level",
                "start_date": "08/2009",
                "end_date": "09/2013"
            }
        ],
        "education": [
            {
                "university": "Vanguard University",
                "start_date": "01/2009",
                "end_date": "12/2009",
                "domain": "Theatre Arts",
                "level": "Bachelor's"
            },
            {
                "university": "Fuller Theological Seminary",
                "start_date": "01/2015",
                "end_date": "12/2015",
                "domain": "Worship Theology and the Arts",
                "level": "Master's"
            }
        ],
        "projects": [],
        "interests": []
    },
    "skills": {
        "skills": [
            {
                "name": "Project Management",
                "level": 5,
                "explanation": "Has extensive experience in managing multiple projects, including festivals, events, and artistic projects, indicating expert-level mastery."
            },
            {
                "name": "Leadership",
                "level": 4,
                "explanation": "Has led teams and coordinated events, showing strong proficiency in leadership and team management."
            },
            {
                "name": "Communication",
                "level": 5,
                "explanation": "Has consistently demonstrated excellent communication skills, both written and verbal, in various roles, indicating expert-level mastery."
            },
            {
                "name": "Problem-Solving",
                "level": 4,
                "explanation": "Has shown ability to think creatively and resolve problems in various situations, including event planning and team management, indicating strong proficiency."
            },
            {
                "name": "Time Management",
                "level": 4,
                "explanation": "Has managed multiple tasks and deadlines in various roles, including event planning and team management, indicating strong proficiency."
            },
            {
                "name": "Collaboration",
                "level": 5,
                "explanation": "Has consistently demonstrated ability to work effectively with others, including artists, volunteers, and team members, indicating expert-level mastery."
            },
            {
                "name": "Event Planning",
                "level": 5,
                "explanation": "Has extensive experience in planning and executing events, including festivals and artistic projects, indicating expert-level mastery."
            },
            {
                "name": "Artistic Direction",
                "level": 4,
                "explanation": "Has shown ability to provide artistic direction and guidance to artists and teams, indicating strong proficiency."
            },
            {
                "name": "Salesforce",
                "level": 2,
                "explanation": "Has used Salesforce for contact management, but the extent of usage is not clear, indicating some practical experience."
            },
            {
                "name": "Google Calendar",
                "level": 2,
                "explanation": "Has used Google Calendar for scheduling meetings, but the extent of usage is not clear, indicating some practical experience."
            },
            {
                "name": "Google Drive",
                "level": 2,
                "explanation": "Has used Google Drive for file sharing, but the extent of usage is not clear, indicating some practical experience."
            }
        ]
    }
}
'''

# %%
recommendation_118 = '''
The sales and customer service representative has built an impressive career centered around exceptional customer care, achieving a 100% customer satisfaction rate while supporting a high-volume customer base. An accomplished professional with a master�s degree in Human Resource Development, their ability to effectively communicate and train peers has not only improved team performance but also reduced turnover within the organization. Their HR experience, including developing streamlined onboarding processes and conducting employee evaluations, showcases their dedication to enhancing both employee engagement and operational efficiency.

In this context, I wholeheartedly recommend the lead administrator, whose detail-oriented and proactive approach complements the skill set of the sales and customer service representative. With a strong background in administrative support and project coordination, the lead administrator�s expertise in managing communications, facilitating timely transactions, and implementing innovative solutions significantly aligns with the high standards of service excellence already established in the sales environment. Together, their combined strengths would drive any organization toward greater success.
'''

msg = f"Resume {resume_118} Recommendation {recommendation_118}"

# %%
x = llm_invoke(sys_msg,msg)
print(x)

# %%
import json
start_index = x.find("{")
end_index = x.rfind("}")

json_output = x[start_index:end_index+1]

# Step 6: Parse the skills JSON part
json_final = json.loads(json_output)

print(json_final)

# %%
json_final

# %%



