import os
import pickle
import sys
import matplotlib.pyplot as plt
import argparse
import pandas as pd

def plot_throughput():
    try:
        # Load throughput data
        with open(os.path.join(os.path.dirname(__file__),'results/throughput-rho.txt'), 'rb') as f:
            pairs = pickle.load(f)
        
        # Plot
        throughput, rho = zip(*pairs)
        plt.figure(figsize=(8, 6))
        plt.plot(rho, throughput, marker='o', linestyle='-', color='coral')
        plt.title('Throughput vs. Traffic Intensity (ρ)')
        plt.xlabel('Traffic Intensity (ρ)')
        plt.ylabel('Throughput (Kbps)')
        plt.grid(True)
        path = os.path.join(os.path.dirname(__file__),'plots/throughput-rho.png')
        plt.savefig(path)
        print(f"Plot saved to {path}")

    except (FileNotFoundError, IOError) as e:
        print(f"Error loading throughput data: {e}")
    except Exception as e:
        print(f"An error occurred while plotting throughput: {e}")

def plot_latency():
    try:
        # Load latency data
        with open(os.path.join(os.path.dirname(__file__),'results/latency-rho.txt'), 'rb') as f:
            pairs = pickle.load(f)

        # Plot
        latency, rho = zip(*pairs)
        plt.figure(figsize=(8, 6))
        plt.plot(rho, latency, marker='o', linestyle='-', color='coral')
        plt.title('Latency vs. Traffic Intensity (ρ)')
        plt.xlabel('Traffic Intensity (ρ)')
        plt.ylabel('Latency (ms)')
        plt.grid(True)
        path = os.path.join(os.path.dirname(__file__),'plots/latency-rho.png')
        plt.savefig(path)
        print(f"Plot saved to {path}")

    except (FileNotFoundError, IOError) as e:
        print(f"Error loading latency data: {e}")
    except Exception as e:
        print(f"An error occurred while plotting latency: {e}")

def plot_websites():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__),'results/performance_metrics.csv'))
    print(df.to_string())
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test result plotter')
    parser.add_argument('test', choices=['t', 'l', 'w'], help="Specify the type of test to plot. Valid options are 't' for throughput test, 'w' for performance test or 'l' for latency test.")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    test = parser.parse_args().test

    if test == "t":
        plot_throughput()
    elif test == "l":
        plot_latency()
    elif test == "w":
        plot_websites()
    else:
        print("No such test!")
