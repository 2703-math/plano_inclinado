import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Física Visual: Dinâmica",
    page_icon="🍎",
    layout="wide"
)

# ============================================
# CSS PERSONALIZADO
# ============================================
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #555;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .concept-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 4px solid;
        margin-bottom: 1rem;
    }
    .step-box {
        background: #fff8e1;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÕES DE PLOTAGEM COM AUTOSCALE DINÂMICO
# ============================================
def plot_plano_horizontal(massa, forca_aplicada, mu):
    """Calcula os limites dinamicamente para que o gráfico faça o autoscale perfeito de acordo com os valores"""
    fig = go.Figure()
    g = 10
    normal = massa * g
    atrito = normal * mu

    # Fator de escala proporcional
    f_scale = 0.04
    v_scale = 0.015

    len_f = (forca_aplicada * f_scale) if forca_aplicada > 0 else 0
    len_at = (atrito * f_scale) if atrito > 0 else 0
    len_vert = normal * v_scale

    # Chão
    max_x_chao = max(8.0, 2.0 + len_f, 2.0 + len_at)
    fig.add_shape(type="rect", x0=-max_x_chao, y0=-1, x1=max_x_chao, y1=0,
                  fillcolor="#bdc3c7", line=dict(width=0))
    
    # Bloco (centro em x=0, y=1)
    fig.add_shape(type="rect", x0=-1.5, y0=0, x1=1.5, y1=2,
                  fillcolor="#3498db", line=dict(color="#2980b9", width=2))
    
    # Vetor Força Aplicada (Direita)
    if forca_aplicada > 0:
        x_end_f = 1.5 + max(1.5, len_f)
        fig.add_annotation(
            x=x_end_f, y=1, ax=1.5, ay=1,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3, arrowcolor="#2ecc71"
        )
        fig.add_annotation(x=1.5 + (x_end_f - 1.5)/2, y=1.5, text=f"F = {forca_aplicada:.1f} N", showarrow=False, font=dict(color="#2ecc71", size=13))
    
    # Vetor Força de Atrito (Esquerda)
    if atrito > 0:
        x_end_at = -1.5 - max(1.5, len_at)
        fig.add_annotation(
            x=x_end_at, y=0.5, ax=-1.5, ay=0.5,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3, arrowcolor="#e74c3c"
        )
        fig.add_annotation(x=-1.5 + (x_end_at - (-1.5))/2, y=1.0, text=f"Fat = {atrito:.1f} N", showarrow=False, font=dict(color="#e74c3c", size=13))

    # Vetor Peso (Baixo)
    y_down = 1 - max(2.0, len_vert)
    fig.add_annotation(
        x=0, y=y_down, ax=0, ay=1, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor="#9b59b6"
    )
    fig.add_annotation(x=1.2, y=1 + (y_down - 1)/2, text=f"P = {normal:.1f} N", showarrow=False, font=dict(color="#9b59b6", size=13))

    # Vetor Normal (Cima)
    y_up = 1 + max(2.0, len_vert)
    fig.add_annotation(
        x=0, y=y_up, ax=0, ay=1, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor="#f39c12"
    )
    fig.add_annotation(x=1.2, y=1 + (y_up - 1)/2, text=f"N = {normal:.1f} N", showarrow=False, font=dict(color="#f39c12", size=13))

    # Autoscale dinâmico dos limites do eixo baseado nos vetores gerados
    lim_x = max_x_chao + 2.0
    lim_y = max(4.0, abs(y_down), abs(y_up)) + 1.5

    fig.update_layout(
        xaxis=dict(range=[-lim_x, lim_x], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-lim_y, lim_y], showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='white', margin=dict(l=0, r=0, t=10, b=10), height=380
    )
    return fig

def plot_plano_inclinado(massa, angulo_deg):
    """Calcula os limites e proporções dinamicamente para o plano inclinado"""
    fig = go.Figure()
    
    g = 10
    peso = massa * g
    ang_rad = math.radians(angulo_deg)
    px = peso * math.sin(ang_rad)
    py = peso * math.cos(ang_rad)
    
    R = 10 
    L = R * math.cos(ang_rad)
    H = R * math.sin(ang_rad)
    
    fig.add_trace(go.Scatter(
        x=[0, L, 0, 0], y=[0, 0, H, 0],
        fill="toself", fillcolor="#ecf0f1", line=dict(color="#bdc3c7", width=2),
        showlegend=False, hoverinfo="skip"
    ))
    
    cx = L / 2
    cy = H / 2
    
    s = 1.0
    bx = cx + s * math.sin(ang_rad)
    by = cy + s * math.cos(ang_rad)
    
    def rot(px_val, py_val):
        rx = px_val * math.cos(-ang_rad) - py_val * math.sin(-ang_rad)
        ry = px_val * math.sin(-ang_rad) + py_val * math.cos(-ang_rad)
        return bx + rx, by + ry

    p1, p2, p3, p4 = rot(-s, -s), rot(s, -s), rot(s, s), rot(-s, s)
    
    fig.add_trace(go.Scatter(
        x=[p1[0], p2[0], p3[0], p4[0], p1[0]],
        y=[p1[1], p2[1], p3[1], p4[1], p1[1]],
        fill="toself", fillcolor="#3498db", line=dict(color="#2980b9", width=2),
        showlegend=False, hoverinfo="skip"
    ))
    
    force_scale = 0.015
    len_p = max(1.8, peso * force_scale)
    len_n = max(1.8, py * force_scale)
    len_px = max(1.8, px * force_scale)
    
    # P (Peso total)
    fig.add_annotation(
        x=bx, y=by - len_p, ax=bx, ay=by, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor="#9b59b6"
    )
    fig.add_annotation(x=bx + 0.8, y=by - len_p / 2, text=f"P={peso:.1f}N", showarrow=False, font=dict(color="#9b59b6", size=12))
    
    # Normal
    nx = bx + len_n * math.sin(ang_rad)
    ny = by + len_n * math.cos(ang_rad)
    fig.add_annotation(
        x=nx, y=ny, ax=bx, ay=by, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#f39c12"
    )
    fig.add_annotation(x=nx + 0.6*math.sin(ang_rad), y=ny + 0.6*math.cos(ang_rad), text=f"N={py:.1f}N", showarrow=False, font=dict(color="#f39c12", size=12))
    
    # Py
    pyx = bx - len_n * math.sin(ang_rad)
    pyy = by - len_n * math.cos(ang_rad)
    fig.add_annotation(
        x=pyx, y=pyy, ax=bx, ay=by, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#e74c3c"
    )
    fig.add_annotation(x=pyx - 0.6*math.sin(ang_rad), y=pyy - 0.6*math.cos(ang_rad), text=f"Py={py:.1f}N", showarrow=False, font=dict(color="#e74c3c", size=12))
    
    # Px
    pxx = bx + len_px * math.cos(ang_rad)
    pxy = by - len_px * math.sin(ang_rad)
    fig.add_annotation(
        x=pxx, y=pxy, ax=bx, ay=by, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#2ecc71"
    )
    fig.add_annotation(x=pxx + 0.6*math.cos(ang_rad), y=pxy - 0.6*math.sin(ang_rad), text=f"Px={px:.1f}N", showarrow=False, font=dict(color="#2ecc71", size=13))

    # Autoscale dinâmico para a rampa
    max_dim = max(L, H) + 4.0
    fig.update_layout(
        xaxis=dict(range=[-3, max_dim], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-4, max_dim], scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0), height=420
    )
    return fig

# ============================================
# TÍTULO E ABAS SUPERIORES DE NAVEGAÇÃO
# ============================================
st.markdown('<div class="main-title">🍎 Física Visual: Dinâmica</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Entendendo as Leis de Newton e a Decomposição de Forças de forma interativa</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs([
    "2ª Lei de Newton (Horizontal)", 
    "Plano Inclinado (Decomposição)"
])

g = 10  # Gravidade local

# ============================================
# ABA 1: 2ª LEI DE NEWTON (HORIZONTAL)
# ============================================
with tab1:
    st.header("➡️ Princípio Fundamental da Dinâmica")
    st.markdown("""
    <div class="concept-card" style="border-left-color: #3498db;">
        <b>Definição:</b> A aceleração de um corpo é diretamente proporcional à força resultante que atua sobre ele e inversamente proporcional à sua massa.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("🎛️ Parâmetros do Bloco")
        massa = st.slider("Massa (kg)", 1.0, 50.0, 10.0, step=1.0, key="m1")
        forca = st.slider("Força Aplicada (N)", 0.0, 200.0, 80.0, step=5.0, key="f1")
        mu = st.slider("Coeficiente de Atrito (μ)", 0.0, 1.0, 0.3, step=0.05, key="mu1")
        
        normal = massa * g
        atrito = mu * normal
        forca_resultante = max(0.0, forca - atrito)
        aceleracao = forca_resultante / massa
        
        st.plotly_chart(plot_plano_horizontal(massa, forca, mu), use_container_width=True)
        
    with col2:
        st.subheader("🧮 Raciocínio e Cálculos")
        st.markdown(r"$$ F_R = m \cdot a \implies a = \frac{F_R}{m} $$")
        
        st.markdown(f"""
        1. **Força Normal ($N$):** $m \cdot g$ = {massa} $\cdot$ {g} = **{normal} N**
        2. **Força de Atrito ($F_{{at}}$):** $\mu \cdot N$ = {mu:.2f} $\cdot$ {normal} = **{atrito:.1f} N**
        3. **Força Aplicada ($F$):** **{forca:.1f} N**
        4. **Força Resultante ($F_R$):** {forca} - {atrito:.1f} = **{forca_resultante:.1f} N**
        """)
        
        st.markdown("---")
        st.markdown("**Aceleração gerada:**")
        st.markdown(rf"$$ a = \frac{{{forca_resultante:.1f}}}{{{massa}}} = {aceleracao:.2f} \text{{ m/s}}^2 $$")
        
        if forca_resultante == 0:
            st.warning("A força aplicada não é suficiente para vencer o atrito. O bloco permanece em repouso ou MRU.")

# ============================================
# ABA 2: PLANO INCLINADO
# ============================================
with tab2:
    st.header("📐 Decomposição de Forças no Plano Inclinado")
    st.markdown("""
    <div class="concept-card" style="border-left-color: #2ecc71;">
        <b>Definição:</b> Em um plano inclinado, a força <b>Peso (P)</b> é decomposta em duas direções: 
        uma paralela ao plano (<b>P<sub>x</sub></b>) e outra perpendicular (<b>P<sub>y</sub></b>).
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("🎛️ Parâmetros do Plano")
        massa_plano = st.slider("Massa do Bloco (kg)", 1.0, 50.0, 10.0, step=1.0, key="m2")
        angulo = st.slider("Ângulo de Inclinação (°)", 0, 90, 30, step=1, key="ang2")
        
        p = massa_plano * g
        ang_rad = math.radians(angulo)
        px = p * math.sin(ang_rad)
        py = p * math.cos(ang_rad)
        
        st.plotly_chart(plot_plano_inclinado(massa_plano, angulo), use_container_width=True)
        
    with col2:
        st.subheader("🧮 Decomposição Matemática")
        st.markdown(r"$$ P = m \cdot g \quad | \quad P_x = P \cdot \sin(\theta) \quad | \quad P_y = P \cdot \cos(\theta) $$")
        
        st.markdown(f"""
        <div style="font-size:1.0rem;line-height:1.8;">
        <b>Dados Iniciais:</b><br>
        Massa (m) = {massa_plano} kg<br>
        Ângulo (&theta;) = {angulo}°<br>
        Peso Total (P) = {massa_plano} &times; {g} = <b>{p:.1f} N</b>
        <hr>
        <b>Componente Paralela (P<sub>x</sub>):</b> {px:.1f} N<br>
        <b>Componente Perpendicular (P<sub>y</sub>):</b> {py:.1f} N
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(rf"$$ P_x = {p:.1f} \cdot \sin({angulo}^\circ) = {px:.1f} \text{{ N}} $$")
        st.markdown(rf"$$ P_y = {p:.1f} \cdot \cos({angulo}^\circ) = {py:.1f} \text{{ N}} $$")
        
        st.markdown("""
        <div class="step-box">
            <b>💡 Dica:</b><br>
            Em <b>0°</b>, <b>P<sub>x</sub></b> = 0 e <b>P<sub>y</sub></b> = P.<br>
            Em <b>90°</b>, <b>P<sub>y</sub></b> = 0 e <b>P<sub>x</sub></b> = P.
        </div>
        """, unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    🍎 <b>Física Visual</b> — Ferramenta educacional para o ensino de Dinâmica
</div>
""", unsafe_allow_html=True)
