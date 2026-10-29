
import streamlit as st
from agent import run_job_application_crew

st.set_page_config(
    page_title="CareerCraft AI",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp {
        background: #F5F7FC;
    }

    [data-testid="stSidebar"] {
        background: #172554;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF;
    }

    .hero {
        background: linear-gradient(120deg, #172554, #4338CA);
        padding: 32px;
        border-radius: 20px;
        color: white;
        margin-bottom: 24px;
    }

    .hero h1 {
        color: white;
        font-size: 36px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #E0E7FF;
        font-size: 16px;
    }

    .section-title {
        color: #172554;
        font-size: 22px;
        font-weight: 700;
        margin: 14px 0;
    }

    div[data-testid="stForm"],
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: white;
        border-radius: 14px;
    }

    .stTextArea textarea,
    .stTextInput input {
        background: #FFFFFF;
        border-radius: 10px;
    }

    .stButton > button,
    .stDownloadButton > button {
        background: #4338CA;
        color: white;
        border: none;
        border-radius: 10px;
        min-height: 44px;
        font-weight: 600;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: #3730A3;
        color: white;
        border: none;
    }

    .hint {
        color: #64748B;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("# 💼 CareerCraft AI")
    st.caption("Your AI-powered career assistant")
    st.divider()

    st.markdown("### Navigation")
    st.markdown("✦ Create application")
    st.markdown("✦ Generated results")

    st.divider()
    st.markdown("**Powered by**")
    st.caption("CrewAI · Groq · Streamlit")

st.markdown("""
<div class="hero">
    <h1>Build your next career move.</h1>
    <p>
        Turn a job description and your real experience into
        personalized application materials with AI.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">01 · Job details</div>',
    unsafe_allow_html=True
)

job_desc = st.text_area(
    "Job description",
    height=190,
    placeholder=(
        "Paste the job responsibilities, required skills, "
        "qualifications and experience here..."
    ),
)

job_location = st.text_input(
    "Job location",
    placeholder="e.g. Mumbai, India",
)

st.markdown(
    '<div class="section-title">02 · Your profile</div>',
    unsafe_allow_html=True
)

candidate_profile = st.text_area(
    "Candidate profile",
    height=190,
    placeholder=(
        "Add your education, technical skills, projects, "
        "certifications and experience..."
    ),
)

st.caption(
    "Tip: Include genuine skills and achievements so the AI "
    "can personalize your application accurately."
)

generate = st.button(
    "✨ Generate my application",
    type="primary",
    use_container_width=True,
)

if generate:
    if not job_desc.strip() or not candidate_profile.strip():
        st.warning(
            "Please enter both the job description and your profile."
        )
    else:
        prompt = job_desc.strip()

        if job_location.strip():
            prompt += (
                "\n\nJob location: "
                + job_location.strip()
                + "\nUse this location when discussing salary."
            )

        with st.spinner(
            "Your AI agents are analyzing the role and preparing your materials..."
        ):
            try:
                result = run_job_application_crew(
                    prompt,
                    candidate_profile.strip(),
                )
                st.session_state["application_result"] = result
            except Exception as error:
                st.error("Could not generate your application.")
                st.code(str(error))

if "application_result" in st.session_state:
    st.divider()
    st.markdown(
        '<div class="section-title">03 · Your application package</div>',
        unsafe_allow_html=True
    )

    result = st.session_state["application_result"]

    st.success("Your application package is ready.")

    tab1, tab2 = st.tabs(["📄 Application materials", "⬇️ Export"])

    with tab1:
        st.markdown(result)

    with tab2:
        st.download_button(
            "Download application package",
            data=result,
            file_name="career_application.txt",
            mime="text/plain",
            use_container_width=True,
        )

    st.caption(
        "Review all AI-generated content before using it. "
        "Remove any inaccurate claims or achievements."
    )
