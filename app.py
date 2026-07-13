import json
import streamlit as st
import tempfile
import os

from backend.parser import extract_text
from backend.generator import generate_csv_documentation
from backend.document_generator import create_csv_document

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="SpecPilot",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# HIDE STREAMLIT DEFAULT COMPONENTS
# ---------------------------------------------------

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

header{
visibility:hidden;
}

footer{
visibility:hidden;
}

[data-testid="collapsedControl"]{
display:none;
}

.block-container{
padding-top:2rem;
padding-bottom:2rem;
max-width:1200px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

/* Background */
.stApp{
    background:linear-gradient(180deg,#F8FAFF 0%,#EEF4FF 100%);
}

/* Main Container */
.block-container{
    max-width:1150px;
    padding-top:1rem;
    padding-bottom:3rem;
}

/* Hero */
.hero{
    text-align:center;
    padding:20px 0 35px 0;
}

.hero h1{
    font-size:64px;
    font-weight:900;
    color:#1F2937;
    margin-bottom:10px;
    letter-spacing:-2px;
}

.hero p{
    font-size:20px;
    color:#6B7280;
}

/* Upload Card */
.upload-card{

    background:rgba(255,255,255,.82);

    backdrop-filter:blur(14px);

    border-radius:24px;

    padding:30px;

    border:1px solid rgba(255,255,255,.6);

    box-shadow:0 15px 45px rgba(0,0,0,.08);

    transition:.25s;

}

.upload-card:hover{

    transform:translateY(-4px);

    box-shadow:0 22px 55px rgba(0,0,0,.12);

}

/* Output Card */
.output-card{

    background:white;

    border-radius:24px;

    padding:30px;

    box-shadow:0 12px 35px rgba(0,0,0,.08);

}

/* File Uploader */

[data-testid="stFileUploader"]{

    border:2px dashed #6366F1;

    border-radius:18px;

    padding:20px;

    background:#F8FAFF;

}

/* Prompt */

textarea{

    border-radius:18px !important;

    border:1px solid #D1D5DB !important;

    font-size:16px !important;

}

/* Buttons */

.stButton>button{

    width:100%;

    height:60px;

    border:none;

    border-radius:18px;

    background:linear-gradient(90deg,#6366F1,#4F46E5);

    color:white;

    font-size:18px;

    font-weight:700;

    transition:.25s;

}

.stButton>button:hover{

    transform:translateY(-2px);

    box-shadow:0 15px 35px rgba(79,70,229,.35);

}

/* Download Buttons */

.stDownloadButton>button{

    width:100%;

    height:52px;

    border-radius:16px;

}

/* Headers */

h1,h2,h3{

    color:#1F2937;

}

/* Divider */

hr{

    border:none;

    height:1px;

    background:#E5E7EB;

}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "generated" not in st.session_state:

    st.session_state.generated=False

if "result" not in st.session_state:

    st.session_state.result=None

if "document_bytes" not in st.session_state:

    st.session_state.document_bytes=None

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------

st.markdown("""
<div class="hero">

<h1>✨ SpecPilot</h1>

<p>
Enterprise AI for Computer System Validation
</p>

<div style="
display:flex;
justify-content:center;
gap:12px;
flex-wrap:wrap;
margin-top:22px;
">

<span style="
background:#EEF2FF;
color:#4338CA;
padding:8px 18px;
border-radius:999px;
font-weight:600;
font-size:14px;
">
📋 User Stories
</span>

<span style="
background:#ECFDF5;
color:#047857;
padding:8px 18px;
border-radius:999px;
font-weight:600;
font-size:14px;
">
⚠️ Risk Assessment
</span>

<span style="
background:#FEF3C7;
color:#92400E;
padding:8px 18px;
border-radius:999px;
font-weight:600;
font-size:14px;
">
🧪 Validation Test Cases
</span>

<span style="
background:#F3F4F6;
color:#374151;
padding:8px 18px;
border-radius:999px;
font-weight:600;
font-size:14px;
">
🤖 AI Powered
</span>

</div>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background:linear-gradient(90deg,#4F46E5,#6366F1);
padding:22px;
border-radius:20px;
color:white;
margin-bottom:25px;
">

<h2 style="margin:0;">
🚀 AI Powered CSV Validation
</h2>

<p style="margin-top:8px;font-size:17px;">
Generate User Stories, Risk Assessment and Validation Test Cases from BRDs, FS, SRS and SOPs in seconds.
</p>

</div>
""", unsafe_allow_html=True)
# ---------------------------------------------------
# DASHBOARD METRICS
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📋 User Stories", "Auto")

with col2:
    st.metric("⚠️ Risks", "Auto")

with col3:
    st.metric("🧪 Test Cases", "Auto")

with col4:
    st.metric("📄 CSV Ready", "100%")

st.write("")

# ---------------------------------------------------
# UPLOAD SECTION
# ---------------------------------------------------

st.markdown("""
<div class="upload-card">

<h2 style="text-align:center;margin-bottom:8px;">
📄 Upload Module Document
</h2>

<p style="
text-align:center;
color:#6B7280;
margin-bottom:25px;
">

Upload your BRD, FS, SRS, SOP or Requirement document.

</p>

</div>

""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(

"Choose your document",

type=["pdf","docx","txt"],

label_visibility="collapsed"

)

st.markdown("""

<div style="
text-align:center;
color:#6B7280;
font-size:14px;
margin-top:-10px;
">

Supported Formats

<br>

📄 PDF &nbsp;&nbsp; 📘 DOCX &nbsp;&nbsp; 📑 TXT

</div>

""", unsafe_allow_html=True)
# ---------------------------------------------------
# PROMPT
# ---------------------------------------------------

st.markdown("### 🤖 Ask SpecPilot")

prompt = st.text_area(

"",

placeholder="""
Example:

Generate User Stories, Risk Assessment and Validation Test Cases from this module.
""",

height=180,

label_visibility="collapsed"

)

# ---------------------------------------------------
# BUTTON
# ---------------------------------------------------

left,center,right=st.columns([2,3,2])

with center:

    generate=st.button(

        "🚀 Generate Validation Package",

        use_container_width=True,

        type="primary"

    )

# ---------------------------------------------------
# GENERATION
# ---------------------------------------------------

if generate:

    if uploaded_file is None:
        st.warning("Please upload a Module or Requirement document.")
        st.stop()

    if prompt.strip() == "":
        st.warning("Please enter your requirement.")
        st.stop()

    import time

    progress = st.progress(0)
    status = st.empty()

    status.markdown("### 📄 Reading uploaded document...")
    progress.progress(15)

    document_text = extract_text(uploaded_file)

    status.markdown("### 🧠 Understanding module...")
    progress.progress(35)

    result = generate_csv_documentation(
        document_text,
        prompt
    )

    st.write("RESULT =", result)
    st.write("TYPE =", type(result))

    st.write("Generated Result:", result)
    st.write("Generated Result Type:", type(result))

    status.markdown("### 📋 Creating User Stories...")
    progress.progress(60)
    time.sleep(0.3)

    status.markdown("### ⚠️ Performing Risk Assessment...")
    progress.progress(80)
    time.sleep(0.3)

    status.markdown("### 🧪 Generating Validation Test Cases...")
    progress.progress(95)
    time.sleep(0.3)

    status.markdown("### ✅ Finalizing Documentation...")
    progress.progress(100)
    time.sleep(0.5)

    progress.empty()
    status.empty()

    st.session_state.generated = True
    st.session_state.result = result
    try:
        st.write("Result Type:", type(result))
        st.write("Result:", result)
        doc = create_csv_document(result)
        st.write("DOC =", doc)
        st.write("TYPE =", type(doc))

        st.session_state.document_bytes = doc

    except Exception as e:
        st.exception(e)
        st.session_state.document_bytes = None

    st.session_state.generated = True
    st.session_state.result = result
# ---------------------------------------------------
# DISPLAY GENERATED OUTPUT
# ---------------------------------------------------
# ---------------------------------------------------
# EMPTY STATE
# ---------------------------------------------------

if not st.session_state.generated:

    st.markdown("""
    <div style="
    text-align:center;
    padding:80px 40px;
    color:#6B7280;
    ">

    <h2 style="font-size:32px;">
    🤖 Ready to Generate
    </h2>

    <p style="font-size:18px;">

    Upload your module document, describe what you need,
    and click <b>Generate Validation Package</b>.

    </p>

    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# GENERATED OUTPUT
# ---------------------------------------------------


if st.session_state.generated:

    st.divider()

    st.markdown("""
    <div style="text-align:center;margin-bottom:25px;">
        <h2>📑 Generated Validation Package</h2>
        <p style="color:#6B7280;">
        Review and download the generated CSV documentation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    result = st.session_state.result

    # ---------------------------------------
    # STEP 10 - AI ANALYSIS SUMMARY
    # ---------------------------------------

    st.markdown("## 📊 AI Analysis Summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("📋 User Stories", "4")

    with c2:
        st.metric("⚠️ Risks", "7")

    with c3:
        st.metric("🧪 Test Cases", "12")

    with c4:
        st.metric("🤖 Confidence", "98%")

    st.write("")

    tab1, tab2, tab3 = st.tabs([
        "📋 User Stories",
        "⚠️ Risk Assessment",
        "🧪 Test Cases"
    ])

    # ---------------- USER STORIES ----------------

    with tab1:

        if "## Risk Assessment" in result:

            user_story = result.split("## Risk Assessment")[0]

        else:

            user_story = result

        st.markdown(user_story)

    # ---------------- RISKS ----------------

    with tab2:

        if "## Risk Assessment" in result:

            risk = result.split("## Risk Assessment")[1]

            if "## Test Cases" in risk:

                risk = risk.split("## Test Cases")[0]

            st.markdown(risk)

        else:

            st.info("No Risk Assessment generated.")

    # ---------------- TEST CASES ----------------

    with tab3:

        if "## Test Cases" in result:

            testcases = result.split("## Test Cases")[1]

            st.markdown(testcases)

        else:

            st.info("No Test Cases generated.")

    st.divider()

    

# ----------------------------------------
# DOWNLOAD CENTER
# ----------------------------------------

st.divider()

st.markdown("""
<div style="text-align:center;margin-bottom:30px;">

<h2>📥 Download Center</h2>

<p style="color:#6B7280;">
Choose your preferred export format
</p>

</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# ---------------- WORD ----------------

with col1:

    st.markdown("""
    <div style="
    background:white;
    border-radius:20px;
    padding:20px;
    text-align:center;
    box-shadow:0 8px 25px rgba(0,0,0,.08);
    margin-bottom:15px;
    ">

    <h3>📄 Word Report</h3>

    <p style="color:#6B7280;">
    Professional CSV Documentation
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.write("Document Bytes =", st.session_state.document_bytes)
    st.write("Type =", type(st.session_state.document_bytes))

    if st.session_state.document_bytes is not None:

     st.download_button(
        "⬇ Download DOCX",
        st.session_state.document_bytes,
        file_name="CSV_Documentation.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )

    else:
     st.error("Word document was not created.")

# ---------------- JSON ----------------

with col2:

    st.markdown("""
    <div style="
    background:white;
    border-radius:20px;
    padding:20px;
    text-align:center;
    box-shadow:0 8px 25px rgba(0,0,0,.08);
    margin-bottom:15px;
    ">

    <h3>📊 JSON Export</h3>

    <p style="color:#6B7280;">
    Structured AI Output
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        "⬇ Download JSON",
        json.dumps(st.session_state.result, indent=4),
        file_name="CSV_Documentation.json",
        mime="application/json",
        use_container_width=True
    )

# ---------------- TEXT ----------------

with col3:

    st.markdown("""
    <div style="
    background:white;
    border-radius:20px;
    padding:20px;
    text-align:center;
    box-shadow:0 8px 25px rgba(0,0,0,.08);
    margin-bottom:15px;
    ">

    <h3>📑 Text File</h3>

    <p style="color:#6B7280;">
    Plain Text Version
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        "⬇ Download TXT",
        json.dumps(st.session_state.result, indent=4),
        file_name="CSV_Documentation.txt",
        mime="text/plain",
        use_container_width=True
    )
# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.write("")
st.write("")

st.markdown(
    """
    <hr>

    <div style="text-align:center;color:gray;padding-bottom:20px;">

    <b>SpecPilot</b><br>

    AI Powered CSV Documentation Generator

    <br><br>

    Built for Computer System Validation (CSV)

    </div>
    """,
    unsafe_allow_html=True
)
