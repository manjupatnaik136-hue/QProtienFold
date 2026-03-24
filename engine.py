import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import Aer
import io
import base64

class QuantumProteinEngine:
    def __init__(self):
        self.backend = Aer.get_backend('qasm_simulator')

    def run_quantum_logic(self, sequence):
        # 1. Encoding Logic from your Notebook
        encoding_map = {char: idx+1 for idx, char in enumerate(set(sequence))}
        encoded = [encoding_map[c] for c in sequence[:4]] # Taking first 4 for 4-qubit circuit
        
        # 2. Quantum Circuit with your Gates (H, Ry, Cx)
        qc = QuantumCircuit(4)
        for i in range(4):
            qc.h(i) # Superposition
            qc.ry(encoded[i] * np.pi / 4, i) # Rotation encoding
            
        for i in range(3):
            qc.cx(i, i+1) # Interaction/Entanglement
            
        qc.measure_all()
        
        # 3. Execution
        job = self.backend.run(qc, shots=1024)
        counts = job.result().get_counts()
        max_state = max(counts, key=counts.get)
        
        # 4. Classification Logic from Notebook
        if max_state.count('1') > max_state.count('0'):
            fold_type = "Beta Sheet"
            energy = -round(np.mean(encoded), 2)
        else:
            fold_type = "Alpha Helix"
            energy = -round(np.mean(encoded) * 0.8, 2)
            
        return fold_type, energy, max_state

    def generate_3d_plot(self, sequence):
        # Coordinates generation (keep your same logic)
        length = len(sequence)
        x = np.cumsum(np.random.uniform(-1, 1, length))
        y = np.cumsum(np.random.uniform(-1, 1, length))
        z = np.cumsum(np.random.uniform(-1, 1, length))
        
        # Figure size set chesi title lekunda clean ga create cheyyi
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plotting
        ax.plot(x, y, z, marker='o', color='#004a99', markersize=8, linewidth=2)

        # IMPORTANT: Title line asalu undakudadhu
        # ax.set_title(...) <--- EE LINE NI POORTHIGA DELETE CHEYI

        # AXIS AND BORDERS CLEANUP
        ax.axis('off') 
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        
        # Convert plot to image
        buf = io.BytesIO()
        # transparent=True valla dashboard color lo image merge avthundi
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True, pad_inches=0)
        plt.close(fig)
        return buf