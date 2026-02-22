# data.py
import streamlit as st
import pandas as pd
from data import HEROES, STRATEGIES  # Importa os dados do outro ficheiro

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="WoR Pro Hub", layout="wide", page_icon="⚔️")

# Estilo para parecer um App Nativo
st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #238636; color: white; }
    .stExpander { background-color: #161b22; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# --- ESTADO DA SESSÃO (MEU TIME) ---
if 'my_team' not in st.session_state:
    st.session_state.my_team = []

# --- SIDEBAR (NAVEGAÇÃO) ---
st.sidebar.title("🎮 WoR Control Center")
page = st.sidebar.radio("Navegar para:", ["🛡️ Meu Time", "📖 Guia Gear Raids", "📑 Lista de Heróis"])

# --- PÁGINA 1: MEU TIME E POSSIBILIDADES ---
if page == "🛡️ Meu Time":
    st.title("🛡️ Gestão de Esquadrão")
    
    # Interface para adicionar heróis
    all_heroes = sorted([h for sublist in HEROES.values() for h in sublist])
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_hero = st.selectbox("Escolha um herói da lista:", all_heroes)
    with col2:
        if st.button("Adicionar"):
            if selected_hero not in st.session_state.my_team:
                st.session_state.my_team.append(selected_hero)
                st.rerun()

    # Exibição do Time Atual
    st.subheader("Seu Time Atual")
    if st.session_state.my_team:
        cols = st.columns(3)
        for i, h in enumerate(st.session_state.my_team):
            cols[i % 3].info(f"👤 {h}")
        if st.button("🗑️ Limpar Tudo", type="secondary"):
            st.session_state.my_team = []
            st.rerun()
    else:
        st.write("Nenhum herói adicionado ainda.")

    st.markdown("---")
    
    # ANÁLISE DE POSSIBILIDADE
    st.subheader("🔍 Analisador de Progressão")
    raid_choice = st.selectbox("Em qual Raid você quer testar seu time?", ["GR1", "GR2", "GR3"])
    
    # MVPs fictícios para o cálculo (ajustável no data.py no futuro)
    mvps = {
        "GR1": ["Khamet", "Vierna", "Boreas", "Eona", "Greed", "Dolores"],
        "GR2": ["Olague", "Baron", "Sadie", "Volka", "Vortex"],
        "GR3": ["Silas", "Idril", "Hatssut", "Aracha", "Maul", "Razaak"]
    }
    
    my_mvps = [h for h in st.session_state.my_team if h in mvps[raid_choice]]
    progresso = len(my_mvps) / 4 # Baseado em ter pelo menos 4 chaves
    
    if progresso >= 1.0:
        st.success(f"🔥 **Possibilidade Alta!** Você tem {len(my_mvps)} heróis chave para {raid_choice}.")
    elif progresso >= 0.5:
        st.warning(f"⚖️ **Possibilidade Média.** Você tem alguns heróis ({len(my_mvps)}), mas pode faltar dano ou sustain.")
    else:
        st.error("❌ **Possibilidade Baixa.** Faltam heróis específicos para as mecânicas desta Raid.")

# --- PÁGINA 2: GUIA GEAR RAIDS ---
elif page == "📖 Guia Gear Raids":
    st.title("📖 Tutoriais de Estratégia")
    st.write("Dicas essenciais para superar os estágios 19, 20 e 21.")
    
    for raid, info in STRATEGIES.items():
        with st.expander(f"📌 {raid} - Ver Detalhes"):
            st.write(info)
            st.markdown(f"**Recomendação:** Foque em heróis que aplicam debuffs específicos para {raid}.")

# --- PÁGINA 3: LISTA DE HERÓIS ---
elif page == "📑 Lista de Heróis":
    st.title("📑 Biblioteca Completa")
    for classe, nomes in HEROES.items():
        with st.expander(f"{classe} ({len(nomes)})"):
            st.write(", ".join(sorted(nomes)))

st.sidebar.markdown("---")
st.sidebar.caption("Versão Organizada 3.0")
