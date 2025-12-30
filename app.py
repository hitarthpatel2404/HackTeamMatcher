import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import plotly.graph_objects as go
import random

#  PAGE CONFIG
st.set_page_config(page_title="HackTeamMatcher Pro", layout="wide", page_icon="⚡")
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css('style.css')

# HEADER & WARNING
st.markdown("""
    <div class="warning-tape">
        <span class="warning-text">⚠️ DATABASE SIMULATION MODE • REAL DATA COMING SOON ⚠️</span>
    </div>
""", unsafe_allow_html=True)

# SESSION STATE
if 'user_avatar' not in st.session_state:
    st.session_state.user_avatar = f"https://api.dicebear.com/7.x/notionists/svg?seed={random.randint(1,1000)}"
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "find_teammate"
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest User"
if 'user_discord' not in st.session_state:
    st.session_state.user_discord = "guest#1234"

# DATA MANAGEMENT
if 'df_live' not in st.session_state:
    try:
        df_init = pd.read_csv('students.csv')
        # placeholder row for the Current User (ID 9999)
        user_row = {
            'Student_ID': 9999,
            'Name': st.session_state.user_name,
            'Discord': st.session_state.user_discord,
            'Avatar': st.session_state.user_avatar,
            'Role': 'Full Stack',
            'Team_Name': np.nan,
            'Is_Recruiting': False,
            'Members_Needed': 0,
            'Looking_For_Role': np.nan,
            'Python': 5, 'Frontend': 5, 'Backend': 5, 'Design': 5, 'SQL': 5,
            'Hours_Available': 20
        }
        df_init = pd.concat([pd.DataFrame([user_row]), df_init], ignore_index=True)
        st.session_state.df_live = df_init
    except FileNotFoundError:
        st.error("Data not found. Run generate_data.py first.")
        st.stop()

df = st.session_state.df_live

# FUNCTIONS: UPDATE / DELETE / DISBAND 
def update_user_stats(py, fe, be, de, sql, hours, name, discord):
    idx = df[df['Student_ID'] == 9999].index
    if not idx.empty:
        df.loc[idx, 'Python'] = py
        df.loc[idx, 'Frontend'] = fe
        df.loc[idx, 'Backend'] = be
        df.loc[idx, 'Design'] = de
        df.loc[idx, 'SQL'] = sql
        df.loc[idx, 'Hours_Available'] = hours
        df.loc[idx, 'Name'] = name
        df.loc[idx, 'Discord'] = discord
        
        skills = {'Python Dev': py, 'Frontend Dev': fe, 'Backend Dev': be, 'Designer': de, 'Data Scientist': sql}
        best_skill = max(skills, key=skills.get)
        role = "Beginner" if skills[best_skill] < 4 else best_skill
        df.loc[idx, 'Role'] = role
        st.session_state.df_live = df 

def delete_user_profile():
    # Removing  the user row completely
    st.session_state.df_live = df[df['Student_ID'] != 9999]
    st.session_state.user_name = "Deleted User"
    st.session_state.user_discord = "---"
    st.rerun()

def disband_team():
    idx = df[df['Student_ID'] == 9999].index
    if not idx.empty:
        df.loc[idx, 'Is_Recruiting'] = False
        df.loc[idx, 'Team_Name'] = np.nan
        df.loc[idx, 'Members_Needed'] = 0
        st.session_state.df_live = df
        st.success("Team Disbanded.")
        st.rerun()

@st.dialog("🚀 Register Your Squad")
def register_team_modal():
    st.write("Fill in the details to list your team on the platform.")
    with st.form("team_reg_form"):
        t_name = st.text_input("Team Name", placeholder="e.g. Velocity Labs")
        t_desc = st.text_area("Project Description", placeholder="We are building an AI that...")
        c1, c2 = st.columns(2)
        t_role = c1.selectbox("Looking for Role", ["Frontend", "Backend", "Data Science", "Designer", "Any"])
        t_count = c2.number_input("Members Needed", 1, 5, 1)
        t_hours = st.slider("Hours/Week Required from Teammate", 5, 40, 10)
        
        if st.form_submit_button("Launch Team"):
            idx = df[df['Student_ID'] == 9999].index
            if not idx.empty:
                df.loc[idx, 'Team_Name'] = t_name
                df.loc[idx, 'Is_Recruiting'] = True
                df.loc[idx, 'Looking_For_Role'] = t_role
                df.loc[idx, 'Members_Needed'] = t_count
                df.loc[idx, 'Hours_Available'] = t_hours 
                st.session_state.df_live = df 
                st.success(f"Team '{t_name}' launched!")
                st.rerun()

# SIDEBAR UI
with st.sidebar:
    st.markdown("### 👤 Your Identity")
    
    # Checking if user exists
    user_exists = not df[df['Student_ID'] == 9999].empty
    
    if user_exists:
        current_role = df.loc[df['Student_ID'] == 9999, 'Role'].values[0]
        has_team = df.loc[df['Student_ID'] == 9999, 'Is_Recruiting'].values[0]
        
        st.markdown(f"""
            <div class="profile-box">
                <img src="{st.session_state.user_avatar}" width="100" style="border-radius:50%; border:4px solid #1e293b; box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);">
                <div style="margin-top:15px; font-size: 1.3rem; font-weight:800; color:white;">{st.session_state.user_name}</div>
                <div style="font-size:0.85rem; color:#94a3b8; margin-top:5px; font-family:monospace; background:rgba(255,255,255,0.05); display:inline-block; padding:2px 8px; border-radius:6px;">{st.session_state.user_discord}</div>
                <div style="margin-top:10px; color:#fbbf24; font-size:0.8rem; font-weight:bold;">{current_role}</div>
            </div>
        """, unsafe_allow_html=True)

        with st.expander("⚙️ Edit Profile & Skills", expanded=False):
            new_name = st.text_input("Display Name", value=st.session_state.user_name)
            new_discord = st.text_input("Discord ID", value=st.session_state.user_discord)
            if new_name != st.session_state.user_name: st.session_state.user_name = new_name
            if new_discord != st.session_state.user_discord: st.session_state.user_discord = new_discord
            
            user_data = df[df['Student_ID'] == 9999].iloc[0]
            my_py = st.slider("Python", 1, 10, int(user_data['Python']))
            my_fe = st.slider("Frontend", 1, 10, int(user_data['Frontend']))
            my_be = st.slider("Backend", 1, 10, int(user_data['Backend']))
            my_de = st.slider("Design", 1, 10, int(user_data['Design']))
            my_sql = st.slider("SQL", 1, 10, int(user_data['SQL']))
            my_hours = st.slider("Hrs/Week Available", 5, 40, int(user_data['Hours_Available']))
            
            update_user_stats(my_py, my_fe, my_be, my_de, my_sql, my_hours, new_name, new_discord)

        st.markdown("---")
        
        # TEAM MANAGEMENT
        st.markdown("### 🛡️ Team Controls")
        if has_team:
             st.info(f"Managing: {df.loc[df['Student_ID'] == 9999, 'Team_Name'].values[0]}")
             if st.button("❌ Disband Team", use_container_width=True, type="primary"):
                 disband_team()
        else:
            if st.button("➕ Register My Team", use_container_width=True):
                register_team_modal()
        
        # DELETE PROFILE
        st.markdown("---")
        if st.button("🗑️ Delete Profile", use_container_width=True):
            delete_user_profile()
            
    else:
        st.error("Profile Deleted.")
        if st.button("♻️ Restore Profile"):
            st.session_state.pop('df_live') # Clear session to force reload
            st.rerun()

# HERO
st.markdown("""
<div class="hero-section">
    <div class="hero-title">
        Build better <br>
        <span class="hero-highlight">teams, faster.</span>
    </div>
    <p class="hero-subtitle">
        Stop randomly DMing people. Use our AI to find the perfect teammate with matching skills and availability in seconds.
    </p>
</div>
""", unsafe_allow_html=True)

# TOGGLES
col_spacer_l, col_center, col_spacer_r = st.columns([1, 2, 1])
with col_center:
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🔍 Find Teammate", use_container_width=True, type="primary" if st.session_state.current_mode == "find_teammate" else "secondary"):
            st.session_state.current_mode = "find_teammate"
            st.rerun()
    with btn_col2:
        if st.button("🤝 Join a Squad", use_container_width=True, type="primary" if st.session_state.current_mode == "join_team" else "secondary"):
            st.session_state.current_mode = "join_team"
            st.rerun()
st.write("") 

# MODE 1: FIND TEAMMATE

if st.session_state.current_mode == "find_teammate":
    
    with st.container():
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: search_query = st.text_input("Search", placeholder="Search by name, skill, or role...", label_visibility="collapsed")
        with c2: role_filter = st.selectbox("Role", ["All Roles", "System Architect", "Product Designer", "Data Strategist", "Full Stack"], label_visibility="collapsed")
        with c3: avail_filter = st.selectbox("Hrs", ["Any", "10+ hrs", "20+ hrs", "30+ hrs"], label_visibility="collapsed")
    st.write("---")

    # LOGIC: Include 9999 (Me) ONLY if filtered by name/self, else exclude for general browsing
    # Actually, we will include everyone but render ID 9999 differently.
    filtered = df.copy()
    
    if avail_filter != "Any": 
        min_hours = int(avail_filter.split('+')[0])
        filtered = filtered[filtered['Hours_Available'] >= min_hours]
    if role_filter != "All Roles":
        filtered = filtered[filtered['Role'].str.contains(role_filter, na=False)]
    if search_query:
        search_term = search_query.lower()
        filtered = filtered[
            filtered['Name'].str.lower().str.contains(search_term, na=False) |
            filtered['Role'].str.lower().str.contains(search_term, na=False) |
            filtered.get('Primary_Interest', pd.Series(['']*len(filtered))).str.lower().str.contains(search_term, na=False)
        ]

    # Get  profile stats for matching distance
    if not df[df['Student_ID'] == 9999].empty:
        user_vals = df[df['Student_ID'] == 9999].iloc[0]
        my_profile = np.array([[user_vals['Python'], user_vals['Frontend'], user_vals['Backend'], user_vals['Design'], user_vals['SQL']]])
    else:
        my_profile = np.array([[5,5,5,5,5]]) # Default if deleted

    if len(filtered) > 0:
        X = filtered[['Python', 'Frontend', 'Backend', 'Design', 'SQL']]
        nn = NearestNeighbors(n_neighbors=min(10, len(filtered))).fit(X)
        dists, indices = nn.kneighbors(my_profile)
        
        for i, idx in enumerate(indices[0]):
            match = filtered.iloc[idx]
            match_score = int((1 - dists[0][i]/15) * 100)
            if match_score < 0: match_score = 0
            
            # CHECK IF THIS IS ME
            is_me = (match['Student_ID'] == 9999)
            card_class = "glass-card is-me-card" if is_me else "glass-card"
            
            with st.container():
                c_pro, c_stat, c_act = st.columns([1.5, 3, 1.5])
                
                with c_pro:
                    # Highlight Badge
                    if is_me: st.markdown("<div style='text-align:center;'><span class='me-badge'>✨ THIS IS YOU</span></div>", unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div style="text-align:center;">
                        <img src="{match['Avatar']}" style="width:70px; height:70px; border-radius:50%; border:2px solid {'#c084fc' if is_me else '#6366f1'};">
                        <h4 style="margin:5px 0 0 0; color:white;">{match['Name']}</h4>
                        <span style="font-size:0.75rem; color:#94a3b8; background:#1e293b; padding:2px 6px; border-radius:4px; border:1px solid #334155;">{match['Role']}</span>
                    </div>
                    """, unsafe_allow_html=True)

                with c_stat:
                    cc1, cc2, cc3 = st.columns(3)
                    cc1.markdown(f"<div style='text-align:center; background:rgba(255,255,255,0.05); padding:5px; border-radius:8px; border:1px solid rgba(255,255,255,0.1); font-size:0.8rem; color:#cbd5e1;'>🔥 {match_score}% Match</div>", unsafe_allow_html=True)
                    cc2.markdown(f"<div style='text-align:center; background:rgba(255,255,255,0.05); padding:5px; border-radius:8px; border:1px solid rgba(255,255,255,0.1); font-size:0.8rem; color:#cbd5e1;'>⏱️ {match['Hours_Available']}h/wk</div>", unsafe_allow_html=True)
                    cc3.markdown(f"<div style='text-align:center; background:rgba(255,255,255,0.05); padding:5px; border-radius:8px; border:1px solid rgba(255,255,255,0.1); font-size:0.8rem; color:#cbd5e1;'>💻 Tech</div>", unsafe_allow_html=True)
                    
                    categories = ['Py', 'Front', 'Back', 'UI', 'SQL']
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(r=[match['Python'], match['Frontend'], match['Backend'], match['Design'], match['SQL']], theta=categories, fill='toself', line_color='#c084fc' if is_me else '#818cf8', opacity=0.6))
                    fig.update_layout(polar=dict(radialaxis=dict(visible=False), angularaxis=dict(color='gray', tickfont=dict(size=9))), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=30, r=30), height=120)
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}, key=f"radar_{idx}")

                with c_act:
                    # If it's me, show "Edit" button instead of Chat
                    if is_me:
                        st.markdown('<div class="action-container" style="align-items:center; justify-content:center;">', unsafe_allow_html=True)
                        st.caption("This is your public profile card.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="action-container">', unsafe_allow_html=True)
                        st.link_button("💬 Chat", "https://discord.com/app", use_container_width=True)
                        st.code(match['Discord'], language=None)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")

# MODE 2: JOIN A TEAM

elif st.session_state.current_mode == "join_team":
    
    # 1. Show MY Team
    my_team = df[(df['Student_ID'] == 9999) & (df['Is_Recruiting'] == True)]
    if not my_team.empty:
        mt = my_team.iloc[0]
        st.markdown(f"""
        <div class="glass-card my-team-card">
            <div style="display:flex; justify-content:space-between; align-items:start;">
                <div>
                    <span class="my-team-badge">✨ YOUR TEAM</span>
                    <h3 style="margin:10px 0 0 0; color:white; text-align:left;">{mt['Team_Name']}</h3>
                    <div style="margin-top:5px; color:#fbbf24; font-size:0.9rem;">
                        Led by <b>You</b>
                    </div>
                </div>
                <div style="text-align:right;">
                    <span style="background:rgba(251, 191, 36, 0.2); color:#fbbf24; padding:4px 8px; border-radius:6px; font-weight:bold; font-size:0.75rem; border:1px solid #fbbf24;">
                        LOOKING FOR: {str(mt['Looking_For_Role']).upper()}
                    </span>
                </div>
            </div>
            <div style="margin-top:15px; display:flex; gap:15px; font-size:0.85rem; color:#cbd5e1; border-top:1px solid rgba(251, 191, 36, 0.3); padding-top:10px;">
                    <span>👥 <b>{mt['Members_Needed']}</b> Slots Open</span>
                    <span>⏱️ <b>{mt['Hours_Available']}</b> Hrs/Week Req.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 2. Show Others
    teams = df[(df['Is_Recruiting'] == True) & (df['Student_ID'] != 9999)].reset_index()
    for i, team in teams.iterrows():
        role_needed = team['Looking_For_Role']
        role_color = "#10b981" 
        if "Backend" in str(role_needed): role_color = "#ef4444" 
        elif "Design" in str(role_needed): role_color = "#f59e0b" 

        with st.container():
            st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid {role_color};">
                <div style="display:flex; justify-content:space-between; align-items:start;">
                    <div>
                        <h3 style="margin:0; color:white; text-align:left;">{team['Team_Name']}</h3>
                        <div style="margin-top:5px; color:#cbd5e1; font-size:0.9rem;">
                            Led by <b>{team['Name']}</b>
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <span style="background:{role_color}20; color:{role_color}; padding:4px 8px; border-radius:6px; font-weight:bold; font-size:0.75rem; border:1px solid {role_color}40;">
                            WANTED: {str(role_needed).upper()}
                        </span>
                    </div>
                </div>
                <div style="margin-top:10px; display:flex; gap:10px; font-size:0.85rem; color:#94a3b8;">
                     <span>👥 {team['Members_Needed']} Spots Open</span> • <span>📅 {team['Hours_Available']}h+ Commitment</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_spacer, col_act_1, col_act_2, col_spacer2 = st.columns([1, 2, 2, 1])
            with col_act_1:
                 st.link_button("👋 Request to Join", "https://discord.com/app", use_container_width=True)
            with col_act_2:
                 st.code(team['Discord'], language=None)
            st.write("")