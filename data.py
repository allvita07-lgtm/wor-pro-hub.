# data.py
import streamlit as st
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DE INTERFACE ---
st.set_page_config(page_title="WoR Pro Hub", layout="wide", page_icon="⚔️")

# Estilo CSS Profissional (Dark Mode & Cards)
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #161b22; border-radius: 5px; color: white; }
    .stTabs [aria-selected="true"] { background-color: #238636; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #58a6ff; }
    </style>
""", unsafe_allow_html=True)

# --- 1. BANCO DE DADOS (DATABASE) ---
# Aqui incluímos as categorias para facilitar a busca de todos os personagens
HERO_DB = {
    "Marksmen": ["Silas", "Hatssut", "Setram", "Aracha", "Idril", "Calypso", "Nyx", "Razaak", "Maul", "Theil", "Brienne"],
    "Mages": ["Khamet", "Vierna", "Boreas", "Ajax", "Morrigan", "Laseer", "Abomination", "Arve", "Eona", "Greed"],
    "Fighters": ["Zilitu", "Valderon", "Lust", "Arrogance", "Salazar", "Wrath", "Valerya", "Volka", "Deimos", "Komodo"],
    "Tanks": ["Olague", "Brokkir", "Torodor", "Regulus", "Baron", "King Harz", "Isolde"],
    "Healers": ["Elowyn", "Hollow", "Laya", "Sadie", "Vortex", "Midan", "Nisson"]
}

GR_REQUIREMENTS = {
    "GR1 (Mages/AoE)": {"Key": ["Khamet", "Vierna", "Boreas", "Eona"], "Strategy": "Necessário Anti-cura e Dano Mágico massivo em área. O boss regenera vida. Use Dolores no centro."},
    "GR2 (Defense)": {"Key": ["Volka", "Olague", "Sadie", "Baron"], "Strategy": "Estratégia de Recuo (Volka A1). Coloque tanques para absorver o impacto e retire antes da morte."},
    "GR3 (Piercers)": {"Key": ["Silas", "Idril", "Hatssut", "Aracha"], "Strategy": "Foco em alcance. Idril (A5) limpa as laterais enquanto Silas foca no Boss central."}
}

# --- 2. ESTADO DO APP (SESSION STATE) ---
if 'my_team' not in st.session_state:
    st.session_state.my_team = []

# --- 3. INTERFACE PRINCIPAL ---
st.title("⚔️ WoR Pro Hub: Strategy & Builds")

tab1, tab2, tab3 = st.tabs(["📊 My Team & Analysis", "📖 GR Strategy Wiki", "🔍 Hero Encyclopedia"])

# --- ABA 1: MEU TIME E ANÁLISE ---
with tab1:
    st.header("Seu Esquadrão")
    
    # Adicionar Heróis ao Time
    all_names = [name for sublist in HERO_DB.values() for name in sublist]
    col_add1, col_add2 = st.columns([2, 1])
    with col_add1:
        new_hero = st.selectbox("Adicionar Herói ao seu Time:", all_names)
    with col_add2:
        if st.button("➕ Adicionar à Conta"):
            if new_hero not in st.session_state.my_team:
                st.session_state.my_team.append(new_hero)
    
    st.write(f"**Heróis na sua conta:** {', '.join(st.session_state.my_team) if st.session_state.my_team else 'Nenhum'}")
    
    if st.button("🗑️ Resetar Time"):
        st.session_state.my_team = []
        st.rerun()

    st.markdown("---")
    st.subheader("🧐 Possibilidade de Progressão (Análise de Stage)")
    
    target_gr = st.selectbox("Qual Raid você quer testar?", list(GR_REQUIREMENTS.keys()))
    reqs = GR_REQUIREMENTS[target_gr]
    
    # Lógica de Verificação
    matches = [h for h in st.session_state.my_team if h in reqs["Key"]]
    score = len(matches) / len(reqs["Key"])
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("Índice de Preparação", f"{int(score*100)}%")
        if score > 0.5:
            st.success("✅ Você tem os heróis base para o Stage 21!")
        else:
            st.warning("⚠️ Faltam peças-chave para o Stage 21.")
            
    with col_res2:
        st.write("**Peças que você já tem:**")
        for m in matches: st.write(f"✔️ {m}")

# --- ABA 2: WIKI DE ESTRATÉGIAS ---
with tab2:
    st.header("Manual de Gear Raids (Stage 19-21)")
    for gr, data in GR_REQUIREMENTS.items():
        with st.expander(f"📌 {gr} - Guia Técnico"):
            st.write(f"**Estratégia:** {data['Strategy']}")
            st.write("**Heróis Recomendados (MVP):**")
            st.code(", ".join(data["Key"]))
            
    st.info("💡 Lembre-se: Dolores e Hollow são suportes universais obrigatórios para quase todos os Stages 21.")

# --- ABA 3: ENCICLOPÉDIA ---
with tab3:
    st.header("Biblioteca de Personagens")
    for cat, members in HERO_DB.items():
        with st.expander(f"{cat} ({len(members)})"):
            cols = st.columns(3)
            for i, m in enumerate(members):
                cols[i % 3].write(f"• {m}")

# --- RODAPÉ ---
st.sidebar.markdown("---")
st.sidebar.write("🟢 **Status da Conta:** " + ("Endgame" if len(st.session_state.my_team) > 10 else "Midgame"))
st.sidebar.caption("WoR Pro Hub v4.0 | Desenvolvido para Elite Players")
