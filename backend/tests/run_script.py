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

        # If counts are available, generate the histogram image
        if counts:
            # Create the histogram plot
            fig = plt.figure()
            plot_histogram(counts, ax=fig.gca())

            # Save the plot to a BytesIO object to return as a base64 string
            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png')
            img_bytes.seek(0)

            # Convert the image to a base64 string
            img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

            # Return the result along with the image in base64
            return {
                "result": "Success",
                "counts": counts,
                "plot_image": img_base64
            }
        else:
            return {"result": "No results", "message": "No counts returned from simulation."}

    except Exception as e:
        # If there was an error during execution, return the error message
        return {"result": "Error", "error_message": str(e)}
