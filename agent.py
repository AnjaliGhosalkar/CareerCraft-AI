
"""
Job Application Agent using CrewAI and Groq.

Generates:
- Job requirement analysis
- Tailored cover letter
- Resume bullet points
- Interview questions and answer frameworks
- Approximate salary negotiation guidance
"""

import argparse
import os

from crewai import Agent, Crew, LLM, Process, Task
from dotenv import load_dotenv

load_dotenv()

SAMPLE_JOB = """Senior Python Engineer at Stripe

Requirements:
- 5+ years of Python development
- Experience with distributed systems
- Strong understanding of REST APIs and microservices
- Experience with PostgreSQL and Redis
- Kubernetes experience preferred
- Strong communication skills

Responsibilities:
- Design and build high-performance APIs
- Lead technical design reviews
- Mentor junior engineers
- Collaborate with product managers
"""

SAMPLE_CANDIDATE = """
Jane Doe — 7 years Python experience
Current role: Senior Software Engineer at DataCorp
Skills: Python, FastAPI, Django, PostgreSQL, Redis,
Docker, Kubernetes, AWS

Achievements:
- Built an API platform handling 5M requests/day
- Led a team of 4 engineers
- Reduced API latency by 40%
- Mentored 3 junior engineers

Education: BS Computer Science, UC Berkeley
"""


def run_job_application_crew(job_desc: str, candidate_profile: str) -> str:
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError(
            "GROQ_API_KEY not found. Check your .env file."
        )

    llm = LLM(
        model="groq/openai/gpt-oss-20b",
        api_key=groq_api_key,
        temperature=0.4,
    )

    analyst = Agent(
        role="Job Requirements Analyst",
        goal=(
            "Identify the most important job requirements, required skills, "
            "company values, and relevant keywords."
        ),
        backstory=(
            "You are an experienced job requirements analyst who helps "
            "candidates understand what employers are looking for."
        ),
        llm=llm,
        verbose=False,
    )

    writer = Agent(
        role="Career Coach and Application Writer",
        goal=(
            "Prepare relevant, professional application materials "
            "based on the job description and candidate profile."
        ),
        backstory=(
            "You are a career coach specializing in resumes, cover letters, "
            "interview preparation, and salary negotiation."
        ),
        llm=llm,
        verbose=False,
    )

    analyst_task = Task(
        description=f"""
Analyze this job description:

{job_desc}

Identify:
1. The top five required skills
2. Company culture signals
3. The employer's main priorities
4. Potential red flags or unclear requirements
5. Important keywords for the application
""",
        agent=analyst,
        expected_output=(
            "A structured analysis of required skills, employer priorities, "
            "culture signals, keywords, and potential red flags."
        ),
    )

    application_task = Task(
        description=f"""
Use the job analysis and this candidate profile:

{candidate_profile}

Prepare the following:

1. COVER LETTER:
   Write 250-300 words with an opening, evidence of relevant experience,
   and a professional closing.

2. RESUME BULLETS:
   Write five targeted resume bullet points.

3. INTERVIEW PREPARATION:
   Provide ten likely interview questions: five behavioral and five
   technical. Include suggested answer frameworks.

4. SALARY NEGOTIATION:
   Provide an approximate salary range, stating that it depends on
   location, experience, and current market conditions.

Important:
- Do not invent candidate qualifications or achievements.
- Base all claims on the supplied candidate profile.
- Clearly identify estimates and assumptions.
""",
        agent=writer,
        expected_output=(
            "A cover letter, five resume bullets, ten interview questions "
            "with answer frameworks, and salary negotiation guidance."
        ),
        context=[analyst_task],
    )

    crew = Crew(
        agents=[analyst, writer],
        tasks=[analyst_task, application_task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    return str(result)


def main():
    parser = argparse.ArgumentParser(
        description="Job Application Agent powered by CrewAI and Groq"
    )

    parser.add_argument(
        "--job-desc",
        default=SAMPLE_JOB,
        help="Job description text",
    )

    parser.add_argument(
        "--candidate",
        default=SAMPLE_CANDIDATE,
        help="Candidate profile summary",
    )

    args = parser.parse_args()

    print("\nPreparing job application materials...\n")

    try:
        result = run_job_application_crew(
            args.job_desc,
            args.candidate,
        )

        print("=" * 60)
        print("JOB APPLICATION PACKAGE")
        print("=" * 60)
        print(result)

    except Exception as error:
        print("\nThe agent could not complete the request.")
        print("Error:", error)
        print(
            "\nCheck your Groq API key, model availability, "
            "internet connection, and API limits."
        )


if __name__ == "__main__":
    main()
