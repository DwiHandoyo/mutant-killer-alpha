from flask import Flask, request, jsonify, copy_current_request_context
from flask_socketio import SocketIO, emit
import subprocess
import os
import tempfile
import shutil
import git
import uuid
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS for all origins


def suggest_test_cases(mutant_analysis, language, repo_dir):
    """
    Suggest test cases based on surviving mutants.
    This is a placeholder for the AI-powered test case suggestion.
    """
    # Replace this with your actual AI-powered test case generation logic
    return ["//Test Case Suggestion 1", "//Test Case Suggestion 2"]

def analyze_mutants(infection_output, repo_dir):
    """
    Analyze the infection output to identify surviving mutants.
    """
    # Implement your logic to parse the infection output and extract information about surviving mutants
    # For example, you can look for lines indicating mutants that were not killed
    # This is a placeholder, replace with actual analysis
    surviving_mutants = []
    return surviving_mutants

def perform_analysis(git_url, repo_dir, analysis_id):
    """
    Perform mutation testing and test case suggestion.
    """
    try:
        # Clone the repository
        print(f"Cloning repository into {repo_dir}")
        git.Repo.clone_from(git_url, repo_dir)
        print("Repository cloned successfully.")

        # Detect programming language (only allow PHP)
        try:
            language = detect_language(repo_dir)
            if language != 'PHP':
                emit('analysis_complete', {'status': 'error', 'message': 'Only PHP repositories are supported'}, room=analysis_id)
                return
            print(f"Detected language: {language}")
        except Exception as e:
            emit('analysis_complete', {'status': 'error', 'message': str(e)}, room=analysis_id)
            return

        # Run Infection and PHPUnit
        print("Running mutation tests...")
        infection_output = run_mutation_tests(repo_dir)
        print("Mutation tests completed.")

        # Analyze mutants and suggest test cases
        print("Analyzing mutants...")
        surviving_mutants = analyze_mutants(infection_output, repo_dir)

        print("Suggesting test cases...")
        test_cases = suggest_test_cases("Mutant analysis details", language, repo_dir)

        emit('analysis_complete', {'status': 'success', 'message': 'Mutation testing complete', 'test_cases': test_cases}, room=analysis_id)
    except Exception as e:
        emit('analysis_complete', {'status': 'error', 'message': str(e)}, room=analysis_id)
@app.route('/analyze', methods=['POST'])
async def analyze_repository():
    """
    Endpoint to analyze a Git repository for mutation testing.
    """
    data = request.get_json()
    git_url = data.get('git_url')

    if not git_url:
        return jsonify({'status': 'error', 'message': 'Git URL is required'}), 400

    analysis_id = str(uuid.uuid4())
    ws_url = f"ws://127.0.0.1:9002/ws?id={analysis_id}"  # Construct WebSocket URL

    # Start analysis in a background thread
    def run_analysis():
        with tempfile.TemporaryDirectory() as repo_dir:
            perform_analysis(git_url, repo_dir, analysis_id)

    thread = Thread(target=run_analysis)
    thread.start()

    return jsonify({'status': 'pending', 'websocket_url': ws_url, 'analysis_id': analysis_id}), 202
@socketio.on('connect')
def handle_connect():
    analysis_id = request.args.get('id')
    if analysis_id:
        print(f"Client connected with analysis_id: {analysis_id}")
        socketio.join_room(analysis_id)

def detect_language(repo_dir):
    """
    Detect the programming language of the repository.
    """
    # Check if it's a PHP project by looking for composer.json
    if os.path.exists(os.path.join(repo_dir, 'composer.json')):
        return 'PHP'
    else:
        raise ValueError("Unsupported language. Only PHP repositories are supported.")

def run_mutation_tests(repo_dir):
    """
    Run mutation tests using Infection and PHPUnit.
    """
    try:
        # Run composer install
        subprocess.run(['composer', 'install'], cwd=repo_dir, check=True, capture_output=True)

        # Run Infection
        infection_process = subprocess.run(
            ['vendor/bin/infection'],
            cwd=repo_dir,
            check=True,
            capture_output=True,
            text=True
        )
        return infection_process.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command: {e.cmd}")
        print(f"Return Code: {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        raise

if __name__ == '__main__':
    socketio.run(app, debug=True, port=9002)
