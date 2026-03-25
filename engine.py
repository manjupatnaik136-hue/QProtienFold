import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import io
import requests

# ✅ Amino Acid Mapping
amino_map = {
    'A':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,
    'I':8,'K':9,'L':10,'M':11,'N':12,'P':13,
    'Q':14,'R':15,'S':16,'T':17,'V':18,'W':19,'Y':20
}

class QuantumProteinEngine:

    def __init__(self):
        self.sim = AerSimulator()

    # ✅ UniProt API Fetch
    def fetch_uniprot_sequence(self, name):
        try:
            url = f"https://rest.uniprot.org/uniprotkb/search?query={name}&format=fasta&size=1"
            response = requests.get(url, timeout=10)

            if response.status_code == 200 and response.text:
                lines = response.text.strip().split('\n')
                seq = "".join(lines[1:]).replace(" ", "").replace("\r", "")
                valid = "".join([c for c in seq if c in amino_map])
                return valid[:25] if valid else None

            return None

        except Exception as e:
            print("UniProt Fetch Error:", e)
            return None

    # ✅ Main Quantum Logic
    def run_quantum_logic(self, seq):

        valid_amino_acids = set("ACDEFGHIKLMNPQRSTVWY")

        if not seq or not isinstance(seq, str):
            seq = "AAAA"

        seq = seq.upper().strip()

        if not all(c in valid_amino_acids for c in seq):
            fetched_seq = self.fetch_uniprot_sequence(seq)
            seq = fetched_seq if fetched_seq else "AAAA"

        if len(seq) < 4:
            seq = (seq * 4)[:4]

        seq = seq[:4].ljust(4, seq[0])

        encoded = np.array([amino_map.get(c, 1) for c in seq])

        max_val = np.max(encoded) if np.max(encoded) != 0 else 1
        normalized = (encoded / max_val) * np.pi

        n = len(normalized)

        best_energy = float('inf')
        best_probs = {}
        energy_history = []

        # ✅ BEFORE ENERGY
        initial_theta = np.random.rand(n)
        initial_energy = -np.sum(np.cos(normalized + initial_theta))

        # ✅ Optimization Loop
        for _ in range(20):

            qc = QuantumCircuit(n)

            for i in range(n):
                qc.ry(normalized[i], i)

            theta = np.random.rand(n)

            for i in range(n):
                qc.rz(theta[i], i)

            for i in range(n - 1):
                qc.cx(i, i + 1)

            qc.measure_all()

            result = self.sim.run(qc, shots=512).result()
            counts = result.get_counts()

            total = sum(counts.values()) if counts else 1
            probs = {k: v / total for k, v in counts.items()}

            energy = -np.sum(np.cos(normalized + theta))
            energy_history.append(energy)

            if energy < best_energy:
                best_energy = energy
                best_probs = probs

        final_energy = best_energy

        if not best_probs:
            best_probs = {"0000": 1.0}

        top_states = sorted(best_probs.items(), key=lambda x: x[1], reverse=True)[:5]
        best_state = top_states[0][0]

        fold = "Beta Sheet" if best_state.count('1') > best_state.count('0') else "Alpha Helix"

        confidence = round(top_states[0][1] * 100, 2)

        confidence_regions = []
        for i in range(n):
            prob_1 = sum(v for k, v in best_probs.items() if len(k) > i and k[i] == '1')
            confidence_regions.append(round(prob_1 * 100, 2))

        # ================================
        # ✅ NEW: Convergence Data
        # ================================
        conv_steps = list(range(len(energy_history)))
        conv_energies = energy_history

        # ================================
        # ✅ NEW: Parallel Search Data
        # ================================
        parallel_energies = []

        for _ in range(10):
            random_theta = np.random.rand(n)
            energy = -np.sum(np.cos(normalized + random_theta))
            parallel_energies.append(energy)

        return (
            fold,
            round(initial_energy, 3),
            round(final_energy, 3),
            energy_history,
            top_states,
            confidence,
            confidence_regions,
            best_state,
            conv_steps,
            conv_energies,
            parallel_energies
        )

    # 📊 Energy Plot
    def generate_energy_plot(self, history):

        fig = plt.figure(figsize=(5, 3))
        plt.plot(history)
        plt.xlabel("Iterations")
        plt.ylabel("Energy")
        plt.title("Optimization Progress")

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)

        buf.seek(0)
        return buf

    # 🧬 2D Probability Plot
    def generate_2d_plot(self, probs):

        states = [k for k, _ in probs]
        values = [v for _, v in probs]

        fig = plt.figure(figsize=(6, 3))
        plt.bar(states, values)

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)

        buf.seek(0)
        return buf

    # 🧊 3D Structure Plot
    def generate_3d_plot(self, sequence):

        sequence = sequence if sequence else "AAAA"
        length = min(len(sequence), 50)

        x = np.cumsum(np.random.uniform(-1, 1, length))
        y = np.cumsum(np.random.uniform(-1, 1, length))
        z = np.cumsum(np.random.uniform(-1, 1, length))

        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111, projection='3d')

        ax.plot(x, y, z, marker='o', linewidth=2)

        ax.axis('off')
        ax.grid(False)

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        plt.close(fig)

        buf.seek(0)
        return buf
