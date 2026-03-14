# Simple TeX Live API Service
# Run: python texlive_api.py

from flask import Flask, request, jsonify, send_file
import subprocess
import tempfile
import os
import base64
from pathlib import Path

app = Flask(__name__)

ALLOWED_ENGINES = ['xelatex', 'pdflatex', 'lualatex']
MAX_TIMEOUT = 180


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


@app.route('/compile', methods=['POST'])
def compile():
    data = request.get_json()
    
    tex_content = data.get('tex')
    engine = data.get('engine', 'xelatex')
    timeout = min(data.get('timeout', MAX_TIMEOUT), MAX_TIMEOUT)
    
    if not tex_content:
        return jsonify({"error": "No tex content provided"}), 400
    
    if engine not in ALLOWED_ENGINES:
        return jsonify({"error": f"Invalid engine: {engine}"}), 400
    
    # Create temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_file = Path(tmpdir) / "input.tex"
        tex_file.write_text(tex_content)
        
        # Compile
        try:
            result = subprocess.run(
                [engine, "-interaction=nonstopmode", tex_file.name],
                cwd=tmpdir,
                capture_output=True,
                timeout=timeout,
            )
            
            pdf_file = tex_file.with_suffix('.pdf')
            
            if pdf_file.exists():
                pdf_data = base64.b64encode(pdf_file.read_bytes()).decode()
                return jsonify({
                    "success": True,
                    "pdf": pdf_data,
                    "engine": engine,
                })
            else:
                # Return error log
                return jsonify({
                    "success": False,
                    "error": "PDF not generated",
                    "log": result.stderr.decode()[-2000:],
                }), 500
                
        except subprocess.TimeoutExpired:
            return jsonify({"error": "Compilation timeout"}), 504
        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
