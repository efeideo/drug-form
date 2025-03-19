import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv
from send_email import send_email
import re

load_dotenv()

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = 0
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# Function to navigate between pages
def next_page():
    st.session_state.page += 1

def previous_page():
    st.session_state.page -= 1

def navigate_pages():
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.session_state.page > 0:
            st.button("Previous", key="prev", on_click=previous_page)
    with col2:
        if st.session_state.page < 5:
            st.button("Next", key="next", on_click=next_page)

# ---- Page Starts ----
st.title("Belinostat & Pralatrexate MAP – Patient Access Form")

# Page 0: Disclaimer
if st.session_state.page == 0:
    st.header("Disclaimer")
    st.write("""
    Are you a Healthcare Professional (HCP)? By proceeding, you confirm that you are a licensed healthcare provider.
    """)
    if st.button("Yes, I am an HCP", key="hpc"):
        st.session_state.page += 1
        st.rerun()

# Page 1: Prescribing Physician Information
elif st.session_state.page == 1:
    st.markdown("## :blue[Section A:] Prescribing Physician Information")

    # Country selectbox with default value based on session state
    country_options = ["Select Country", "Switzerland", "France", "Germany", "United Kingdom"]
    default_country = st.session_state.form_data.get("phys_country", "Select Country")
    phys_country = st.selectbox("Country", country_options, index=country_options.index(default_country))
    st.session_state.form_data["phys_country"] = phys_country

    # Text input for physician name
    phys_name = st.text_input("Physician Name", st.session_state.form_data.get("phys_name", ""))
    st.session_state.form_data["phys_name"] = phys_name

    # Text input for physician email
    phys_email = st.text_input("Email Address", st.session_state.form_data.get("phys_email", ""))
    if phys_email and not re.match(r"[^@]+@[^@]+\.[^@]+", phys_email):
        st.error("Please enter a valid email address.")
    st.session_state.form_data["phys_email"] = phys_email

    phys_hospital = st.text_input("Hospital/Treatment Center", st.session_state.form_data.get("phys_hospital", ""))
    st.session_state.form_data["phys_hospital"] = phys_hospital
    navigate_pages()

# Page 2: Patient Demographics & Clinical Characteristics
elif st.session_state.page == 2:
    st.write(":blue[Section B]: Patient Information – Demographics & Clinical Characteristics")
    
    # Sex radio button
    sex_options = ["Male", "Female"]
    if "patient_sex_widget" not in st.session_state:
        st.session_state.patient_sex_widget = st.session_state.form_data.get("patient_sex", sex_options[0])
    patient_sex = st.radio("Sex *", sex_options, key="patient_sex_widget")
    st.session_state.form_data["patient_sex"] = st.session_state.patient_sex_widget

    # Birth Year selectbox
    birth_years = list(range(1920, datetime.now().year + 1))
    if "birth_year_widget" not in st.session_state:
        st.session_state.birth_year_widget = st.session_state.form_data.get("birth_year", birth_years[0])
    birth_year_index = birth_years.index(st.session_state.birth_year_widget) if st.session_state.birth_year_widget in birth_years else 0
    birth_year = st.selectbox("Birth Year *", birth_years, key="birth_year_widget", index=birth_year_index)
    st.session_state.form_data["birth_year"] = st.session_state.birth_year_widget

    # Height selectbox
    heights = list(range(100, 221))
    if "height_widget" not in st.session_state:
        st.session_state.height_widget = st.session_state.form_data.get("height", heights[0])
    height_index = heights.index(st.session_state.height_widget) if st.session_state.height_widget in heights else 0
    height = st.selectbox("Height (cm) *", heights, key="height_widget", index=height_index)
    st.session_state.form_data["height"] = st.session_state.height_widget

    # Weight selectbox
    weights = list(range(20, 201))
    if "weight_widget" not in st.session_state:
        st.session_state.weight_widget = st.session_state.form_data.get("weight", weights[0])
    weight_index = weights.index(st.session_state.weight_widget) if st.session_state.weight_widget in weights else 0
    weight = st.selectbox("Weight (kg) *", weights, key="weight_widget", index=weight_index)
    st.session_state.form_data["weight"] = st.session_state.weight_widget

    # Diagnosis Year selectbox
    diag_years = list(range(1950, datetime.now().year + 1))
    if "diag_year_widget" not in st.session_state:
        st.session_state.diag_year_widget = st.session_state.form_data.get("diag_year", diag_years[0])
    diag_year_index = diag_years.index(st.session_state.diag_year_widget) if st.session_state.diag_year_widget in diag_years else 0
    diag_year = st.selectbox("Initial Diagnosis Year *", diag_years, key="diag_year_widget", index=diag_year_index)
    st.session_state.form_data["diag_year"] = st.session_state.diag_year_widget

    # T-Cell Diagnosis radio button
    tcell_options = ["PTCL", "CTCL"]
    if "tcell_diagnosis_widget" not in st.session_state:
        st.session_state.tcell_diagnosis_widget = st.session_state.form_data.get("tcell_diagnosis", tcell_options[0])
    tcell_diagnosis = st.radio("Diagnosis of T-Cell Lymphoma *", tcell_options, key="tcell_diagnosis_widget")
    st.session_state.form_data["tcell_diagnosis"] = st.session_state.tcell_diagnosis_widget

    # Conditional subtype questions based on T-Cell Diagnosis
    if st.session_state.tcell_diagnosis_widget == "PTCL":
        ptcl_options = ["Select Subtype", "PTCL-NOS", "AITL", "ALCL", "Extra-nodal", "Other"]
        if "ptcl_subtype_widget" not in st.session_state:
            st.session_state.ptcl_subtype_widget = st.session_state.form_data.get("ptcl_subtype", ptcl_options[0])
        ptcl_subtype = st.selectbox("Subtype (PTCL) *", ptcl_options, key="ptcl_subtype_widget")
        st.session_state.form_data["ptcl_subtype"] = st.session_state.ptcl_subtype_widget

        if st.session_state.ptcl_subtype_widget in ["Extra-nodal", "Other"]:
            if "ptcl_extra_other_widget" not in st.session_state:
                st.session_state.ptcl_extra_other_widget = st.session_state.form_data.get("ptcl_extra_other", "")
            ptcl_extra_other = st.text_input("Specify subtype...", key="ptcl_extra_other_widget")
            st.session_state.form_data["ptcl_extra_other"] = st.session_state.ptcl_extra_other_widget
    elif st.session_state.tcell_diagnosis_widget == "CTCL":
        ctcl_options = ["Select Subtype", "Mycosis Fungoides", "Sezary Syndrome", "Other"]
        if "ctcl_subtype_widget" not in st.session_state:
            st.session_state.ctcl_subtype_widget = st.session_state.form_data.get("ctcl_subtype", ctcl_options[0])
        ctcl_subtype = st.selectbox("Subtype (CTCL) *", ctcl_options, key="ctcl_subtype_widget")
        st.session_state.form_data["ctcl_subtype"] = st.session_state.ctcl_subtype_widget

        if st.session_state.ctcl_subtype_widget == "Other":
            if "ctcl_other_widget" not in st.session_state:
                st.session_state.ctcl_other_widget = st.session_state.form_data.get("ctcl_other", "")
            ctcl_other = st.text_input("Specify subtype...", key="ctcl_other_widget")
            st.session_state.form_data["ctcl_other"] = st.session_state.ctcl_other_widget

    navigate_pages()

# Page 3: Diagnostic Algorithm
elif st.session_state.page == 3:
    st.markdown("## :blue[Section C:] Patient Information – Diagnostic Algorithm")

    # Time to Diagnosis
    default_time = st.session_state.form_data.get("time_to_diagnosis", 0)
    time_to_diagnosis = st.number_input("Time to Diagnosis", min_value=0, value=default_time)
    st.session_state.form_data["time_to_diagnosis"] = int(time_to_diagnosis)

    # Country selectbox with default value based on session state
    unit_options = ["weeks", "months"]
    default_unit = st.session_state.form_data.get("time_to_diagnosis_unit", unit_options[0])
    time_unit = st.selectbox("Unit", unit_options, index=unit_options.index(default_unit))
    st.session_state.form_data["time_to_diagnosis_unit"] = time_unit

    # Diagnostic Tests Used
    diag_tests_options = ["Flow Cytometry", "Genetic Testing", "Immunohistochemistry", "Other"]
    selected_diag_tests = st.session_state.form_data.get("diag_tests", [])

    # Ensure the widget key is initialized only once
    if "diag_tests_widget" not in st.session_state:
        st.session_state.diag_tests_widget = st.session_state.form_data.get("diag_tests", [])

    diag_tests = st.multiselect(
        "Diagnostic Tests Used *",
        options=diag_tests_options,
        key="diag_tests_widget",
    )
    # Update the form_data dictionary with the widget value
    st.session_state.form_data["diag_tests"] = st.session_state.diag_tests_widget

     # Other Diagnostic Test if selected
    if "Other" in diag_tests:
        default_other_test = st.session_state.form_data.get("diag_test_other_text", "")
        diag_test_other_text = st.text_input("Other test...", key="diag_test_other_text", value=default_other_test)
        st.session_state.form_data["diag_test_other_text"] = diag_test_other_text

    # Types of Specimens Used
    if "specimen_type_widget" not in st.session_state:
        st.session_state.specimen_type_widget = st.session_state.form_data.get("specimen_type", [])

    specimen_type = st.multiselect(
        "Types of Specimens Used",
        ["Bone Marrow", "Whole Blood", "Biopsy", "Other"],
        key="specimen_type_widget"
    )

    st.session_state.form_data["specimen_type"] = st.session_state.specimen_type_widget

    # Other Specimen if selected
    if "Other" in specimen_type:
        default_specimen_other = st.session_state.form_data.get("specimen_other_text", "")
        specimen_other_text = st.text_input("Other specimen...", key="specimen_other_text", value=default_specimen_other)
        st.session_state.form_data["specimen_other_text"] = specimen_other_text

    # Biomarkers Considered
    if "biomarkers_widget" not in st.session_state:
        st.session_state.biomarkers_widget = st.session_state.form_data.get("biomarkers", [])

    biomarkers = st.multiselect(
        "Biomarkers Considered",
        ["Immunophenotypic Markers", "Genetic Markers", "Transcription Factors", "Serum Markers", 
        "Metabolic Markers", "Cell Proliferation Markers", "EBV", "HIV", "HTLV-1", "TFH Markers", "Other"],
        key="biomarkers_widget"
    )
    st.session_state.form_data["biomarkers"] = st.session_state.biomarkers_widget

    # Other Biomarkers if selected
    if "Other" in biomarkers:
        default_biom_other = st.session_state.form_data.get("biom_other_text", "")
        biom_other_text = st.text_input("Other biomarkers...", key="biom_other_text", value=default_biom_other)
        st.session_state.form_data["biom_other_text"] = biom_other_text

    # Cytogenetic Abnormalities
    cytogenetics_options = ["Yes", "No"]

    # One-time initialization of the widget's state
    if "cytogenetics_widget" not in st.session_state:
        st.session_state.cytogenetics_widget = st.session_state.form_data.get("cytogenetics", cytogenetics_options[0])

    # Render the radio button using the dedicated widget key
    cytogenetics = st.radio("Cytogenetic Abnormalities?", options=cytogenetics_options, key="cytogenetics_widget")

    # Update the form_data with the current widget value
    st.session_state.form_data["cytogenetics"] = st.session_state.cytogenetics_widget

    # Specify Cytogenetic Details if Yes
    if cytogenetics == "Yes":
        default_cyto_text = st.session_state.form_data.get("cytogenetic_text", "")
        cytogenetic_text = st.text_input("If yes, specify:", key="cytogenetic_text", value=default_cyto_text)
        st.session_state.form_data["cytogenetic_text"] = cytogenetic_text

    # Biological Specimens Available for research
    specimens_avail_options = ["Yes", "No"]

    # One-time initialization for the widget's state
    if "specimens_avail_widget" not in st.session_state:
        st.session_state.specimens_avail_widget = st.session_state.form_data.get("specimens_avail", specimens_avail_options[0])

    # Render the radio button with the dedicated widget key
    specimens_avail = st.radio(
        "Biological Specimens Available for research?",
        options=specimens_avail_options,
        key="specimens_avail_widget"
    )
    # Update your form_data with the widget's value
    st.session_state.form_data["specimens_avail"] = st.session_state.specimens_avail_widget

    # If Specimens are Available, Choose the Available Specimens
    if specimens_avail == "Yes":
        # Initialize the multiselect widget key if not already in session state
        if "specimen_available_type_widget" not in st.session_state:
            st.session_state.specimen_available_type_widget = st.session_state.form_data.get("specimen_available_type", [])
        
        specimen_available_type = st.multiselect(
            "Available Specimens:",
            ["FFPE", "Frozen Tissue", "Other"],
            key="specimen_available_type_widget"
        )
        st.session_state.form_data["specimen_available_type"] = st.session_state.specimen_available_type_widget

        # If "Other" is selected, display a text input for additional info
        if "Other" in specimen_available_type:
            if "spec_avail_other_text_widget" not in st.session_state:
                st.session_state.spec_avail_other_text_widget = st.session_state.form_data.get("spec_avail_other_text", "")
            spec_avail_other_text = st.text_input(
                "Other specimen type...", 
                key="spec_avail_other_text_widget"
            )
            st.session_state.form_data["spec_avail_other_text"] = spec_avail_other_text

    navigate_pages()

# Page 4: Treatment Algorithm
elif st.session_state.page == 4:
    st.markdown("## :blue[Section D:] Patient Information – Treatment Algorithm")
    
    # Number of Prior Systemic Therapies
    num_therapies_options = ["Select Number", "0", "1", "2", "3"]
    if "num_therapies_widget" not in st.session_state:
        st.session_state.num_therapies_widget = st.session_state.form_data.get("num_therapies", "Select Number")
    default_num_index = num_therapies_options.index(st.session_state.num_therapies_widget) if st.session_state.num_therapies_widget in num_therapies_options else 0
    num_therapies = st.selectbox("Number of Prior Systemic Therapies *", 
                                 num_therapies_options, 
                                 key="num_therapies_widget", 
                                 index=default_num_index)
    st.session_state.form_data["num_therapies"] = st.session_state.num_therapies_widget

    # 1st Line Therapy (if applicable)
    if st.session_state.num_therapies_widget != "0":
        st.subheader("1st Line Therapy")
        if "therapy1_type_widget" not in st.session_state:
            st.session_state.therapy1_type_widget = st.session_state.form_data.get("therapy1_type", "")
        therapy1_type = st.text_input("Type of therapy (regimen)", key="therapy1_type_widget")
        st.session_state.form_data["therapy1_type"] = st.session_state.therapy1_type_widget

        cycles_range = list(range(1, 21))
        if "therapy1_cycles_widget" not in st.session_state:
            st.session_state.therapy1_cycles_widget = st.session_state.form_data.get("therapy1_cycles", 1)
        default_cycle_index = cycles_range.index(st.session_state.therapy1_cycles_widget) if st.session_state.therapy1_cycles_widget in cycles_range else 0
        therapy1_cycles = st.selectbox("Number of cycles", 
                                       cycles_range, 
                                       key="therapy1_cycles_widget", 
                                       index=default_cycle_index)
        st.session_state.form_data["therapy1_cycles"] = st.session_state.therapy1_cycles_widget

        outcome_options = ["CR", "PR", "SD", "PD"]
        if "therapy1_outcome_widget" not in st.session_state:
            st.session_state.therapy1_outcome_widget = st.session_state.form_data.get("therapy1_outcome", outcome_options[0])
        default_outcome_index = outcome_options.index(st.session_state.therapy1_outcome_widget) if st.session_state.therapy1_outcome_widget in outcome_options else 0
        therapy1_outcome = st.radio("Outcome", 
                                    outcome_options, 
                                    key="therapy1_outcome_widget", 
                                    index=default_outcome_index)
        st.session_state.form_data["therapy1_outcome"] = st.session_state.therapy1_outcome_widget

        duration_range = list(range(1, 61))
        if "therapy1_duration_widget" not in st.session_state:
            st.session_state.therapy1_duration_widget = st.session_state.form_data.get("therapy1_duration", 1)
        default_duration_index = duration_range.index(st.session_state.therapy1_duration_widget) if st.session_state.therapy1_duration_widget in duration_range else 0
        therapy1_duration = st.selectbox("Duration of therapy (months)", 
                                         duration_range, 
                                         key="therapy1_duration_widget", 
                                         index=default_duration_index)
        st.session_state.form_data["therapy1_duration"] = st.session_state.therapy1_duration_widget

    # 2nd Line Therapy (if applicable)
    if st.session_state.num_therapies_widget in ["2", "3"]:
        st.subheader("2nd Line Therapy")
        if "therapy2_type_widget" not in st.session_state:
            st.session_state.therapy2_type_widget = st.session_state.form_data.get("therapy2_type", "")
        therapy2_type = st.text_input("Type of therapy", key="therapy2_type_widget")
        st.session_state.form_data["therapy2_type"] = st.session_state.therapy2_type_widget

        if "therapy2_cycles_widget" not in st.session_state:
            st.session_state.therapy2_cycles_widget = st.session_state.form_data.get("therapy2_cycles", 1)
        default_cycle_index = list(range(1, 21)).index(st.session_state.therapy2_cycles_widget) if st.session_state.therapy2_cycles_widget in list(range(1, 21)) else 0
        therapy2_cycles = st.selectbox("Number of cycles", 
                                       list(range(1, 21)), 
                                       key="therapy2_cycles_widget", 
                                       index=default_cycle_index)
        st.session_state.form_data["therapy2_cycles"] = st.session_state.therapy2_cycles_widget

        if "therapy2_outcome_widget" not in st.session_state:
            st.session_state.therapy2_outcome_widget = st.session_state.form_data.get("therapy2_outcome", outcome_options[0])
        default_outcome_index = outcome_options.index(st.session_state.therapy2_outcome_widget) if st.session_state.therapy2_outcome_widget in outcome_options else 0
        therapy2_outcome = st.radio("Outcome", 
                                    outcome_options, 
                                    key="therapy2_outcome_widget", 
                                    index=default_outcome_index)
        st.session_state.form_data["therapy2_outcome"] = st.session_state.therapy2_outcome_widget

        if "therapy2_duration_widget" not in st.session_state:
            st.session_state.therapy2_duration_widget = st.session_state.form_data.get("therapy2_duration", 1)
        default_duration_index = list(range(1, 61)).index(st.session_state.therapy2_duration_widget) if st.session_state.therapy2_duration_widget in list(range(1, 61)) else 0
        therapy2_duration = st.selectbox("Duration of therapy (months)", 
                                         list(range(1, 61)), 
                                         key="therapy2_duration_widget", 
                                         index=default_duration_index)
        st.session_state.form_data["therapy2_duration"] = st.session_state.therapy2_duration_widget

    # 3rd Line Therapy (if applicable)
    if st.session_state.num_therapies_widget == "3":
        st.subheader("3rd Line Therapy")
        if "therapy3_type_widget" not in st.session_state:
            st.session_state.therapy3_type_widget = st.session_state.form_data.get("therapy3_type", "")
        therapy3_type = st.text_input("Type of therapy", key="therapy3_type_widget")
        st.session_state.form_data["therapy3_type"] = st.session_state.therapy3_type_widget

        if "therapy3_cycles_widget" not in st.session_state:
            st.session_state.therapy3_cycles_widget = st.session_state.form_data.get("therapy3_cycles", 1)
        default_cycle_index = list(range(1, 21)).index(st.session_state.therapy3_cycles_widget) if st.session_state.therapy3_cycles_widget in list(range(1, 21)) else 0
        therapy3_cycles = st.selectbox("Number of cycles", 
                                       list(range(1, 21)), 
                                       key="therapy3_cycles_widget", 
                                       index=default_cycle_index)
        st.session_state.form_data["therapy3_cycles"] = st.session_state.therapy3_cycles_widget

        if "therapy3_outcome_widget" not in st.session_state:
            st.session_state.therapy3_outcome_widget = st.session_state.form_data.get("therapy3_outcome", outcome_options[0])
        default_outcome_index = outcome_options.index(st.session_state.therapy3_outcome_widget) if st.session_state.therapy3_outcome_widget in outcome_options else 0
        therapy3_outcome = st.radio("Outcome", 
                                    outcome_options, 
                                    key="therapy3_outcome_widget", 
                                    index=default_outcome_index)
        st.session_state.form_data["therapy3_outcome"] = st.session_state.therapy3_outcome_widget

        if "therapy3_duration_widget" not in st.session_state:
            st.session_state.therapy3_duration_widget = st.session_state.form_data.get("therapy3_duration", 1)
        default_duration_index = list(range(1, 61)).index(st.session_state.therapy3_duration_widget) if st.session_state.therapy3_duration_widget in list(range(1, 61)) else 0
        therapy3_duration = st.selectbox("Duration of therapy (months)", 
                                         list(range(1, 61)), 
                                         key="therapy3_duration_widget", 
                                         index=default_duration_index)
        st.session_state.form_data["therapy3_duration"] = st.session_state.therapy3_duration_widget

    # Previous Stem Cell Transplantation
    prev_transplant_options = ["Autologous", "Allogenic", "No"]
    if "prev_transplant_widget" not in st.session_state:
        st.session_state.prev_transplant_widget = st.session_state.form_data.get("prev_transplant", prev_transplant_options[0])
    default_prev_index = prev_transplant_options.index(st.session_state.prev_transplant_widget) if st.session_state.prev_transplant_widget in prev_transplant_options else 0
    prev_transplant = st.radio("Previous Stem Cell Transplantation? *", 
                               prev_transplant_options, 
                               key="prev_transplant_widget", 
                               index=default_prev_index)
    st.session_state.form_data["prev_transplant"] = st.session_state.prev_transplant_widget

    if st.session_state.prev_transplant_widget == "Autologous":
        if "auto_regimen_widget" not in st.session_state:
            st.session_state.auto_regimen_widget = st.session_state.form_data.get("auto_regimen", "")
        auto_regimen = st.text_input("Autologous Transplant – Conditioning Regimen:", key="auto_regimen_widget")
        st.session_state.form_data["auto_regimen"] = st.session_state.auto_regimen_widget
    elif st.session_state.prev_transplant_widget == "Allogenic":
        if "allo_regimen_widget" not in st.session_state:
            st.session_state.allo_regimen_widget = st.session_state.form_data.get("allo_regimen", "")
        allo_regimen = st.text_input("Allogenic Transplant – Conditioning Regimen:", key="allo_regimen_widget")
        st.session_state.form_data["allo_regimen"] = st.session_state.allo_regimen_widget

        if "allo_bridging_widget" not in st.session_state:
            st.session_state.allo_bridging_widget = st.session_state.form_data.get("allo_bridging", "")
        allo_bridging = st.text_input("Allogenic Transplant – Bridging Therapy:", key="allo_bridging_widget")
        st.session_state.form_data["allo_bridging"] = st.session_state.allo_bridging_widget

    navigate_pages()

# Page 5: Data Privacy Disclaimer & Physician Declaration
elif st.session_state.page == 5:
    st.markdown("## :red[Section E:] Data Privacy Disclaimer")
    st.write("""
    The personal information provided in this form will be processed by Ideogen AG (Switzerland) to supply Belinostat-Pralatrexate per your request, in compliance with EU GDPR, Swiss FADP, and other applicable privacy laws. It may be shared with [Sponsor] to: (1) verify patient eligibility, (2) inform regulatory authorities if required, (3) manage pharmacovigilance and quality reporting. The data will not be retained longer than necessary for these purposes and as required by law. For more information or to exercise data rights, contact Ideogen at [contact].
    """)

    st.markdown("## :blue[Section F:] Physician Declaration")
    st.write("""
    By signing below, I confirm that I am a licensed healthcare provider knowledgeable in PTCL/CTCL treatment, and that I will prescribe Belinostat-Pralatrexate under the MAP in my country. I will take responsibility for patient safety, adhere to all pharmacovigilance reporting requirements (reporting any serious adverse events within 24 hours), and ensure the patient (or caregiver) has been informed and consented to the conditions of this program. I have read and agree to the Data Privacy Disclaimer (Section E). I will comply with all relevant data protection laws, including obtaining the patient’s consent for processing and not sharing any patient identifiable information with the sponsor or Ideogen.
    """)

    # Declaration Checkbox using a dedicated widget key
    if "agree_decl_widget" not in st.session_state:
        st.session_state.agree_decl_widget = st.session_state.form_data.get("agree_decl", False)
    agree_decl = st.checkbox(
        "I, the prescribing physician, have read and agree to the above declarations and terms. *",
        key="agree_decl_widget"
    )
    st.session_state.form_data["agree_decl"] = st.session_state.agree_decl_widget

    # Physician Signature Text Input using a dedicated widget key
    if "phys_signature_widget" not in st.session_state:
        st.session_state.phys_signature_widget = st.session_state.form_data.get("phys_signature", "")
    phys_signature = st.text_input(
        "Physician Signature (Full Name) *",
        key="phys_signature_widget"
    )
    st.session_state.form_data["phys_signature"] = st.session_state.phys_signature_widget

    # Date Input using a dedicated widget key; default to today's date if none stored
    if "sign_date_widget" not in st.session_state:
        st.session_state.sign_date_widget = st.session_state.form_data.get("sign_date", datetime.now())
    sign_date = st.date_input(
        "Date *",
        key="sign_date_widget"
    )
    st.session_state.form_data["sign_date"] = st.session_state.sign_date_widget

    # Submit Form Button with a unique key
    if st.button("Submit Form", key="submit_form"):
        # Define the required fields and their user-friendly labels
        required_fields = {
            "agree_decl": "Declaration Agreement",
            "phys_signature": "Physician Signature (Full Name)",
            "sign_date": "Date"
        }
        missing_fields = [label for key, label in required_fields.items() 
                          if not st.session_state.form_data.get(key)]
        
        if missing_fields:
            st.error("Please fill in the following required fields: " + ", ".join(missing_fields))
        else:
            current_time = datetime.now()
            # Anti-spam: check if a previous submission exists and enforce a threshold (e.g., 10 seconds)
            if "last_submission" in st.session_state:
                threshold = 10  # seconds
                time_diff = (current_time - st.session_state.last_submission).total_seconds()
                if time_diff < threshold:
                    st.error("You are submitting too quickly. Please wait a few seconds before trying again.")
                else:
                    st.session_state.last_submission = current_time
                    try:
                        # Build email content
                        subject = "MAP Form Submission Notification"
                        body = "A new form submission has been received and processed successfully.\n\n" + \
                            "Please review the submission in the admin dashboard.\n\n" + \
                            f"{st.session_state.form_data}"
                        # Use the admin email specified in the .env
                        admin_email = os.getenv("SMTP_RECEIVER", "efe.sahin@ideogen.com")
                        if send_email(subject, body, admin_email):
                            st.info("A notification email has been sent to " + admin_email)
                        else:
                            st.warning("Form submitted, but notification email could not be sent.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            else:
                st.session_state.last_submission = current_time
                try:
                    subject = "MAP Form Submission Notification"
                    body = "A new form submission has been received and processed successfully.\n\n" + \
                        "Please review the submission in the admin dashboard.\n\n" + \
                        f"{st.session_state.form_data}"
                    print(st.session_state.form_data)
                    admin_email = os.getenv("SMTP_RECEIVER", "efe.sahin@ideogen.com")
                    if send_email(subject, body, admin_email):
                        st.info("A notification email has been sent to " + admin_email)
                    else:
                        st.warning("Form submitted, but notification email could not be sent.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    navigate_pages()
