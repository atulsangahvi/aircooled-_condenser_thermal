
import streamlit as st
import math

# Physical property constants (can be replaced with CoolProp for more accuracy)
AIR_CP = 1006  # J/kg-K, specific heat of air
AIR_DENSITY = 1.06  # kg/m3
AIR_K = 0.0262  # W/m-K, thermal conductivity of air
AIR_PR = 0.71  # Prandtl number

def calculate_velocity(volume_flow_m3h, area_m2):
    return (volume_flow_m3h / 3600) / area_m2

def calculate_reynolds_number(rho, velocity, diameter, mu):
    return (rho * velocity * diameter) / mu

def calculate_nusselt_number(Re, Pr):
    if Re < 2300:
        return 3.66  # laminar
    else:
        return 0.023 * Re**0.8 * Pr**0.3  # Dittus-Boelter for turbulent

def calculate_u(nu, k, d_h):
    return nu * k / d_h

def main():
    st.title("Condenser Heat Transfer Calculator")

    st.sidebar.header("Geometry Inputs")
    d_outer_mm = st.sidebar.number_input("Tube Outer Diameter (mm)", value=9.52)
    coil_height_mm = st.sidebar.number_input("Coil Height (mm)", value=600.0)
    coil_length_mm = st.sidebar.number_input("Coil Length (mm)", value=1000.0)
    fin_spacing_fpi = st.sidebar.number_input("Fin Density (FPI)", value=14.0)
    n_rows = st.sidebar.number_input("Number of Tube Rows", value=3)
    coil_thickness_mm = st.sidebar.number_input("Coil Thickness (mm)", value=76.2)

    st.sidebar.header("Air Side Inputs")
    air_flow_m3h = st.sidebar.number_input("Air Flow Rate (m³/h)", value=2500.0)
    air_temp_in = st.sidebar.number_input("Air Inlet Temperature (°C)", value=35.0)
    air_temp_out = st.sidebar.number_input("Air Outlet Temperature (°C)", value=45.0)

    d_outer = d_outer_mm / 1000  # m
    coil_height = coil_height_mm / 1000
    coil_length = coil_length_mm / 1000
    coil_thickness = coil_thickness_mm / 1000

    fins_per_m = fin_spacing_fpi * 39.37
    finned_area = coil_length * coil_height
    flow_area = finned_area * 0.25  # Assume 25% free area

    velocity = calculate_velocity(air_flow_m3h, flow_area)
    Re = calculate_reynolds_number(AIR_DENSITY, velocity, d_outer, 1.8e-5)
    Nu = calculate_nusselt_number(Re, AIR_PR)
    U = calculate_u(Nu, AIR_K, d_outer)

    Q_air = AIR_DENSITY * (air_flow_m3h / 3600) * AIR_CP * (air_temp_out - air_temp_in)
    delta_T_lm = ((air_temp_out - air_temp_in) / math.log((air_temp_out + 273.15)/(air_temp_in + 273.15)))
    A_required = Q_air / (U * delta_T_lm)

    st.subheader("Results")
    st.write(f"Air Velocity: {velocity:.2f} m/s")
    st.write(f"Reynolds Number: {Re:.0f}")
    st.write(f"Nusselt Number: {Nu:.1f}")
    st.write(f"Overall Heat Transfer Coefficient U: {U:.2f} W/m²·K")
    st.write(f"Heat Transfer Rate Q: {Q_air/1000:.2f} kW")
    st.write(f"Log Mean Temperature Difference (LMTD): {delta_T_lm:.2f} °C")
    st.write(f"Required Surface Area: {A_required:.2f} m²")

if __name__ == "__main__":
    main()

