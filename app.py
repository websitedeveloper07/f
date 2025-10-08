from flask import Flask, request, Response
import subprocess
import shlex
import os

app = Flask(__name__)

@app.route("/script.php", methods=["GET"])
def run_php_script():
    # Capture GET parameters
    sec = request.args.get("sec", "")
    lista = request.args.get("lista", "")

    if not sec or not lista:
        return {"error": "Missing sec or lista parameter"}, 400

    # Build the command to call PHP script
    cmd = f"php sk.php '{sec}' '{lista}'"

    # Pass any environment variables if needed
    env = os.environ.copy()

    try:
        # Run the PHP script and capture output
        result = subprocess.run(
            shlex.split(cmd),
            capture_output=True,
            text=True,
            env=env,
            timeout=20
        )
        output = result.stdout
        if result.stderr:
            output += "\nErrors:\n" + result.stderr
        return Response(output, mimetype="text/html")
    except subprocess.TimeoutExpired:
        return {"error": "PHP script timed out"}, 504

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
