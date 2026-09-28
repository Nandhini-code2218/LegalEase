import os
import requests
import streamlit as st
from dotenv import load_dotenv
from backend.document_utils import export_txt, export_docx, export_pdf

load_dotenv()
st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")
API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
st.title("⚖️ LegalEase")
st.caption("AI-powered legal document drafting • Create, edit, and export a first draft.")
st.warning("AI-generated content is not legal advice and may contain errors. Have a qualified lawyer review before use. Avoid entering sensitive personal information.")

with st.sidebar:
    st.subheader("Document details")
    choices = ["Employment Contract", "Non-Disclosure Agreement (NDA)", "Residential Lease Agreement", "Freelance Work Contract", "Employment Offer Letter", "Service Agreement", "Other"]
    selected = st.selectbox("Document type", choices)
    doc_type = st.text_input("Specify document type") if selected == "Other" else selected
    jurisdiction = st.text_input("Jurisdiction", "Tamil Nadu, India")
    effective_date = st.text_input("Effective date", "To be agreed")
    parties = st.text_area("Parties and roles", placeholder="Name/entity and role for each party")
    terms = st.text_area("Terms and conditions", placeholder="Separate terms with semicolons or new lines")
    instructions = st.text_area("Additional instructions (optional)")
    logo = st.file_uploader("Optional logo (PNG/JPG)", type=["png", "jpg", "jpeg"])
    generate = st.button("Generate document", type="primary", use_container_width=True)

if "draft" not in st.session_state:
    st.session_state.draft = ""

if generate:
    if not parties.strip() or not terms.strip() or not effective_date.strip() or not doc_type.strip():
        st.error("Please fill in document type, parties, terms, and effective date.")
    else:
        payload = {"document_type": doc_type, "parties": parties, "terms": terms,
                   "effective_date": effective_date, "jurisdiction": jurisdiction or "Not specified",
                   "additional_instructions": instructions}
        with st.spinner("Generating draft with Gemini..."):
            try:
                response = requests.post(f"{API_URL}/api/generate", json=payload, timeout=180)
                if response.ok:
                    st.session_state.draft = response.json()["document"]
                    st.success("Draft generated. Review and edit below.")
                else:
                    st.error(f"API error {response.status_code}: {response.json().get('detail', response.text)}")
            except requests.RequestException as exc:
                st.error(f"Cannot reach backend at {API_URL}. Start FastAPI first. Details: {exc}")

st.subheader("Editable document")
st.session_state.draft = st.text_area("Edit your draft before exporting", value=st.session_state.draft, height=460, label_visibility="collapsed")
if st.session_state.draft.strip():
    logo_bytes = logo.getvalue() if logo else None
    a, b, c = st.columns(3)
    a.download_button("Download TXT", export_txt(st.session_state.draft), "legalease_draft.txt", "text/plain", use_container_width=True)
    b.download_button("Download DOCX", export_docx(st.session_state.draft, doc_type, logo_bytes), "legalease_draft.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    c.download_button("Download PDF", export_pdf(st.session_state.draft, doc_type), "legalease_draft.pdf", "application/pdf", use_container_width=True)
else:
    st.info("Enter details in the sidebar and click Generate document.")
