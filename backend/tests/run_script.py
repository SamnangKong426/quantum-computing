from fastapi import FastAPI
import io
import base64
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram

app = FastAPI()

@app.post("/runscript")
async def runscript():
    # Raw code string to be executed
    code = """
        from qiskit import QuantumCircuit, transpile
        from qiskit_aer import AerSimulator
        from qiskit.visualization import plot_histogram

        qc = QuantumCircuit(2, 2)

        qc.h(0)
        qc.h(1)

        qc.measure([0, 1], [0, 1])

        sim = AerSimulator()
        compiled = transpile(qc, sim)
        result = sim.run(compiled).result()
        counts = result.get_counts()

        # plot_histogram(counts)
    """
    
    # Normalize indentation of the code before executing it
    code = "\n".join([line.lstrip() for line in code.splitlines()])
    
    # Create a safe local context for the execution of the user code
    local_var = {}

    try:
        # Dynamically execute the cleaned code in a restricted local context
        exec(code, {}, local_var)

        # Extract counts from the local variables
        counts = local_var.get('counts', {})

        # Convert counts into a more user-friendly response
        if counts:
            # If there are counts, return the counts
            return {"result": "Success", "counts": counts}
        else:
            return {"result": "No results", "message": "No counts returned from simulation."}

    except Exception as e:
        # If there was an error during execution, return the error message
        return {"result": "Error", "error_message": str(e)}
