import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from io import StringIO


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Automotive Radiator Simulator",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# TITLE
# ==========================================================

st.title("🚗 Automotive Radiator Simulator")

st.markdown("""
### Educational Heat Transfer Simulator

Didactic simulator for thermal analysis of a compact cross-flow
automotive radiator using energy balance and convection equations.
""")

# ==========================================================
# IMAGE
# ==========================================================

import os

if os.path.exists("radiator.png"):
    st.image(
        "radiator.png",
        caption="Automotive Radiator",
        width=500
    )
else:
    st.info(
        "Optional image not found. Add 'radiator.png' to the project folder."
    )

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("⚙️ Input Parameters")

# ----------------------------------------------------------
# GEOMETRY
# ----------------------------------------------------------

st.sidebar.subheader("Geometry")

N_tubes = st.sidebar.slider(
    "Number of Tubes",
    10,
    100,
    40
)

D_i = st.sidebar.slider(
    "Tube Diameter [m]",
    0.001,
    0.020,
    0.005
)

L = st.sidebar.slider(
    "Tube Length [m]",
    0.10,
    2.00,
    0.65
)

st.sidebar.divider()

# ----------------------------------------------------------
# FLUID
# ----------------------------------------------------------

st.sidebar.subheader("Fluid")

fluids = {
    "Water": 4180,
    "Antifreeze": 3500,
    "Oil": 2100
}

selected_fluid = st.sidebar.selectbox(
    "Working Fluid",
    list(fluids.keys())
)

cp = fluids[selected_fluid]

st.sidebar.divider()

# ----------------------------------------------------------
# CONDITIONS
# ----------------------------------------------------------

st.sidebar.subheader("Operating Conditions")

m_dot = st.sidebar.slider(
    "Mass Flow Rate [kg/s]",
    0.1,
    2.0,
    0.6
)

T_in = st.sidebar.slider(
    "Water Inlet Temperature [°C]",
    40,
    120,
    90
)

T_out = st.sidebar.slider(
    "Water Outlet Temperature [°C]",
    20,
    100,
    65
)

T_air_in = st.sidebar.slider(
    "Air Inlet Temperature [°C]",
    0,
    50,
    20
)

T_air_out = st.sidebar.slider(
    "Air Outlet Temperature [°C]",
    0,
    80,
    40
)

h = st.sidebar.slider(
    "Convective Coefficient h [W/(m²·K)]",
    10,
    200,
    45
)

# ==========================================================
# CALCULATIONS
# ==========================================================

A_tube = math.pi * D_i * L
A_total = N_tubes * A_tube

Q = m_dot * cp * (T_in - T_out)

qpp = Q / A_total

DeltaT = (
    ((T_in + T_out) / 2)
    -
    ((T_air_in + T_air_out) / 2)
)

Q_conv = h * A_total * DeltaT

# ==========================================================
# TABS
# ==========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "📈 Parametric Studies",
    "🔥 Thermal Diagram",
    "📖 Theory",
    "🧠 Conclusions"
])

# ==========================================================
# DASHBOARD
# ==========================================================

with tab1:

    st.header("Main Results")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Heat Transfer",
        f"{Q/1000:.2f} kW"
    )

    c2.metric(
        "Heat Flux",
        f"{qpp:,.0f} W/m²"
    )

    c3.metric(
        "Area",
        f"{A_total:.3f} m²"
    )

    c4.metric(
        "Convective Heat",
        f"{Q_conv:.2f} W"
    )

    st.markdown("---")

    results = pd.DataFrame({
        "Parameter":[
            "Heat Transfer Q",
            "Heat Flux q''",
            "Total Area",
            "Convective Heat",
            "Specific Heat"
        ],
        "Value":[
            Q,
            qpp,
            A_total,
            Q_conv,
            cp
        ]
    })

    st.subheader("Results Table")

    st.dataframe(
        results,
        use_container_width=True
    )

    csv = results.to_csv(index=False)

    st.download_button(
        label="📥 Download Results CSV",
        data=csv,
        file_name="radiator_results.csv",
        mime="text/csv"
    )

# ==========================================================
# PARAMETRIC STUDIES
# ==========================================================

with tab2:

    g1, g2, g3, g4 = st.tabs([
        "Flow Rate",
        "Geometry",
        "Thermal",
        "Fluids"
    ])

    # ======================================================
    # FLOW RATE
    # ======================================================

    with g1:

        mass_flow_rates = np.linspace(
            0.1,
            2.0,
            20
        )

        Q_mass = []

        for mdot in mass_flow_rates:

            Q_temp = mdot * cp * (T_in - T_out)

            Q_mass.append(
                Q_temp / 1000
            )

        fig1, ax1 = plt.subplots(figsize=(8,5))

        ax1.plot(
            mass_flow_rates,
            Q_mass,
            marker="o"
        )

        ax1.set_title(
            "Heat Transfer vs Mass Flow Rate"
        )

        ax1.set_xlabel(
            "Mass Flow Rate [kg/s]"
        )

        ax1.set_ylabel(
            "Heat Transfer [kW]"
        )

        ax1.grid(True)

        st.pyplot(fig1)

    # ======================================================
    # GEOMETRY
    # ======================================================

    with g2:

        tube_numbers = [20,40,60,80,100]

        qpp_values = []

        for Nt in tube_numbers:

            area_temp = Nt * math.pi * D_i * L

            qpp_values.append(
                Q / area_temp
            )

        fig2, ax2 = plt.subplots(figsize=(8,5))

        ax2.plot(
            tube_numbers,
            qpp_values,
            marker="s"
        )

        ax2.set_title(
            "Heat Flux vs Number of Tubes"
        )

        ax2.set_xlabel(
            "Number of Tubes"
        )

        ax2.set_ylabel(
            "Heat Flux [W/m²]"
        )

        ax2.grid(True)

        st.pyplot(fig2)

        diameters = [
            0.003,
            0.005,
            0.007,
            0.009
        ]

        qpp_diam = []

        for d in diameters:

            area_temp = N_tubes * math.pi * d * L

            qpp_diam.append(
                Q / area_temp
            )

        fig3, ax3 = plt.subplots(figsize=(8,5))

        ax3.plot(
            diameters,
            qpp_diam,
            marker="o"
        )

        ax3.set_title(
            "Heat Flux vs Diameter"
        )

        ax3.set_xlabel(
            "Diameter [m]"
        )

        ax3.set_ylabel(
            "Heat Flux [W/m²]"
        )

        ax3.grid(True)

        st.pyplot(fig3)

    # ======================================================
    # THERMAL
    # ======================================================

    with g3:

        Tin_values = [
            70,
            80,
            90,
            100,
            110
        ]

        Q_temp_values = []

        for Tin in Tin_values:

            Q_temp = (
                m_dot
                * cp
                * (Tin - T_out)
            )

            Q_temp_values.append(
                Q_temp / 1000
            )

        fig4, ax4 = plt.subplots(figsize=(8,5))

        ax4.plot(
            Tin_values,
            Q_temp_values,
            marker="o"
        )

        ax4.set_title(
            "Heat Transfer vs Inlet Temperature"
        )

        ax4.set_xlabel(
            "Inlet Temperature [°C]"
        )

        ax4.set_ylabel(
            "Heat Transfer [kW]"
        )

        ax4.grid(True)

        st.pyplot(fig4)

        h_values = [
            20,
            40,
            60,
            80,
            100,
            120
        ]

        Qconv_values = []

        for h_value in h_values:

            Qconv_values.append(
                h_value
                * A_total
                * DeltaT
            )

        fig5, ax5 = plt.subplots(figsize=(8,5))

        ax5.plot(
            h_values,
            Qconv_values,
            marker="^"
        )

        ax5.set_title(
            "Convective Heat vs h"
        )

        ax5.set_xlabel(
            "h [W/(m²·K)]"
        )

        ax5.set_ylabel(
            "Qconv [W]"
        )

        ax5.grid(True)

        st.pyplot(fig5)

    # ======================================================
    # FLUIDS
    # ======================================================

    with g4:

        fluid_names = []
        Q_fluids = []

        for fluid, cp_value in fluids.items():

            fluid_names.append(
                fluid
            )

            Q_temp = (
                m_dot
                * cp_value
                * (T_in - T_out)
            )

            Q_fluids.append(
                Q_temp / 1000
            )

        fig6, ax6 = plt.subplots(figsize=(8,5))

        ax6.bar(
            fluid_names,
            Q_fluids
        )

        ax6.set_title(
            "Fluid Comparison"
        )

        ax6.set_ylabel(
            "Heat Transfer [kW]"
        )

        st.pyplot(fig6)

# ==========================================================
# THERMAL DIAGRAM
# ==========================================================

with tab3:

    st.header("Radiator Thermal Diagram")

    fig, ax = plt.subplots(figsize=(10,4))

    ax.axis("off")

    ax.arrow(
        0.1,
        0.7,
        0.6,
        0,
        head_width=0.03
    )

    ax.text(
        0.02,
        0.72,
        f"Water In\n{T_in}°C"
    )

    ax.text(
        0.75,
        0.72,
        f"Water Out\n{T_out}°C"
    )

    rect = plt.Rectangle(
        (0.40,0.45),
        0.15,
        0.20,
        fill=False,
        linewidth=2
    )

    ax.add_patch(rect)

    ax.text(
        0.43,
        0.53,
        "Radiator"
    )

    for i in range(7):

        ax.arrow(
            0.48,
            0.15,
            0,
            0.20,
            head_width=0.02
        )

    ax.text(
        0.20,
        0.05,
        f"Air In {T_air_in}°C"
    )

    ax.text(
        0.60,
        0.05,
        f"Air Out {T_air_out}°C"
    )

    st.pyplot(fig)

# ==========================================================
# THEORY
# ==========================================================

with tab4:

    st.header("Mathematical Model")

    st.latex(
        r"Q=\dot{m}c_p(T_{in}-T_{out})"
    )

    st.latex(
        r"A_{tube}=\pi D_i L"
    )

    st.latex(
        r"A_{total}=N_{tubes}\pi D_iL"
    )

    st.latex(
        r"q''=\frac{Q}{A_{total}}"
    )

    st.latex(
        r"Q_{conv}=hA\Delta T"
    )

    st.subheader("Assumptions")

    st.write("• Steady-state operation")
    st.write("• Constant properties")
    st.write("• Uniform flow")
    st.write("• No external losses")
    st.write("• Constant h")

# ==========================================================
# CONCLUSIONS
# ==========================================================

with tab5:

    st.header("Automatic Engineering Assessment")

    if selected_fluid == "Water":

        st.success(
            "Water provides the highest heat transfer capability."
        )

    if qpp > 150000:

        st.warning(
            "High heat flux detected."
        )

    if Q_conv > 1000:

        st.success(
            "Radiator exhibits strong convective performance."
        )

    elif Q_conv > 500:

        st.info(
            "Moderate cooling performance."
        )

    else:

        st.error(
            "Low cooling performance."
        )

    st.markdown("---")

    st.write(
        "Increasing mass flow rate increases heat transfer."
    )

    st.write(
        "Increasing inlet temperature increases thermal energy."
    )

    st.write(
        "Increasing area reduces heat flux concentration."
    )

    st.write(
        "Higher convection coefficients improve cooling."
    )