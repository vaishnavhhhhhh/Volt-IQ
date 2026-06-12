import streamlit as st
import math
from groq import Groq
from fpdf import FPDF
API_KEY = st.secrets["GROQ_API_KEY"]
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
st.set_page_config(  
    page_title="Volt-IQ",
    layout="wide"
)
st.markdown("""
<style>

h1, h2 {
    color: #00E5FF !important;
}
h3{
       color: white; 
            
}
.stButton > button {
    width: 250%;
    height: 120px;
    border-radius: 100px;
    background: #1E3A5F;
    color: white;
    border: none;
    font-size: 20px;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}
.stButton > button:hover {
    background: #2A4D75;
    transform: translateY(-5px);
    transition: all 0.3s ease;
}

[data-testid="stMetric"] {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #00E5FF;
}
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-30px);
    }

    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

.hero-title {
    animation: fadeIn 1.2s ease-in-out;
}
/* Back button only */
button[kind="secondary"] {
    width: 100px !important;
    height: 50px !important;
    min-height: 50px !important;
    border-radius: 50% !important;
    font-size: 22px !important;
}
/* Feature cards */
button[kind="primary"] {
    width: 100%;
    height: 120px;
    border-radius: 18px;
}
button[kind="tertiary"] {
    width: 180px !important;
    height: 45px !important;
    color: white !important;
    border-radius: 12px !important;
    font-size: 1px !important;
    
    border: none !important;
}

button[kind="tertiary"]:hover {
    box-shadow: 0 0 15px #00E5FF !important;
    transform: translateY(-2px);
}
.stDownloadButton > button {
    width: auto !important;
    min-width: 180px !important;
    height: 45px !important;
    background-color: #444444 !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
}
.stDownloadButton > button:hover {
    background-color: #5a5a5a !important;
}
/* Upload button only */
[data-testid="stFileUploader"] button {
    min-width: 180px !important;
    height: 45px !important;
    padding: 0 20px !important;

   
    color: white !important;

    border: none !important;
    border-radius: 10px !important;

    font-size: 16px !important;
    font-weight: bold !important;

    white-space: nowrap !important;
}


[data-testid="stFileUploader"] button:hover {
    box-shadow: 0 0 10px #00E5FF !important;
}
.center-btn {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)
import requests
import base64

client = Groq(api_key=API_KEY)

def get_ai_response(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"
from fpdf import FPDF

def create_pdf(content):

    content = str(content)

    content = content.replace("Ω", "Ohm")
    content = content.replace("η", "eta")
    content = content.replace("√", "sqrt")
    content = content.replace("°", "deg")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in content.split("\n"):

        # Convert unsupported Unicode characters
        line = line.encode("latin-1", "replace").decode("latin-1")

        # Skip completely empty lines
        if not line.strip():
            pdf.ln(5)
            continue

        pdf.multi_cell(190, 8, line)

    return pdf.output(dest="S").encode("latin-1")
# PASTE THE NEW FUNCTION HERE
def analyze_circuit_image(image_file):

    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen/qwen2.5-vl-72b-instruct",
        "messages": [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Analyze this circuit. Identify components, explain working, applications and viva questions."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image_base64}"
                    }
                }
            ]
        }]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload
    )

    return response.json()["choices"][0]["message"]["content"]

st.sidebar.title("Volt-IQ")
st.sidebar.markdown("---")

st.sidebar.markdown("### MODULES")

if st.sidebar.button(" AI Chat Assistant" , type = "tertiary"):
    st.session_state.page = "AI Chat"
    st.rerun()

if st.sidebar.button(" Lab Assistant",type = "tertiary"):
    st.session_state.page = "Lab Assistant"
    st.rerun()

if st.sidebar.button(" Viva Generator",type = "tertiary"):
    st.session_state.page = "Viva Generator"
    st.rerun()

if st.sidebar.button(" Notes Generator",type = "tertiary"):
    st.session_state.page = "Notes Generator"
    st.rerun()

if st.sidebar.button(" EEE Calculator",type = "tertiary"):
    st.session_state.page = "EEE Calculator"
    st.rerun()

if st.sidebar.button(" Circuit Analyzer",type = "tertiary"):
    st.session_state.page = "Circuit Analysis"
    st.rerun()
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if st.session_state.page == "Home":

    st.markdown("""
<h1 class="hero-title"    style="
    text-align: center;
    font-size: 90px;
    font-weight: 900;
    color: #00E5FF;
    letter-spacing: 4px;
    margin-bottom: 0px;
    text-shadow: 0px 0px 15px rgba(0,229,255,0.7);
">
 Volt-IQ
</h1>

<h4 style="
    text-align: center;
    color: #b0b0b0;
    margin-top: 15px;
">
AI-Powered Electrical & Electronics Engineering Companion
</h4>
""", unsafe_allow_html=True)

    st.subheader("FEATURES")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🤖\n\nAI Chat Assistant", key="chat",type="primary"):
            st.session_state.page = "AI Chat"
            st.rerun()

    with col2:
        if st.button("🧪\n\nLab Assistantance", key="lab",type="primary"):
            st.session_state.page = "Lab Assistant"
            st.rerun()

    with col3:
        if st.button("🎤\n\nViva Generator", key="viva",type="primary"):
            st.session_state.page = "Viva Generator"
            st.rerun()

    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button("📝\n\nNotes Generator", key="notes",type="primary"):
            st.session_state.page = "Notes Generator"
            st.rerun()

    with col5:
        if st.button("🧮\nEEE Calculator", key="calc",type="primary"):
            st.session_state.page = "EEE Calculator"
            st.rerun()

    with col6:
        if st.button("🔌\n\nCircuit Analyzer", key="circuit",type="primary"):
            st.session_state.page = "Circuit Analysis"
            st.rerun()
                    
            

  
elif st.session_state.page == "AI Chat":

    back_btn = st.button("HOME", key="back_home", type="secondary")

    if back_btn:
        st.session_state.page = "Home"
        st.rerun()

   
    chat_col, history_col = st.columns([5,1.3])
    with history_col:

        st.markdown(
            """
            <style>
            div[data-testid="column"] {
                padding-top: 0rem;
            }

            /* Reduce spacing above widgets inside column */
            div[data-testid="stVerticalBlock"] {
                gap: 0.3rem;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<h3 style='margin-bottom:5px;'>History</h3>",
            unsafe_allow_html=True
        )

        if st.button(" Clear History", type="tertiary"):
            st.session_state.search_history = []
            st.rerun()

        searches = "\n".join(
            [f"• {item['question']}" for item in reversed(st.session_state.search_history)]
        )

        searches_html = "<br>".join(
            [f"• {item['question']}" for item in reversed(st.session_state.search_history)]
        )

        st.markdown(
            f"""
            <div style="
                height: 500px;
                overflow-y: auto;
                padding: 12px;
                background-color: #111;
                border: 1px solid #00E5FF;
                border-radius: 10px;
                color: #b0b0b0;
                font-size: 14px;
                line-height: 1.6;
            ">
                {searches_html}
            </div>
            """,
            unsafe_allow_html=True
        )
    with chat_col:
        st.header("🤖 AI Chat")

        user_question = st.text_area("Ask a question")
        col1, col2, col3 = st.columns([2, 1, 2])

        with col2:
            ask_ai = st.button(
                "Ask AI",
                key="ask_ai",
                type="tertiary",
                
            )

    if ask_ai:

        with st.spinner("Generating response..."):

          prompt = f"""
          You are an expert Electrical and Electronics Engineering assistant.

          Answer the following question clearly and accurately:

          {user_question}
          """

          result = get_ai_response(prompt)
          st.session_state.search_history.insert(
            0,
            {
                "question": user_question,
                "answer": result
            }
        )
        st.write(result)
        pdf_file = create_pdf(result)
        st.download_button(
            "Download PDF",
            data=pdf_file,
            file_name="chat_response.pdf",
            mime="application/pdf",
            key="download_pdf"
        )
       
        
elif st.session_state.page == "Lab Assistant":
    if st.button("HOME", key="back_home"):
        st.session_state.page = "Home"
        st.rerun()
    st.header("Lab Assistant")

    subject = st.selectbox(
        "Select Subject",
        [
            "Electrical Machines",
            "Power Electronics",
            "Circuits",
            "Analog Electronics"
        ]
    )

    experiment = st.text_input("Enter Experiment Name")
    col1, col2, col3 = st.columns([2, 1, 2])

    with col2:
      generate_lab = st.button(
        "Generate Lab Guide",
         key="generate_lab",
         type="tertiary"
      )
    if generate_lab:
        prompt = f"""
        Subject: {subject}

        Experiment: {experiment}

        Generate:

        1. Aim
        2. Apparatus
        3. Theory
        4. Procedure
        5. Observation Table
        6. Calculations
        7. Result
        8. Viva Questions
        9. Precautions
        """
        

        with st.spinner("Generating response..."):
            result = get_ai_response(prompt)
        st.write(result)

        pdf_file = create_pdf(result)

        st.download_button(
            "Download Lab Guide PDF",
            data=pdf_file,
            file_name="lab_guide.pdf",
            mime="application/pdf"
        )
elif st.session_state.page == "Viva Generator":
    if st.button("HOME", key="back_home"):
        st.session_state.page = "Home"
        st.rerun()
    st.header("Viva Generator")

    topic = st.text_input("Enter Topic")

    difficulty = st.selectbox(
        "Select Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    num_questions = st.slider(
        "Number of Questions",
        5,
        20,
        10
    )
     
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
      Generate_viva = st.button(
        "Generate Viva",
        key="Generate_viva",
        type="tertiary"
      )

    if Generate_viva:
        prompt = f"""
        Generate {num_questions} viva questions and answers on {topic}.

        Difficulty: {difficulty}

        Format:
        Q1:
        Ans:
        """

        with st.spinner("Generating response..."):
          result = get_ai_response(prompt)
        st.write(result)
        pdf_file = create_pdf(result)

        st.download_button(
          "Download Viva PDF",
           data=pdf_file,
           file_name="viva_questions.pdf",
          mime="application/pdf"
        )
elif st.session_state.page == "Notes Generator":
    if st.button("HOME", key="back_home"):
        st.session_state.page = "Home"
        st.rerun()
    st.header("Notes Generator")

    topic = st.text_input("Enter Topic")

    note_type = st.selectbox(
        "Select Notes Type",
        [
            "Short Notes",
            "Exam Notes",
            "Detailed Notes"
        ]
    )
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
      Generate_Notes = st.button(
        "Generate Notes",
        key="Generate_Notes",
        type="tertiary"
      )

    if Generate_Notes:
        prompt = f"""
        Generate {note_type} for:

        {topic}

        Include:
        Definition
        Working
        Advantages
        Disadvantages
        Applications
        """
        with st.spinner("Generating notes..."):
          result = get_ai_response(prompt)
        st.write(result)

        pdf_file = create_pdf(result)

        st.download_button(
          "Download Notes PDF",
            data=pdf_file,
           file_name="notes.pdf",
           mime="application/pdf"
        )
elif st.session_state.page == "EEE Calculator":
    if st.button("HOME", key="back_home"):
        st.session_state.page = "Home"
        st.rerun()
    st.header("Smart EEE Calculator")
    formula = st.selectbox(
        "Select Formula",
        [
            "Ohm's Law",
            "Power Formula",
            "Three Phase Power",
            "Transformer Efficiency",
            "Synchronous Speed",
            "Voltage Regulation",
            "Transformer EMF Equation",
            "Induction Motor Slip",
            "Power Factor Correction",
            "Capacitive Reactance",
            "Inductive Reactance",
            "Resonant Frequency"
        ]
    )

    # ---------------- OHM'S LAW ----------------

    if formula == "Ohm's Law":

        st.subheader("V = I × R")

        find = st.selectbox(
            "Find",
            ["Voltage", "Current", "Resistance"]
        )

        if find == "Voltage":

            current = st.number_input("Current (A)", min_value=0.0)
            resistance = st.number_input("Resistance (Ω)", min_value=0.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):
                voltage = current * resistance
                st.success(f"Voltage = {voltage:.2f} V")

        elif find == "Current":

            voltage = st.number_input("Voltage (V)", min_value=0.0)
            resistance = st.number_input("Resistance (Ω)", min_value=0.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):

                if resistance != 0:
                    current = voltage / resistance
                    st.success(f"Current = {current:.2f} A")
                else:
                    st.error("Resistance cannot be zero")

        elif find == "Resistance":

            voltage = st.number_input("Voltage (V)", min_value=0.0)
            current = st.number_input("Current (A)", min_value=0.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):

                if current != 0:
                    resistance = voltage / current
                    st.success(f"Resistance = {resistance:.2f} Ω")
                else:
                    st.error("Current cannot be zero")

    # ---------------- POWER FORMULA ----------------

    elif formula == "Power Formula":

        st.subheader("P = V × I")

        find = st.selectbox(
            "Find",
            ["Power", "Voltage", "Current"]
        )

        if find == "Power":

            voltage = st.number_input("Voltage (V)", min_value=0.0)
            current = st.number_input("Current (A)", min_value=0.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):
                power = voltage * current
                st.success(f"Power = {power:.2f} W")

        elif find == "Voltage":

            power = st.number_input("Power (W)", min_value=0.0)
            current = st.number_input("Current (A)", min_value=0.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):

                if current != 0:
                    voltage = power / current
                    st.success(f"Voltage = {voltage:.2f} V")
                else:
                    st.error("Current cannot be zero")

        elif find == "Current":

            power = st.number_input("Power (W)", min_value=0.0)
            voltage = st.number_input("Voltage (V)", min_value=0.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):

                if voltage != 0:
                    current = power / voltage
                    st.success(f"Current = {current:.2f} A")
                else:
                    st.error("Voltage cannot be zero")

    # ---------------- THREE PHASE POWER ----------------

    elif formula == "Three Phase Power":

        st.subheader("P = √3 × V × I × PF")

        find = st.selectbox(
            "Find",
            ["Power", "Voltage", "Current", "Power Factor"]
        )

        root3 = 1.732

        if find == "Power":

            voltage = st.number_input("Voltage (V)", min_value=0.0)
            current = st.number_input("Current (A)", min_value=0.0)
            pf = st.number_input("Power Factor", min_value=0.0, max_value=1.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):
                power = root3 * voltage * current * pf
                st.success(f"Power = {power:.2f} W")

        elif find == "Voltage":

            power = st.number_input("Power (W)", min_value=0.0)
            current = st.number_input("Current (A)", min_value=0.0)
            pf = st.number_input("Power Factor", min_value=0.0, max_value=1.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):

                if current * pf != 0:
                    voltage = power / (root3 * current * pf)
                    st.success(f"Voltage = {voltage:.2f} V")
                else:
                    st.error("Current and PF cannot be zero")

        elif find == "Current":

            power = st.number_input("Power (W)", min_value=0.0)
            voltage = st.number_input("Voltage (V)", min_value=0.0)
            pf = st.number_input("Power Factor", min_value=0.0, max_value=1.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):

                if voltage * pf != 0:
                    current = power / (root3 * voltage * pf)
                    st.success(f"Current = {current:.2f} A")
                else:
                    st.error("Voltage and PF cannot be zero")

        elif find == "Power Factor":

            power = st.number_input("Power (W)", min_value=0.0)
            voltage = st.number_input("Voltage (V)", min_value=0.0)
            current = st.number_input("Current (A)", min_value=0.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):

                if voltage * current != 0:
                    pf = power / (root3 * voltage * current)
                    st.success(f"Power Factor = {pf:.2f}")
                else:
                    st.error("Voltage and Current cannot be zero")

    # ---------------- TRANSFORMER EFFICIENCY ----------------

    elif formula == "Transformer Efficiency":

        st.subheader("η = (Output Power / Input Power) × 100")

        find = st.selectbox(
            "Find",
            ["Efficiency", "Output Power", "Input Power"]
        )

        if find == "Efficiency":

            output_power = st.number_input("Output Power (W)", min_value=0.0)
            input_power = st.number_input("Input Power (W)", min_value=0.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):

                if input_power != 0:
                    efficiency = (output_power / input_power) * 100
                    st.success(f"Efficiency = {efficiency:.2f}%")
                else:
                    st.error("Input Power cannot be zero")

        elif find == "Output Power":

            efficiency = st.number_input("Efficiency (%)", min_value=0.0)
            input_power = st.number_input("Input Power (W)", min_value=0.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):

                output_power = (efficiency / 100) * input_power
                st.success(f"Output Power = {output_power:.2f} W")

        elif find == "Input Power":

            efficiency = st.number_input("Efficiency (%)", min_value=0.1)
            output_power = st.number_input("Output Power (W)", min_value=0.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):

                input_power = output_power / (efficiency / 100)
                st.success(f"Input Power = {input_power:.2f} W")

    # ---------------- SYNCHRONOUS SPEED ----------------

    elif formula == "Synchronous Speed":

        st.subheader("Ns = (120 × f) / P")

        find = st.selectbox(
            "Find",
            ["Speed", "Frequency", "Poles"]
        )

        if find == "Speed":

            frequency = st.number_input("Frequency (Hz)", min_value=0.0)
            poles = st.number_input("Number of Poles", min_value=1)

            if st.button("Calculate",key="ask_ai", type="tertiary"):
                speed = (120 * frequency) / poles
                st.success(f"Synchronous Speed = {speed:.2f} RPM")

        elif find == "Frequency":

            speed = st.number_input("Speed (RPM)", min_value=0.0)
            poles = st.number_input("Number of Poles", min_value=1)

            if st.button("Calculate",key="ask_ai", type="tertiary"):
                frequency = (speed * poles) / 120
                st.success(f"Frequency = {frequency:.2f} Hz")

        elif find == "Poles":

            speed = st.number_input("Speed (RPM)", min_value=0.1)
            frequency = st.number_input("Frequency (Hz)", min_value=0.0)

            if st.button("Calculate",key="ask_ai", type="tertiary"):
                poles = (120 * frequency) / speed
                st.success(f"Number of Poles = {poles:.2f}")
    elif formula == "Voltage Regulation":
        st.subheader("VR = ((VNL - VFL) / VFL) × 100")
        find = st.selectbox(
        "Find",
        ["Voltage Regulation", "No Load Voltage", "Full Load Voltage"]
        )

        if find == "Voltage Regulation":

            vnl = st.number_input("No Load Voltage (V)")
            vfl = st.number_input("Full Load Voltage (V)")

            if st.button("Calculate", key="vr1"):

                vr = ((vnl - vfl) / vfl) * 100
                st.success(f"Voltage Regulation = {vr:.2f}%")

        elif find == "No Load Voltage":

            vr = st.number_input("Voltage Regulation (%)")
            vfl = st.number_input("Full Load Voltage (V)")

            if st.button("Calculate", key="vr2"):

                vnl = vfl * (1 + vr/100)
                st.success(f"No Load Voltage = {vnl:.2f} V")

        elif find == "Full Load Voltage":

            vr = st.number_input("Voltage Regulation (%)")
            vnl = st.number_input("No Load Voltage (V)")

            if st.button("Calculate", key="vr3"):
                vfl = vnl / (1 + vr/100)
                st.success(f"Full Load Voltage = {vfl:.2f} V")   
    elif formula == "Transformer EMF Equation":
        st.subheader("E = 4.44 × f × N × Φ")
        find = st.selectbox(
            "Find",
            ["EMF", "Frequency", "Turns", "Flux"]
        )

        if find == "EMF":

            f = st.number_input("Frequency")
            N = st.number_input("Turns")
            phi = st.number_input("Flux")

            if st.button("Calculate", key="emf1"):

                E = 4.44*f*N*phi
                st.success(f"EMF = {E:.2f} V")

        elif find == "Frequency":

            E = st.number_input("EMF")
            N = st.number_input("Turns")
            phi = st.number_input("Flux")

            if st.button("Calculate", key="emf2"):

                f = E/(4.44*N*phi)
                st.success(f"Frequency = {f:.2f} Hz")

        elif find == "Turns":

            E = st.number_input("EMF")
            f = st.number_input("Frequency")
            phi = st.number_input("Flux")

            if st.button("Calculate", key="emf3"):

                N = E/(4.44*f*phi)
                st.success(f"Turns = {N:.2f}")

        elif find == "Flux":

            E = st.number_input("EMF")
            f = st.number_input("Frequency")
            N = st.number_input("Turns")

            if st.button("Calculate", key="emf4"):

                phi = E/(4.44*f*N)
                st.success(f"Flux = {phi:.6f} Wb")
    elif formula == "Induction Motor Slip":
        st.subheader("S = ((Ns - Nr) / Ns) × 100")
        find = st.selectbox(
            "Find",
            ["Slip", "Synchronous Speed", "Rotor Speed"]
        )

        if find == "Slip":

            Ns = st.number_input("Synchronous Speed")
            Nr = st.number_input("Rotor Speed")

            if st.button("Calculate", key="slip1"):

                slip = ((Ns-Nr)/Ns)*100
                st.success(f"Slip = {slip:.2f}%")

        elif find == "Synchronous Speed":

            slip = st.number_input("Slip (%)")
            Nr = st.number_input("Rotor Speed")

            if st.button("Calculate", key="slip2"):

                Ns = Nr/(1-slip/100)
                st.success(f"Synchronous Speed = {Ns:.2f} RPM")

        elif find == "Rotor Speed":

            slip = st.number_input("Slip (%)")
            Ns = st.number_input("Synchronous Speed")

            if st.button("Calculate", key="slip3"):

                Nr = Ns*(1-slip/100)
                st.success(f"Rotor Speed = {Nr:.2f} RPM")
    elif formula == "Capacitive Reactance":
        st.subheader("Xc = 1 / (2πfC)")
        find = st.selectbox(
            "Find",
            ["Reactance", "Frequency", "Capacitance"]
        )

        if find == "Reactance":

            f = st.number_input("Frequency")
            C = st.number_input("Capacitance")

            if st.button("Calculate", key="xc1"):

                Xc = 1/(2*math.pi*f*C)
                st.success(f"Xc = {Xc:.2f} Ω")

        elif find == "Frequency":

            Xc = st.number_input("Reactance")
            C = st.number_input("Capacitance")

            if st.button("Calculate", key="xc2"):

                f = 1/(2*math.pi*Xc*C)
                st.success(f"Frequency = {f:.2f} Hz")

        elif find == "Capacitance":

            Xc = st.number_input("Reactance")
            f = st.number_input("Frequency")

            if st.button("Calculate", key="xc3"):

                C = 1/(2*math.pi*f*Xc)
                st.success(f"Capacitance = {C:.8f} F")
    elif formula == "Inductive Reactance":
        st.subheader("XL = 2πfL")
        find = st.selectbox(
            "Find",
            ["Reactance", "Frequency", "Inductance"]
        )

        if find == "Reactance":

            f = st.number_input("Frequency")
            L = st.number_input("Inductance")

            if st.button("Calculate", key="xl1"):

                Xl = 2*math.pi*f*L
                st.success(f"Xl = {Xl:.2f} Ω")

        elif find == "Frequency":

            Xl = st.number_input("Reactance")
            L = st.number_input("Inductance")

            if st.button("Calculate", key="xl2"):

                f = Xl/(2*math.pi*L)
                st.success(f"Frequency = {f:.2f} Hz")

        elif find == "Inductance":

            Xl = st.number_input("Reactance")
            f = st.number_input("Frequency")

            if st.button("Calculate", key="xl3"):

                L = Xl/(2*math.pi*f)
                st.success(f"Inductance = {L:.6f} H")
    elif formula == "Resonant Frequency":
        st.subheader("fr = 1 / (2π√LC)")
        find = st.selectbox(
            "Find",
            ["Frequency", "Inductance", "Capacitance"]
        )

        if find == "Frequency":

            L = st.number_input("Inductance")
            C = st.number_input("Capacitance")

            if st.button("Calculate", key="rf1"):

                fr = 1/(2*math.pi*math.sqrt(L*C))
                st.success(f"Frequency = {fr:.2f} Hz")

        elif find == "Inductance":

            fr = st.number_input("Frequency")
            C = st.number_input("Capacitance")

            if st.button("Calculate", key="rf2"):

                L = 1/((2*math.pi*fr)**2*C)
                st.success(f"Inductance = {L:.6f} H")

        elif find == "Capacitance":

            fr = st.number_input("Frequency")
            L = st.number_input("Inductance")

            if st.button("Calculate", key="rf3"):

                C = 1/((2*math.pi*fr)**2*L)
                st.success(f"Capacitance = {C:.8f} F")
    elif formula == "Power Factor Correction":
        st.subheader("Q = P × (tanφ₁ − tanφ₂)")
        find = st.selectbox(
            "Find",
            [
                "Capacitor Rating (kVAR)",
                "Active Power (kW)"
            ]
        )

        if find == "Capacitor Rating (kVAR)":

            P = st.number_input("Active Power (kW)", min_value=0.0)
            pf1 = st.number_input("Initial Power Factor", min_value=0.01, max_value=1.0)
            pf2 = st.number_input("Desired Power Factor", min_value=0.01, max_value=1.0)

            if st.button("Calculate", key="pfc1"):

                phi1 = math.acos(pf1)
                phi2 = math.acos(pf2)

                Q = P * (math.tan(phi1) - math.tan(phi2))

                st.success(f"Required Capacitor Rating = {Q:.2f} kVAR")

        elif find == "Active Power (kW)":

            Q = st.number_input("Capacitor Rating (kVAR)", min_value=0.0)
            pf1 = st.number_input("Initial Power Factor", min_value=0.01, max_value=1.0)
            pf2 = st.number_input("Desired Power Factor", min_value=0.01, max_value=1.0)

            if st.button("Calculate", key="pfc2"):

                phi1 = math.acos(pf1)
                phi2 = math.acos(pf2)

                denominator = math.tan(phi1) - math.tan(phi2)

                if denominator != 0:
                    P = Q / denominator
                    st.success(f"Active Power = {P:.2f} kW")
                else:
                    st.error("Invalid Power Factor values")
elif st.session_state.page == "Circuit Analysis":
    if st.button("HOME", key="back_home"):
        st.session_state.page = "Home"
        st.rerun()
    st.header("Circuit Analyzer")

    st.subheader("Upload Circuit Image")

    uploaded_file = st.file_uploader(
      "",
      type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        st.image(
            uploaded_file,
            caption="Uploaded Circuit",
            use_container_width=True
        )
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            Analyze_circuit = st.button(
                "Analyze Circuit",
                key="Generate_viva",
                type="tertiary"
            )
        if Analyze_circuit:

             with st.spinner("Analyzing circuit..."):

                try:
                    result = analyze_circuit_image(uploaded_file)
                    st.write(result)

                except Exception as e:
                    st.error(f"Error: {e}")
