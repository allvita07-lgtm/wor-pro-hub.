import streamlit as st
import random
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURAÇÃO NEON-GAMER ---
st.set_page_config(page_title="WOR NEO-TACTICAL GOD MODE", layout="wide", page_icon="🧿")

st.markdown("""
    <style>
    .main { background: #00050a; color: #00f2ff; font-family: 'Segoe UI', sans-serif; }
    .stApp { background: radial-gradient(circle at top, #001d3d 0%, #00050a 100%); }
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(0, 242, 255, 0.05); border-bottom: 2px solid #00f2ff; }
    .stTabs [data-baseweb="tab"] { color: #00f2ff66; padding: 20px; font-weight: bold; }
    .stTabs [aria-selected="true"] { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; }
    .metric-card { background: rgba(0, 242, 255, 0.05); border: 1px solid #00f2ff; border-radius: 10px; padding: 20px; text-align: center; box-shadow: 0 0 15px #00f2ff22; }
    .ai-terminal { border-left: 4px solid #ff0055; background: rgba(255, 0, 85, 0.05); padding: 15px; font-family: 'Consolas', monospace; color: #ff0055; }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE TOTAL (LENDAS, ÉPICOS E ARTEFATOS) ---
DB = {
    "HEROES": {
        "Marksman": ["Silas", "Hatssut", "Setram", "Aracha", "Idril", "Calypso", "Nyx", "Razaak", "Maul", "Luneria", "Alaura", "Sargak", "Jeera", "Brunor", "Theil"],
        "Mages": ["Khamet", "Vierna", "Boreas", "Ajax", "Morrigan", "Laseer", "Twinfiend", "Solcadens", "Eona", "Greed", "Raiden", "Marri", "Anai", "Zelus"],
        "Fighters": ["Zilitu", "Valderon", "Lust", "Arrogance", "Salazar", "Valerya", "Volka", "Wrath", "Deimos", "Abomination", "Komodo", "Estrid"],
        "Tanks": ["Brokkir", "Torodor", "King Harz", "Regulus", "Olague", "Baron", "Isolde", "Azhor", "Ghan", "Titus"],
        "Healers": ["Elowyn", "Hollow", "Laya", "Sadie", "Vortex", "Midan", "Nisson", "Ezryn", "Ferssi"]
    },
    "ARTIFACTS": {
        "DPS": ["Spirit Projection", "Tear of Twilight", "The Watcher", "Ichor Chalice"],
        "Support": ["Lulu's Necklace", "Golden Scarab", "Euphoria"],
        "Tank": ["Bastion Ring", "The King's Guard", "Soul Siphon"]
    }
}

# --- MOTOR DE INTELIGÊNCIA ---
if 'my_team' not in st.session_state: st.session_state.my_team = []

def get_victory_chance(team, stage):
    # Lógica de simulação de probabilidade
    base = len(team) * 5
    if "Dolores" in team or "Dolores (Buffer)" in team: base += 20
    if "Silas" in team and "Vierna" in team: base += 15
    penalty = (stage - 15) * 4 if stage > 15 else 0
    return max(5, min(99, base - penalty))

# --- UI PRINCIPAL ---
st.title("🧿 NEO-TACTICAL COMMAND CENTER")

# TERMINAL IA NO TOPO
st.markdown(f"""<div class='ai-terminal'> > [SISTEMA]: {'Analise de Esquadrão Ativa. Pronto para simulação.' if st.session_state.my_team else 'Aguardando recrutamento de unidades...'}</div>""", unsafe_allow_html=True)

tabs = st.tabs(["🛸 HANGAR", "⚔️ MISSÕES & RAIDS", "💎 ARTEFATOS & GEAR", "📊 SIMULADOR"])

# --- ABA 1: HANGAR (GERENCIAMENTO) ---
with tabs[0]:
    st.subheader("📡 REGISTRO DE UNIDADES")
    col1, col2 = st.columns([2,1])
    with col1:
        all_h = sorted([name for cat in DB["HEROES"].values() for name in cat])
        selected = st.multiselect("Selecione os Heróis da sua Conta:", all_h)
        if st.button("SINCRONIZAR DATABASE"):
            st.session_state.my_team = selected
            st.success("Database Sincronizada com sucesso!")
    
    with col2:
        st.markdown(f"<div class='metric-card'><h3>UNIDADES ATIVAS</h3><h2>{len(st.session_state.my_team)}</h2></div>", unsafe_allow_html=True)

# --- ABA 2: MISSÕES E RAIDS ---
with tabs[1]:
    st.subheader("🎯 OPERAÇÕES DE CAMPO")
    mode = st.radio("Selecione o Conteúdo:", ["Gear Raid 1", "Gear Raid 2", "Gear Raid 3", "Guild Boss NM4", "Void Rift Nightmare"], horizontal=True)
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown(f"""
        <div class='hero-card'>
        <h3>TUTORIAL DE ELITE: {mode}</h3>
        <b>Objetivo Primário:</b> Maximizar o DPS durante a janela de buff.<br>
        <b>Dica Tática:</b> Use o Ultimate da Hollow logo após a Dolores para manter o ciclo de Rage infinito.<br>
        <b>Missão de Campanha:</b> Se estiver travado, suba seus heróis de 5⭐ para 6⭐. É o maior boost de status.
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.info("💡 **METODO PRO:** Em missões primárias, foque em fechar os 'Feitos de Campanha' para ganhar Cristais Sagrados rápidos.")

# --- ABA 3: ARTEFATOS E GEAR ---
with tabs[2]:
    st.subheader("🛠️ FORJA NEURAL")
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.write("**MELHORES ARTEFATOS:**")
        for cat, arts in DB["ARTIFACTS"].items():
            st.write(f"🔹 *{cat}:* {', '.join(arts)}")
    with col_g2:
        st.write("**PRIORIDADE DE EQUIPAMENTO:**")
        st.code("DPS: ATK% > CRIT RATE > CRIT DMG > SPEED\nTANK: HP% > DEF% > RESISTÊNCIA\nHEALER: SPEED > HP% > RECARGA")

# --- ABA 4: SIMULADOR DE COMBATE ---
with tabs[3]:
    st.subheader("📈 SIMULADOR DE PROBABILIDADE")
    target_st = st.slider("Selecione o Estágio da Gear Raid:", 1, 21, 19)
    
    chance = get_victory_chance(st.session_state.my_team, target_st)
    
    # Gráfico de Radar ou Gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = chance,
        title = {'text': f"Chance de Vitória (Stage {target_st})"},
        gauge = {
            'axis': {'range': [0, 100], 'tickcolor': "#00f2ff"},
            'bar': {'color': "#00f2ff"},
            'steps': [
                {'range': [0, 40], 'color': "#ff0055"},
                {'range': [40, 70], 'color': "#ffaa00"},
                {'range': [70, 100], 'color': "#238636"}
            ],
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "#00f2ff"})
    st.plotly_chart(fig)
    
    if chance < 50:
        st.error("⚠️ SISTEMA: Probabilidade crítica. Considere recrutar heróis chaves como Dolores ou Silas.")
    else:
        st.success("✅ SISTEMA: Parâmetros aceitáveis para tentativa de invasão.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🌑 PROTOCOLO DE IA")
st.sidebar.write("Estado: **DOMINAÇÃO TOTAL**")
st.sidebar.caption("Neo-Tactical v9.0 Final Edition")
