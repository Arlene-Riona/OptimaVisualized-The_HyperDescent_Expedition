import streamlit as st
import plotly.graph_objects as go
import landscapes
import base64
import json
import numpy as np
import io
from gtts import gTTS
import speech_recognition as sr

def get_base64_image(image_path):
    """Reads a local image file and converts it to a base64 string for CSS insertion."""
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"
    except FileNotFoundError:
        return ""

def generate_voice_transmission(text_content):
    """Converts the AI response text into a high-energy spoken audio byte stream."""
    try:
        # Switching TLD to 'co.uk' gives a crisper, more articulate arcade guide tone
        tts = gTTS(text=text_content, lang='en', tld='co.uk', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except Exception as e:
        print(f"[AUDIO LAYER ERROR]: {str(e)}")
        return None

# --- EMERGENCY FISHING NET BOWL MATH OVERRIDES ---
def local_simple_arcade_data():
    x = np.linspace(-3.0, 3.0, 100)
    y = np.linspace(-3.0, 3.0, 100)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + Y**2
    return X, Y, Z

def local_simple_arcade_fitness(x, y):
    return float(x**2 + y**2)

def local_simple_arcade_gradient(x, y):
    return 2 * x, 2 * y

# System Configuration Layout Initialization
st.set_page_config(layout="wide", page_title="OptimaVisualized", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { 
        background: linear-gradient(135deg, #06020f 0%, #120524 50%, #03010a 100%);
        color: #cbd5e1; 
        font-family: 'Courier New', monospace; 
    }
    .game-title {
        text-align: center; font-size: 4rem; font-weight: 900; letter-spacing: 5px;
        color: #00ffcc !important; text-shadow: 0 0 20px rgba(0, 255, 204, 0.6);
        margin-bottom: 0px; margin-top: 50px;
    }
    .game-subtitle {
        text-align: center; color: #6d5887; letter-spacing: 3px; font-size: 1rem;
        margin-top: 5px; margin-bottom: 60px;
    }
    .center-label {
        text-align: center; font-size: 1.3rem; color: #f8fafc;
        margin-top: 35px; margin-bottom: 15px; font-weight: 600;
    }
    div.stButton { display: flex; justify-content: center; align-items: center; margin-top: 40px; }
    .stButton>button { 
        background: linear-gradient(135deg, #0e051c 0%, #1c0b36 100%); color: #00ffcc; 
        border: 2px solid #00ffcc; padding: 16px 45px; font-size: 1.1rem; font-weight: bold;
        letter-spacing: 2px; border-radius: 4px; transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        background: #00ffcc; color: #06020f; box-shadow: 0 0 25px #00ffcc; border: 2px solid #00ffcc;
    }
    </style>
""", unsafe_allow_html=True)

if "app_screen" not in st.session_state: st.session_state.app_screen = "WELCOME"
if "selected_algo" not in st.session_state: st.session_state.selected_algo = None
if "selected_scenario" not in st.session_state: st.session_state.selected_scenario = None
if "simulation_path" not in st.session_state: st.session_state.simulation_path = None
if "chat_session" not in st.session_state: st.session_state.chat_session = None
if "unlocked_math_symbols" not in st.session_state: st.session_state.unlocked_math_symbols = []
if "hud_stage" not in st.session_state: st.session_state.hud_stage = "STORY_START"  
if "ready_for_plot" not in st.session_state: st.session_state.ready_for_plot = False
if "current_hyperparameters" not in st.session_state: st.session_state.current_hyperparameters = {}

def consult_mission_ai_chat(user_directive, current_algo, current_scenario):
    """Interfaces with Gemini using ultra-simple language, gaming energy, and clear rules."""
    from google import genai
    from google.genai import types

    fallback_response = {
        "radio_transmission": "Wow! Telemetry link updated! Let's get moving, operator!",
        "unlock_symbols": [], "ready_to_simulate": False,
        "learning_rate": 0.05, "momentum_beta": 0.9, "exploration_noise": 0.2
    }

    system_prompt = (
        "You are the high-energy, fun, and extremely enthusiastic Game Guide for an arcade math simulation.\n"
        "Your job is to teach complex computer algorithms to a school student. Use simple words. Never use jargon.\n"
        "Instead of 'flywheel', talk about a heavy bowling ball rolling down a hill. Instead of 'non-convex contours', call it a wavy skateboard park.\n\n"
        f"CURRENT SCENARIO: {current_scenario}\n"
        f"ACTIVE OPTIMIZER SYSTEM: {current_algo}\n\n"
        "YOUR MISSION DESIGN STEPS:\n"
        "1. If the user input is 'INITIALIZE_ENVIRONMENT', give a super fun, 2-sentence intro to this map. "
        "Then, add a short rule: 'Look down below! See those locked math slots on your dashboard? Every time you talk to me or type a physical strategy to solve this map, we unlock a piece of the secret final formula! You can speak into your microphone or type to reply back!' End by asking one simple question about how to roll down the slope.\n"
        "2. When the user replies with an idea (by text or voice), praise them with high energy! Connect their physical idea to one symbol and unlock it. Then state what simple goal is left.\n"
        "3. Once they handle the basic concepts, unlock everything and say: 'Woohoo! System synchronized! The final master formula is complete! Click that huge ENGAGE LIVE PLOT button below to see your line roll down live!' Set ready_to_simulate to true.\n\n"
        "MATH UNMASKING DESIGNATIONS:\n"
        "- For Momentum: ['w_t', 'grad_w', 'v_t', 'beta']\n"
        "- For Adam: ['m_t', 'v_t', 'm_hat', 'v_hat']\n"
        "- For Grey Wolf: ['alpha_pos', 'A', 'D', 'a_factor']\n\n"
        "STRICT COMPLIANCE STRUCTURE: You must output your reply ONLY as a valid JSON object matching this schema layout:\n"
        "{\n"
        '  "radio_transmission": "Your fun, high-energy, simple text narrative here.",\n'
        '  "unlock_symbols": ["symbol_id_1"],\n'
        '  "ready_to_simulate": boolean,\n'
        '  "learning_rate": float,\n'
        '  "momentum_beta": float,\n'
        '  "exploration_noise": float\n'
        "}"
    )

    try:
        if "GOOGLE_API_KEY" in st.secrets:
            api_key_val = st.secrets["GOOGLE_API_KEY"]
        else:
            return fallback_response
            
        if "ai_client" not in st.session_state or st.session_state.ai_client is None:
            st.session_state.ai_client = genai.Client(api_key=api_key_val)
            
        if st.session_state.chat_session is None:
            st.session_state.chat_session = st.session_state.ai_client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json"
                )
            )
        
        message_to_send = user_directive if user_directive.strip() else "INITIALIZE_ENVIRONMENT"
        response = st.session_state.chat_session.send_message(message_to_send)
        parsed_output = json.loads(response.text)
        return parsed_output
        
    except Exception as e:
        print(f"[DEBUG LOG AI EXCEPTION]: {str(e)}")
        return fallback_response

# SCREEN 1: THE INITIALIZATION DECK (WELCOME SCREEN)
if st.session_state.app_screen == "WELCOME":
    st.markdown("<h1 class='game-title'>OPTIMA_VISUALIZED</h1>", unsafe_allow_html=True)
    st.markdown("<p class='game-subtitle'>INTERACTIVE 3D LOSS LANDSCAPE EXPEDITION ENGINE</p>", unsafe_allow_html=True)
    
    _, center_col, _ = st.columns([1, 1.6, 1])
    with center_col:
        st.markdown("<p class='center-label'>⚡ Select the optimization algorithm to explore</p>", unsafe_allow_html=True)
        algo_choice = st.selectbox(
            "LABEL_HIDDEN_ALGO",
            ["Gradient Descent with Momentum (Vector Acceleration)", "Adam (Adaptive Step Size Estimation)", "Adaptive Grey Wolf Optimizer (Cooperative Swarm)"],
            label_visibility="collapsed", key="welcome_algo_select"
        )
        st.markdown("<p class='center-label'>🗺️ Select an expedition scenario</p>", unsafe_allow_html=True)
        scenario_choice = st.selectbox(
            "LABEL_HIDDEN_SCENARIO",
            ["1. Deep Ocean Trench Escape (The Rosenbrock Chasm)", "2. Cyberpunk Signal Jam (The Adaptive Matrix)", "3. Sonoran Desert Swarm Rescue (The Rastrigin Dunes)"],
            label_visibility="collapsed", key="welcome_scenario_select"
        )
        st.write("\n")
        dev_mode = st.checkbox("🛠️ Activate Sandbox Debug Mode (Disables Gemini API)", key="welcome_dev_checkbox")
            
        if st.button("INITIALIZE MISSION DESCENT", key="welcome_init_btn"):
            st.session_state.selected_algo = algo_choice
            st.session_state.selected_scenario = scenario_choice
            st.session_state.simulation_path = None  
            st.session_state.app_screen = "HUD"
            st.session_state.hud_stage = "STORY_START"
            st.session_state.unlocked_math_symbols = []
            st.session_state.chat_session = None
            st.session_state.ready_for_plot = False
            st.session_state.dev_mode_active = dev_mode 
            if "mission_override_log" in st.session_state: del st.session_state.mission_override_log
            if "active_voice_broadcast" in st.session_state: del st.session_state.active_voice_broadcast
            st.rerun()

# SCREEN 2: THE FULL-SCREEN TACTICAL HUD
elif st.session_state.app_screen == "HUD":
    hud_cols = st.columns([3, 1])
    with hud_cols[0]:
        short_algo = st.session_state.selected_algo.split('(')[0].strip()
        short_scenario = st.session_state.selected_scenario.split('(')[0].strip()
        st.markdown(f"### 🛰️ OPTIMA_VISUALIZED // {short_algo.upper()} // {short_scenario.upper()}")
    with hud_cols[1]:
        st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
        if st.button("← Go Back", key="hud_goback_btn"):
            st.session_state.app_screen = "WELCOME"
            st.session_state.simulation_path = None  
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
            
    st.write("---")
    scenario = st.session_state.selected_scenario
    
    if "Ocean" in scenario:
        X, Y, Z = landscapes.get_trench_escape_data()
        terrain_colorscale = [[0, '#010b1a'], [0.4, '#0a2c5c'], [0.8, '#1e71cc'], [1, '#ffffff']]
        radar_line_color = "#00ffff"
        bg_image_url = get_base64_image("assets/ocean.jpg")
        f_eval = landscapes.rosenbrock_fitness if hasattr(landscapes, 'rosenbrock_fitness') else lambda x, y: (1-x)**2 + 100*(y-x**2)**2
    elif "Cyberpunk" in scenario:
        X, Y, Z = landscapes.get_cyberpunk_matrix_data()
        terrain_colorscale = [[0, '#05010a'], [0.3, '#32045c'], [0.7, '#88069e'], [1, '#ff007f']]
        radar_line_color = "#ff007f"
        bg_image_url = get_base64_image("assets/cyberCity.jpg")
        f_eval = landscapes.ackley_fitness if hasattr(landscapes, 'ackley_fitness') else lambda x, y: -20*np.exp(-0.2*np.sqrt(0.5*(x**2+y**2)))
    else:
        X, Y, Z = local_simple_arcade_data()
        terrain_colorscale = [[0, '#1a0600'], [0.4, '#5c1903'], [0.8, '#c74416'], [1, '#ffa473']]
        radar_line_color = "#ff4500"
        bg_image_url = get_base64_image("assets/desert.jpg")
        f_eval = local_simple_arcade_fitness

    st.markdown(f"""
        <style>
        [data-testid="stPlotlyChart"] {{
            background-image: linear-gradient(to bottom, rgba(6, 2, 15, 0.3), rgba(6, 2, 15, 0.6)), url('{bg_image_url}');
            background-size: cover; background-position: center; background-repeat: no-repeat;
            border-radius: 12px; padding: 15px; border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .js-plotly-plot .plotly .main-svg {{ background: transparent !important; }}
        </style>
    """, unsafe_allow_html=True)

    fig = go.Figure(data=[go.Surface(
        z=Z, x=X, y=Y, colorscale=terrain_colorscale, showscale=False, opacity=0.8,
        contours_z=dict(show=True, usecolormap=False, highlightcolor=radar_line_color, project_z=True, color=radar_line_color)
    )])

    # --- PLOTLY TRAJECTORY ENGINE ---
    if st.session_state.simulation_path is not None:
        path_data = st.session_state.simulation_path
        unlocked_symbols = st.session_state.unlocked_math_symbols
        annotations_3d = []
        frames = []
        slider_steps = []
        
        if len(path_data.shape) == 2:  
            z_vals = [f_eval(p[0], p[1]) for p in path_data]
            algo_color = '#00ffcc' if "Momentum" in st.session_state.selected_algo else '#ff007f'
            
            fig.add_trace(go.Scatter3d(
                x=[path_data[0, 0]], y=[path_data[0, 1]], z=[z_vals[0]],
                mode='lines+markers',
                marker=dict(size=6, color=[z_vals[0]], colorscale='Jet', showscale=False),
                line=dict(color=[z_vals[0]], colorscale='Jet', width=9),
                name='Active Trajectory'
            ))
            fig.add_trace(go.Scatter3d(
                x=[path_data[0, 0]], y=[path_data[0, 1]], z=[0],
                mode='lines', line=dict(color='rgba(255,255,255,0.3)', width=3, dash='dash'),
                name='Shadow Projection', showlegend=False
            ))
            
            target_trace_index = len(fig.data) - 2 
            shadow_trace_index = len(fig.data) - 1 
            
            for idx in range(1, len(path_data) + 1):
                sub_path = path_data[:idx]
                sub_z = [f_eval(p[0], p[1]) for p in sub_path]
                frame_name = f'step_{idx}'
                
                frames.append(go.Frame(
                    data=[
                        go.Scatter3d(x=sub_path[:, 0], y=sub_path[:, 1], z=sub_z, mode='lines+markers', marker=dict(size=6, color=sub_z, colorscale='Jet'), line=dict(color=sub_z, colorscale='Jet', width=9)),
                        go.Scatter3d(x=sub_path[:, 0], y=sub_path[:, 1], z=[0]*len(sub_path), mode='lines', line=dict(color='rgba(255,255,255,0.3)', width=3, dash='dash'))
                    ],
                    name=frame_name, traces=[target_trace_index, shadow_trace_index]
                ))
                slider_steps.append(dict(args=[[frame_name], dict(mode="immediate", transition=dict(duration=0), frame=dict(duration=0, redraw=False))], label=str(idx), method="animate"))
                
            annotations_3d.append(dict(
                showarrow=True, arrowhead=2, x=path_data[0,0], y=path_data[0,1], z=f_eval(path_data[0,0], path_data[0,1]),
                text="<b>START POSITION (w₀)</b>", font=dict(color="#00ffcc", size=14), bgcolor="rgba(14, 5, 28, 0.95)", bordercolor="#00ffcc", borderwidth=2, borderpad=6
            ))
            
        elif len(path_data.shape) == 3:  
            fig.add_trace(go.Scatter3d(x=path_data[0, :, 0], y=path_data[0, :, 1], z=[f_eval(w[0], w[1]) for w in path_data[0]], mode='markers', marker=dict(size=7, color='#ffaa00', symbol='x'), name='AGWO Swarm'))
            target_trace_index = len(fig.data) - 1
            
            for idx in range(len(path_data)):
                swarm_pos = path_data[idx]
                frame_name = f'step_{idx}'
                frames.append(go.Frame(data=[go.Scatter3d(x=swarm_pos[:, 0], y=swarm_pos[:, 1], z=[f_eval(w[0], w[1]) for w in swarm_pos], mode='markers', marker=dict(size=7, color='#ffaa00', symbol='x'))], name=frame_name, traces=[target_trace_index]))
                slider_steps.append(dict(args=[[frame_name], dict(mode="immediate", transition=dict(duration=0), frame=dict(duration=0, redraw=False))], label=str(idx + 1), method="animate"))

            annotations_3d.append(dict(
                showarrow=True, arrowhead=2, x=path_data[0,0,0], y=path_data[0,0,1], z=f_eval(path_data[0,0,0], path_data[0,0,1]),
                text="<b>INITIAL SEARCH SWARM (X⃗)</b>", font=dict(color="#ffaa00", size=14), bgcolor="rgba(14, 5, 28, 0.95)", bordercolor="#ffaa00", borderwidth=2, borderpad=6
            ))

        fig.frames = frames
        fig.update_layout(
            scene_annotations=annotations_3d,
            updatemenus=[dict(
                type="buttons", direction="left", x=0.05, y=-0.05, xanchor="right", yanchor="top", pad=dict(t=15, r=10), showactive=False,
                buttons=[
                    dict(label="▶ PLAY DESCENT", method="animate", args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True, mode="immediate", transition=dict(duration=150))]),
                    dict(label="⏸ PAUSE", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=True), mode="immediate", transition=dict(duration=0))])
                ]
            )],
            sliders=[dict(active=0, currentvalue=dict(prefix="Mission Iteration Sequence: ", font=dict(color="#00ffcc", size=14)), pad=dict(t=15), x=0.08, y=-0.05, len=0.92, steps=slider_steps)]
        )
    else:
        fig.add_trace(go.Scatter3d(x=[None], y=[None], z=[None], mode='markers', showlegend=False))

    if st.session_state.simulation_path is not None:
        p_data = st.session_state.simulation_path
        x_coords = p_data[:, 0] if len(p_data.shape) == 2 else p_data[:, :, 0].flatten()
        y_coords = p_data[:, 1] if len(p_data.shape) == 2 else p_data[:, :, 1].flatten()
        x_range = [float(np.min(x_coords) - 0.6), float(np.max(x_coords) + 0.6)]
        y_range = [float(np.min(y_coords) - 0.6), float(np.max(y_coords) + 0.6)]
    else:
        x_range = [-2.0, 2.0] if "Ocean" in scenario else [-4.5, 4.5]
        y_range = [-1.0, 3.0] if "Ocean" in scenario else [-4.5, 4.5]

    if "Ocean" in scenario: z_range, camera_eye = [0, 400], dict(x=1.5, y=-1.5, z=0.8)
    elif "Cyberpunk" in scenario: z_range, camera_eye = [0, 25], dict(x=1.4, y=1.4, z=0.9)
    else: z_range, camera_eye = [0, 40], dict(x=1.3, y=-1.3, z=1.0)

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=x_range, backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)", title="X Axis"),
            yaxis=dict(range=y_range, backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)", title="Y Axis"),
            zaxis=dict(range=z_range, backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(255,255,255,0.1)", title="Loss"),
            camera=dict(eye=camera_eye, center=dict(x=0, y=0, z=-0.1))
        ),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, b=40, t=0), height=650, uirevision='constant_view_angle'
    )

    st.plotly_chart(fig, width="stretch", key="tactical_loss_landscape_canvas")
    st.write("---")
    
    # 4. Workspace Panels
    log_col, control_col = st.columns([1.2, 1])
    with log_col:
        st.markdown("#### 💬 Mission Guidance AI")
        
        if "active_voice_broadcast" not in st.session_state: st.session_state.active_voice_broadcast = None
        if "dev_mode_active" not in st.session_state: st.session_state.dev_mode_active = False

        if "mission_override_log" not in st.session_state:
            if st.session_state.dev_mode_active:
                st.session_state.mission_override_log = "🛠️ **SANDBOX DEBUG MODE ACTIVE.** AI text streams offline."
                st.session_state.unlocked_math_symbols = []
                st.session_state.ready_for_plot = False
                st.session_state.current_hyperparameters = {"lr": 0.01, "beta": 0.9, "noise": 0.2}
            else:
                with st.spinner("Establishing secure neural link..."):
                    ai_payload = consult_mission_ai_chat("INITIALIZE_ENVIRONMENT", st.session_state.selected_algo, st.session_state.selected_scenario)
                    st.session_state.mission_override_log = ai_payload["radio_transmission"]
                    st.session_state.unlocked_math_symbols = ai_payload.get("unlock_symbols", [])
                    st.session_state.ready_for_plot = ai_payload.get("ready_to_simulate", False)
                    st.session_state.current_hyperparameters = {
                        "lr": ai_payload.get("learning_rate", 0.01), "beta": ai_payload.get("momentum_beta", 0.9), "noise": ai_payload.get("exploration_noise", 0.2)
                    }
                    audio_stream = generate_voice_transmission(st.session_state.mission_override_log)
                    st.session_state.active_voice_broadcast = audio_stream.read() if audio_stream else None
            st.rerun()

        # AUDIO AUTOPLAY TRICK: HTML audio element with autoplay attribute forces instantaneous playback
        if st.session_state.active_voice_broadcast:
            b64_audio = base64.b64encode(st.session_state.active_voice_broadcast).decode()
            audio_html = f"""
                <audio autoplay class="stAudio">
                <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
            # Fallback standard control widget
            st.audio(st.session_state.active_voice_broadcast, format="audio/mp3")
        else:
            st.caption("🔊 Audio deck offline.")
            
        st.info(st.session_state.mission_override_log)
        st.write("---")
        
        # --- THE MATH UNMASKING CANVAS ---
        st.markdown("#### 📐 Recovered Telemetry Formulas")
        unlocked = st.session_state.unlocked_math_symbols
        metric_cols = st.columns(4)
        
        if "Momentum" in st.session_state.selected_algo:
            with metric_cols[0]: st.metric("Position Vector", "$w_t$" if "w_t" in unlocked else "🔒 LOCKED")
            with metric_cols[1]: st.metric("Gradient", r"$\nabla f(w_t)$" if "grad_w" in unlocked else "🔒 LOCKED")
            with metric_cols[2]: st.metric("Velocity Force", "$v_t$" if "v_t" in unlocked else "🔒 LOCKED")
            with metric_cols[3]: st.metric("Friction Lag", r"$\beta$" if "beta" in unlocked else "🔒 LOCKED")
            if all(sym in unlocked for sym in ["w_t", "grad_w", "v_t", "beta"]):
                st.success("🎯 **MATH SYNCHRONIZED**")
                st.markdown("### $$v_t = \\beta v_{t-1} + \\eta \\nabla f(w_t)$$")
                st.markdown("### $$w_{t+1} = w_t - v_t$$")
                
        elif "Adam" in st.session_state.selected_algo:
            with metric_cols[0]: st.metric("1st Moment (Mean)", "$m_t$" if "m_t" in unlocked else "🔒 LOCKED")
            with metric_cols[1]: st.metric("2nd Moment (Variance)", "$v_t$" if "v_t" in unlocked else "🔒 LOCKED")
            with metric_cols[2]: st.metric("Bias Corr Mean", r"$\hat{m}_t$" if "m_hat" in unlocked else "🔒 LOCKED")
            with metric_cols[3]: st.metric("Bias Corr Var", r"$\hat{v}_t$" if "v_hat" in unlocked else "🔒 LOCKED")
            if all(sym in unlocked for sym in ["m_t", "v_t", "m_hat", "v_hat"]):
                st.success("🎯 **MATH SYNCHRONIZED**")
                st.markdown("### $$w_{t+1} = w_t - \\frac{\\eta}{\\sqrt{\\hat{v}_t} + \\epsilon} \\hat{m}_t$$")
                
        elif "Grey Wolf" in st.session_state.selected_algo:
            with metric_cols[0]: st.metric("Alpha Leader Vector", r"$\vec{X}_\alpha$" if "alpha_pos" in unlocked else "🔒 LOCKED")
            with metric_cols[1]: st.metric("Encircle Step", r"$\vec{A}$" if "A" in unlocked else "🔒 LOCKED")
            with metric_cols[2]: st.metric("Distance Variance", r"$\vec{D}$" if "D" in unlocked else "🔒 LOCKED")
            with metric_cols[3]: st.metric("Convergence Factor", "$a$" if "a_factor" in unlocked else "🔒 LOCKED")
            if all(sym in unlocked for sym in ["alpha_pos", "A", "D", "a_factor"]):
                st.success("🎯 **MATH SYNCHRONIZED**")
                st.markdown("### $$\\vec{D} = |\\vec{C} \\cdot \\vec{X}_{\\text{leader}} - \\vec{X}|$$")
                st.markdown("### $$\\vec{X}_{(t+1)} = \\frac{\\vec{X}_1 + \\vec{X}_2 + \\vec{X}_3}{3}$$")

    with control_col:
        st.markdown("🛠️ **DEVELOPER CONTROLS**")
        dbg_cols = st.columns(3)
        with dbg_cols[0]:
            if st.button("🔓 Cheat: Unlock 2", key="dbg_unlock_half"):
                st.session_state.unlocked_math_symbols = ["w_t", "grad_w", "m_t", "v_t", "alpha_pos", "A"]
                st.rerun()
        with dbg_cols[1]:
            if st.button("🎯 Cheat: Unlock All", key="dbg_unlock_all"):
                st.session_state.unlocked_math_symbols = ["w_t", "grad_w", "v_t", "beta", "m_t", "v_t", "m_hat", "v_hat", "alpha_pos", "A", "D", "a_factor"]
                st.session_state.ready_for_plot = True
                st.session_state.hud_stage = "SIMULATION_ACTIVE" 
                st.session_state.current_hyperparameters = {"lr": 0.05, "beta": 0.9, "noise": 0.2}
                st.rerun()
        with dbg_cols[2]:
            if st.button("🧹 Clear State", key="dbg_clear"):
                st.session_state.unlocked_math_symbols, st.session_state.ready_for_plot = [], False
                st.session_state.hud_stage = "STORY_START"
                st.session_state.simulation_path = None
                if "active_voice_broadcast" in st.session_state: del st.session_state.active_voice_broadcast
                st.rerun()
                
        st.write("---") 
        st.markdown("#### 🛰️ Command Terminal")
        
        if st.session_state.hud_stage == "STORY_START":
            st.markdown("💡 *Communicate with your Guide. Record your voice or type your entry below.*")
            
            # 🎙️ AUDIO RECORDING AND TRANSCRIPTION LAYER
            st.caption("🎙️ Live Microphone Input Link Array:")
            mic_audio_packet = st.audio_input("Record Oral Strategy Packet Override", key="hud_voice_recorder")
            
            transcribed_text = ""
            if mic_audio_packet is not None:
                st.success("🔊 Voice packet compiled into buffer. Translating signal...")
                try:
                    recognizer = sr.Recognizer()
                    # Convert Streamlit's audio file object into a form the speech_recognition engine reads
                    audio_file = sr.AudioFile(mic_audio_packet)
                    with audio_file as source:
                        audio_data = recognizer.record(source)
                    # Run clean, free local transcription matrix
                    transcribed_text = recognizer.recognize_google(audio_data)
                    st.info(f"🎤 **TRANSCRIBED AUDIO MESSAGE:** '{transcribed_text}'")
                except Exception as e:
                    st.error("Could not parse audio frequencies. Try typing in the field below!")

            user_input = st.text_input(
                "Transmit strategy text payload:", 
                value=transcribed_text if transcribed_text else "",
                placeholder="Type your strategic ideas or concept questions here...",
                key="terminal_text_input"
            )
            
            st.write("\n")
            
            if st.button("🚀 TRANSMIT COMMUNICATIONS SIGNAL", key="submit_directive_btn"):
                # System execution gate now successfully checks both text and vocal transcript channels!
                final_transmission = user_input if user_input.strip() else transcribed_text
                if not final_transmission.strip():
                    st.warning("Please type a message or speak into your microphone before hitting transmit.")
                else:
                    with st.spinner("Decoding telemetry payload..."):
                        ai_payload = consult_mission_ai_chat(final_transmission, st.session_state.selected_algo, st.session_state.selected_scenario)
                        st.session_state.mission_override_log = ai_payload["radio_transmission"]
                        new_symbols = ai_payload.get("unlock_symbols", [])
                        st.session_state.unlocked_math_symbols = list(set(st.session_state.unlocked_math_symbols + new_symbols))
                        st.session_state.ready_for_plot = ai_payload.get("ready_to_simulate", False)
                        st.session_state.current_hyperparameters = {
                            "lr": ai_payload.get("learning_rate", 0.01), "beta": ai_payload.get("momentum_beta", 0.9), "noise": ai_payload.get("exploration_noise", 0.2)
                        }
                        audio_stream = generate_voice_transmission(st.session_state.mission_override_log)
                        st.session_state.active_voice_broadcast = audio_stream.read() if audio_stream else None
                        st.rerun()
            
            if st.session_state.ready_for_plot:
                st.success("🎯 **PROPULSION MATRICES ALIGNED**")
                if st.button("🔥 UNLOCK & ENGAGE LIVESTREAM TRAJECTORY SIMULATION", key="transition_stage_btn"):
                    st.session_state.hud_stage = "SIMULATION_ACTIVE"
                    st.rerun()

        elif st.session_state.hud_stage == "SIMULATION_ACTIVE":
            st.success("🛰️ **PROPULSION STAGE RUNNING**")
            
            if st.session_state.simulation_path is None:
                import optimizers
                params = st.session_state.current_hyperparameters
                
                if "Ocean" in scenario:
                    start_x, start_y = 1.2, 1.8 
                    raw_grad = landscapes.rosenbrock_gradient if hasattr(landscapes, 'rosenbrock_gradient') else lambda x, y: (2*(x-1) - 400*x*(y-x**2), 200*(y-x**2))
                    grad_func = lambda x, y: tuple(np.clip(raw_grad(x, y), -8.0, 8.0))
                elif "Cyberpunk" in scenario:
                    start_x, start_y = 2.5, 2.5 
                    raw_grad = landscapes.ackley_gradient if hasattr(landscapes, 'ackley_gradient') else lambda x, y: (x*0.1, y*0.1)
                    grad_func = lambda x, y: tuple(np.clip(raw_grad(x, y), -8.0, 8.0))
                else:
                    start_x, start_y = 2.5, 2.5 
                    grad_func = local_simple_arcade_gradient

                if "Momentum" in st.session_state.selected_algo:
                    st.session_state.simulation_path = optimizers.simulate_momentum(start_x, start_y, grad_func, steps=40, lr=0.0005 if "Ocean" in scenario else params.get("lr", 0.01), beta=params.get("beta", 0.9))
                elif "Adam" in st.session_state.selected_algo:
                    st.session_state.simulation_path = optimizers.simulate_adam(start_x, start_y, grad_func, steps=40, lr=0.001 if "Ocean" in scenario else params.get("lr", 0.02), beta1=params.get("beta", 0.9))
                elif "Grey Wolf" in st.session_state.selected_algo:
                    st.session_state.simulation_path = np.array(optimizers.simulate_agwo(start_x, start_y, f_eval, steps=35, num_wolves=10))
                st.rerun()

            live_tweak = st.text_input("Send mid-flight steering optimization directive:", placeholder="e.g., Stabilize velocity vectors...", key="hud_live_tweak_input")
            if st.button("⚡ TRANSMIT STEERING OVERRIDE", key="live_tweak_btn"):
                with st.spinner("Processing adjustments..."):
                    ai_payload = consult_mission_ai_chat(f"MID_FLIGHT_ADJUSTMENT: {live_tweak}", st.session_state.selected_algo, st.session_state.selected_scenario)
                    st.session_state.mission_override_log = ai_payload["radio_transmission"]
                    st.session_state.current_hyperparameters = {
                        "lr": ai_payload.get("learning_rate", 0.01), "beta": ai_payload.get("momentum_beta", 0.9), "noise": ai_payload.get("exploration_noise", 0.2)
                    }
                    st.session_state.simulation_path = None
                    st.rerun()
                
            st.write("---")
            if st.button("🔄 Reset Mission Scenario & Clear Memory", key="reset_mission_btn"):
                st.session_state.hud_stage = "STORY_START"
                st.session_state.unlocked_math_symbols = []
                st.session_state.chat_session, st.session_state.ai_client = None, None 
                st.session_state.ready_for_plot = False
                if "mission_override_log" in st.session_state: del st.session_state.mission_override_log
                if "simulation_path" in st.session_state: st.session_state.simulation_path = None
                if "active_voice_broadcast" in st.session_state: del st.session_state.active_voice_broadcast
                st.rerun()