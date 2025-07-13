import streamlit as st
import psutil
import pandas as pd
import time
import matplotlib.pyplot as plt

def system_monitor_viz():
    st.subheader("📊 Real-time System Resource Monitor")

    # CPU
    st.markdown("### 🧠 CPU Usage")
    cpu_perc = psutil.cpu_percent(percpu=True)
    df_cpu = pd.DataFrame({
        "Core": [f"Core {i}" for i in range(len(cpu_perc))],
        "Usage (%)": cpu_perc
    })
    st.bar_chart(df_cpu.set_index("Core"))

    # Memory
    st.markdown("### 💾 Memory Usage")
    memory = psutil.virtual_memory()
    df_mem = pd.DataFrame({
        "Metric": ["Used", "Free"],
        "Value (GB)": [round(memory.used / 1e9, 2), round(memory.available / 1e9, 2)]
    })
    st.bar_chart(df_mem.set_index("Metric"))

    st.markdown(f"**Total RAM**: {round(memory.total / 1e9, 2)} GB")
    st.markdown(f"**Used RAM**: {round(memory.used / 1e9, 2)} GB ({memory.percent}%)")
    st.markdown(f"**Available RAM**: {round(memory.available / 1e9, 2)} GB")

def read_ram(st):
    st.subheader("📟 System RAM Information")

    ram = psutil.virtual_memory()
    st.write(f"**Total RAM:** {round(ram.total / 1e9, 2)} GB")
    st.write(f"**Available RAM:** {round(ram.available / 1e9, 2)} GB")
    st.write(f"**Used RAM:** {round(ram.used / 1e9, 2)} GB")
    st.write(f"**RAM Usage Percentage:** {ram.percent}%")

    st.markdown("### 🧮 Running Processes (Top 5 by Memory)")

    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    top_processes = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:5]
    st.table(top_processes)
