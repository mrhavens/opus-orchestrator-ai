"""Web UI for Opus Orchestrator.

A simple, novice-friendly web interface for generating manuscripts.
"""

import os
import asyncio
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()


# HTML Template for the UI
WEB_UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Opus Orchestrator - AI Book Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #e4e4e7;
            padding: 20px;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        h1 {
            font-size: 2.5rem;
            background: linear-gradient(90deg, #a855f7, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #9ca3af;
            font-size: 1.1rem;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 24px;
            backdrop-filter: blur(10px);
        }
        
        .card h2 {
            font-size: 1.3rem;
            margin-bottom: 20px;
            color: #a855f7;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #d1d5db;
        }
        
        input[type="text"],
        input[type="number"],
        textarea,
        select {
            width: 100%;
            padding: 12px 16px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            background: rgba(0, 0, 0, 0.3);
            color: #e4e4e7;
            font-size: 1rem;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #a855f7;
            box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2);
        }
        
        textarea {
            min-height: 120px;
            resize: vertical;
        }
        
        .row {
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
        }
        
        .col {
            flex: 1;
            min-width: 200px;
        }
        
        .btn {
            padding: 14px 28px;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .btn-primary {
            background: linear-gradient(90deg, #a855f7, #ec4899);
            color: white;
            width: 100%;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(168, 85, 247, 0.4);
        }
        
        .btn-primary:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .tabs {
            display: flex;
            gap: 8px;
            margin-bottom: 20px;
        }
        
        .tab {
            padding: 10px 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            background: transparent;
            color: #9ca3af;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .tab.active {
            background: rgba(168, 85, 247, 0.2);
            border-color: #a855f7;
            color: #a855f7;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .source-input {
            display: none;
        }
        
        .source-input.active {
            display: block;
        }
        
        .output-section {
            display: none;
        }
        
        .output-section.active {
            display: block;
        }
        
        #manuscript {
            min-height: 300px;
            font-family: 'Courier New', monospace;
            font-size: 0.95rem;
            line-height: 1.7;
            white-space: pre-wrap;
        }
        
        .progress {
            display: none;
            text-align: center;
            padding: 40px;
        }
        
        .progress.active {
            display: block;
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 4px solid rgba(168, 85, 247, 0.2);
            border-top-color: #a855f7;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .status {
            color: #9ca3af;
            font-size: 1.1rem;
        }
        
        .success-message {
            background: rgba(34, 197, 94, 0.1);
            border: 1px solid rgba(34, 197, 94, 0.3);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 20px;
            color: #22c55e;
        }
        
        .error-message {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 20px;
            color: #ef4444;
        }
        
        .file-drop {
            border: 2px dashed rgba(168, 85, 247, 0.4);
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .file-drop:hover, .file-drop.dragover {
            border-color: #a855f7;
            background: rgba(168, 85, 247, 0.1);
        }
        
        .file-drop input {
            display: none;
        }
        
        .file-info {
            margin-top: 10px;
            color: #22c55e;
            font-size: 0.9rem;
        }
        
        footer {
            text-align: center;
            margin-top: 40px;
            color: #6b7280;
            font-size: 0.9rem;
        }
        
        footer a {
            color: #a855f7;
            text-decoration: none;
        }
        
        .features {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 20px;
        }
        
        .feature {
            flex: 1;
            min-width: 150px;
            padding: 16px;
            background: rgba(168, 85, 247, 0.1);
            border-radius: 8px;
            text-align: center;
        }
        
        .feature-icon {
            font-size: 1.5rem;
            margin-bottom: 8px;
        }
        
        .feature-name {
            font-weight: 600;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 Opus Orchestrator</h1>
            <p class="subtitle">AI-Powered Book Generation</p>
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">🎯</div>
                    <div class="feature-name">7 Story Frameworks</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">🤖</div>
                    <div class="feature-name">AI Critique</div>
                </div>
                <div class="feature">
                    <div class="feature-icon">☁️</div>
                    <div class="feature-name">Cloud Storage</div>
                </div>
            </div>
        </header>
        
        <div class="card">
            <h2>Generate Your Manuscript</h2>
            
            <form id="generateForm">
                <!-- Source Type Tabs -->
                <div class="tabs">
                    <button type="button" class="tab active" data-source="concept">💡 Idea</button>
                    <button type="button" class="tab" data-source="github">🐙 GitHub</button>
                    <button type="button" class="tab" data-source="s3">🪣 S3</button>
                    <button type="button" class="tab" data-source="upload">📁 Upload</button>
                </div>
                
                <!-- Source Inputs -->
                <div class="source-input active" id="concept-input">
                    <div class="form-group">
                        <label>Your Story Concept</label>
                        <textarea name="concept" placeholder="A robot dreams of electric sheep and discovers love in the last library on Earth..."></textarea>
                    </div>
                </div>
                
                <div class="source-input" id="github-input">
                    <div class="form-group">
                        <label>GitHub Repository</label>
                        <input type="text" name="repo" placeholder="owner/repository">
                    </div>
                </div>
                
                <div class="source-input" id="s3-input">
                    <div class="row">
                        <div class="col">
                            <div class="form-group">
                                <label>S3 Bucket</label>
                                <input type="text" name="s3_bucket" placeholder="my-bucket">
                            </div>
                        </div>
                        <div class="col">
                            <div class="form-group">
                                <label>Path Prefix</label>
                                <input type="text" name="s3_prefix" placeholder="notes/">
                            </div>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Endpoint (optional, for MinIO/DO Spaces)</label>
                        <input type="text" name="s3_endpoint" placeholder="https://nyc3.digitaloceanspaces.com">
                    </div>
                </div>
                
                <div class="source-input" id="upload-input">
                    <div class="form-group">
                        <label>Upload Files</label>
                        <div class="file-drop" id="fileDrop">
                            <input type="file" id="fileInput" name="files" multiple accept=".txt,.md,.markdown,.notes">
                            <p>📂 Drag & drop files here<br>or click to browse</p>
                            <div class="file-info" id="fileInfo"></div>
                        </div>
                    </div>
                </div>
                
                <!-- Generation Options -->
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label>Framework</label>
                            <select name="framework">
                                <option value="snowflake">Snowflake Method</option>
                                <option value="hero-journey">Hero's Journey</option>
                                <option value="three-act">Three-Act Structure</option>
                                <option value="save-the-cat">Save the Cat</option>
                                <option value="story-circle">Story Circle</option>
                                <option value="seven-point">7-Point Plot</option>
                                <option value="fichtean">Fichtean Curve</option>
                            </select>
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label>Genre</label>
                            <select name="genre">
                                <option value="fiction">Fiction</option>
                                <option value="science-fiction">Science Fiction</option>
                                <option value="fantasy">Fantasy</option>
                                <option value="romance">Romance</option>
                                <option value="mystery">Mystery</option>
                                <option value="thriller">Thriller</option>
                                <option value="literary">Literary Fiction</option>
                                <option value="nonfiction">Nonfiction</option>
                            </select>
                        </div>
                    </div>
                </div>
                
                <div class="row">
                    <div class="col">
                        <div class="form-group">
                            <label>Target Words</label>
                            <input type="number" name="words" value="5000" min="100" max="200000">
                        </div>
                    </div>
                    <div class="col">
                        <div class="form-group">
                            <label>Chapters</label>
                            <input type="number" name="chapters" value="3" min="1" max="50">
                        </div>
                    </div>
                </div>
                
                <!-- Output Options -->
                <div class="form-group">
                    <label>Save Output To</label>
                    <select name="output_dest">
                        <option value="">Download (browser)</option>
                        <option value="s3">S3 / MinIO</option>
                        <option value="github">GitHub Repository</option>
                    </select>
                </div>
                
                <div id="s3-output-options" style="display:none;">
                    <div class="row">
                        <div class="col">
                            <input type="text" name="output_s3_bucket" placeholder="Output bucket">
                        </div>
                        <div class="col">
                            <input type="text" name="output_s3_path" placeholder="Path (e.g., manuscripts/)">
                        </div>
                    </div>
                </div>
                
                <div id="github-output-options" style="display:none;">
                    <input type="text" name="output_repo" placeholder="owner/repository" style="margin-bottom:10px;">
                </div>
                
                <button type="submit" class="btn btn-primary" id="generateBtn">
                    ✨ Generate Manuscript
                </button>
            </form>
        </div>
        
        <!-- Progress -->
        <div class="card progress" id="progress">
            <div class="spinner"></div>
            <p class="status" id="statusText">Initializing...</p>
        </div>
        
        <!-- Output -->
        <div class="card output-section" id="output">
            <h2>Your Manuscript</h2>
            <div id="successMessage"></div>
            <pre id="manuscript"></pre>
            <button class="btn btn-primary" id="downloadBtn" style="margin-top:20px;">
                📥 Download
            </button>
            <button class="btn" id="copyBtn" style="margin-top:20px;background:rgba(255,255,255,0.1);color:#e4e4e7;">
                📋 Copy
            </button>
        </div>
        
        <footer>
            <p>Powered by <a href="https://github.com/mrhavens/opus-orchestrator-ai">Opus Orchestrator AI</a></p>
            <p>Built with LangGraph, CrewAI, AutoGen, and PydanticAI</p>
        </footer>
    </div>
    
    <script>
        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.source-input').forEach(i => i.classList.remove('active'));
                
                tab.classList.add('active');
                document.getElementById(tab.dataset.source + '-input').classList.add('active');
            });
        });
        
        // Output destination switching
        document.querySelector('select[name="output_dest"]').addEventListener('change', (e) => {
            document.getElementById('s3-output-options').style.display = e.target.value === 's3' ? 'flex' : 'none';
            document.getElementById('github-output-options').style.display = e.target.value === 'github' ? 'block' : 'none';
        });
        
        // File upload
        const fileInput = document.getElementById('fileInput');
        const fileDrop = document.getElementById('fileDrop');
        const fileInfo = document.getElementById('fileInfo');
        
        fileDrop.addEventListener('click', () => fileInput.click());
        fileDrop.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileDrop.classList.add('dragover');
        });
        fileDrop.addEventListener('dragleave', () => fileDrop.classList.remove('dragover'));
        fileDrop.addEventListener('drop', (e) => {
            e.preventDefault();
            fileDrop.classList.remove('dragover');
            handleFiles(e.dataTransfer.files);
        });
        fileInput.addEventListener('change', () => handleFiles(fileInput.files));
        
        function handleFiles(files) {
            if (files.length > 0) {
                fileInfo.textContent = `✓ ${files.length} file(s) selected`;
            }
        }
        
        // Form submission
        const form = document.getElementById('generateForm');
        const generateBtn = document.getElementById('generateBtn');
        const progress = document.getElementById('progress');
        const statusText = document.getElementById('statusText');
        const outputSection = document.getElementById('output');
        const manuscriptEl = document.getElementById('manuscript');
        const successMessage = document.getElementById('successMessage');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            generateBtn.disabled = true;
            progress.classList.add('active');
            outputSection.classList.remove('active');
            successMessage.innerHTML = '';
            
            const formData = new FormData(form);
            
            // Determine source type
            const activeTab = document.querySelector('.tab.active').dataset.source;
            
            const payload = {
                framework: formData.get('framework'),
                genre: formData.get('genre'),
                target_word_count: parseInt(formData.get('words')),
                chapters: parseInt(formData.get('chapters')),
            };
            
            // Add source based on active tab
            if (activeTab === 'concept') {
                payload.concept = formData.get('concept');
            } else if (activeTab === 'github') {
                payload.repo = formData.get('repo');
            } else if (activeTab === 's3') {
                // For S3, we'd need additional API support
                statusText.textContent = 'S3 input not yet implemented in API';
                progress.classList.remove('active');
                generateBtn.disabled = false;
                return;
            } else if (activeTab === 'upload') {
                // Handle file upload
                statusText.textContent = 'Processing files...';
                const files = formData.getAll('files');
                if (files.length > 0) {
                    // Read first file as concept for now
                    const reader = new FileReader();
                    reader.onload = async (e) => {
                        payload.concept = e.target.result;
                        await generateManuscript(payload);
                    };
                    reader.readAsText(files[0]);
                    return;
                }
            }
            
            await generateManuscript(payload);
        });
        
        async function generateManuscript(payload) {
            statusText.textContent = 'Generating manuscript...';
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                
                if (!response.ok) {
                    throw new Error((await response.json()).detail || 'Generation failed');
                }
                
                const result = await response.json();
                
                progress.classList.remove('active');
                outputSection.classList.add('active');
                manuscriptEl.textContent = result.manuscript;
                
                successMessage.innerHTML = `<div class="success-message">
                    ✓ Generated ${result.word_count.toLocaleString()} words in ${result.chapters} chapters
                </div>`;
                
            } catch (error) {
                progress.classList.remove('active');
                successMessage.innerHTML = `<div class="error-message">${error.message}</div>`;
            }
            
            generateBtn.disabled = false;
        }
        
        // Download
        document.getElementById('downloadBtn').addEventListener('click', () => {
            const content = manuscriptEl.textContent;
            const blob = new Blob([content], {type: 'text/markdown'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'opus-manuscript.md';
            a.click();
            URL.revokeObjectURL(url);
        });
        
        // Copy
        document.getElementById('copyBtn').addEventListener('click', () => {
            navigator.clipboard.writeText(manuscriptEl.textContent);
            document.getElementById('copyBtn').textContent = '✓ Copied!';
            setTimeout(() => {
                document.getElementById('copyBtn').textContent = '📋 Copy';
            }, 2000);
        });
    </script>
</body>
</html>
"""


def create_web_ui(app: FastAPI) -> None:
    """Create and mount the web UI."""
    from fastapi.responses import HTMLResponse
    
    @app.get("/", response_class=HTMLResponse)
    async def index():
        """Serve the main UI page."""
        return WEB_UI_TEMPLATE
    
    @app.get("/ui", response_class=HTMLResponse)
    async def ui():
        """Alias for /"""
        return WEB_UI_TEMPLATE
