import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 1. THE DATA (Phase 3 Results)
# ==========================================
# X-Axis: Input Load (Transactions Submitted)
tx_load = [100, 500, 1000, 5000]

# Y-Axis 1: Throughput (TPS)
# Shows linear growth until saturation at ~342 TPS
tps_values = [48, 152, 285, 342]

# Y-Axis 2: Latency (ms)
# Shows strict adherence to 2s block time with slight overhead
latency_values = [2042, 2045, 2048, 2115]

# ==========================================
# 2. GRAPH 1: THROUGHPUT ANALYSIS
# ==========================================
def plot_throughput():
    plt.figure(figsize=(10, 6))
    
    # Plot Line
    plt.plot(tx_load, tps_values, marker='o', linestyle='-', color='#0072BD', linewidth=2, markersize=8)
    
    # Styling
    plt.title('Figure 1: Network Throughput vs. Transaction Load', fontsize=14, fontweight='bold')
    plt.xlabel('Input Load (Transactions)', fontsize=12)
    plt.ylabel('Throughput (TPS)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Annotate the Peak
    plt.annotate(f'Saturation Point\n({tps_values[-1]} TPS)', 
                 xy=(tx_load[-1], tps_values[-1]), 
                 xytext=(tx_load[-1]-1500, tps_values[-1]-50),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    # Save
    filename = 'throughput_analysis.png'
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Saved: {filename}")

# ==========================================
# 3. GRAPH 2: LATENCY ANALYSIS
# ==========================================
def plot_latency():
    plt.figure(figsize=(10, 6))
    
    # Plot Line
    plt.plot(tx_load, latency_values, marker='s', linestyle='--', color='#D95319', linewidth=2, markersize=8)
    
    # Styling
    plt.title('Figure 2: Transaction Latency vs. Load', fontsize=14, fontweight='bold')
    plt.xlabel('Input Load (Transactions)', fontsize=12)
    plt.ylabel('Average Latency (ms)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Set Y-Axis limit to show the "2 second" floor clearly
    plt.ylim(0, 2500)
    
    # Add a reference line for the Block Time (2000ms)
    plt.axhline(y=2000, color='green', linestyle=':', label='Block Time (2.0s)')
    plt.legend()

    # Save
    filename = 'latency_analysis.png'
    plt.savefig(filename, dpi=300)
    plt.close()
    print(f"Saved: {filename}")

if __name__ == "__main__":
    print("--- Generating IEEE Research Graphs ---")
    plot_throughput()
    plot_latency()
    print("---------------------------------------")
    print("Graphs generated successfully.")
