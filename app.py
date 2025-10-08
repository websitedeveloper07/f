from flask import Flask, request, Response
import subprocess
import shlex
import os

app = Flask(__name__)

# ---------- API Endpoint ----------
# Users will call: /sk.php?sec=<stripe_key>&lista=<card_data>
@app.route("/sk.php", methods=["GET"])
def run_php_script():
    # Capture GET parameters
    sec = request.args.get("sec", "")
    lista = request.args.get("lista", "")

    if not sec or not lista:
        return {"error": "Missing 'sec' or 'lista' parameter"}, 400

    # Safely build the PHP command
    cmd = f"php sk.php {shlex.quote(sec)} {shlex.quote(lista)}"

    # Pass environment variables if needed (e.g., for your proxy credentials)
    env = os.environ.copy()

    try:
        # Run the PHP script and capture stdout and stderr
        result = subprocess.run(
            shlex.split(cmd),
            capture_output=True,
            text=True,
            env=env,
            timeout=30  # prevent hanging
        )

        output = result.stdout
        if result.stderr:
            output += "\nErrors:\n" + result.stderr

        return Response(output, mimetype="text/html")

    except subprocess.TimeoutExpired:
        return {"error": "PHP script timed out"}, 504
    except Exception as e:
        return {"error": str(e)}, 500

# ---------- Run Flask ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
