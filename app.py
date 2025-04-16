from flask import Flask, request, jsonify
import subprocess
import os
import tempfile
import shutil
import git
import asyncio

app = Flask(__name__)

def suggest_test_cases(mutant_analysis, language):
    """
    Suggest test cases based on surviving mutants.
    This is a placeholder for the AI-powered test case suggestion.
    """
    # Replace this with your actual AI-powered test case generation logic
    return ["//Test Case Suggestion 1", "//Test Case Suggestion 2"]

def analyze_mutants(infection_output):
    """
    Analyze the infection output to identify surviving mutants.
    """
    # Implement your logic to parse the infection output and extract information about surviving mutants
    # For example, you can look for lines indicating mutants that were not killed
    # This is a placeholder, replace with actual analysis
    surviving_mutants = []
    return surviving_mutants


@app.route('/analyze', methods=['POST'])
async def analyze_repository():
    """
    Endpoint to analyze a Git repository for mutation testing.
    """
    data = request.get_json()
    git_url = data.get('git_url')

    if not git_url:
        return jsonify({'status': 'error', 'message': 'Git URL is required'}), 400

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as repo_dir:
        try:
            # Clone the repository
            print(f"Cloning repository into {repo_dir}")
            git.Repo.clone_from(git_url, repo_dir)
            print("Repository cloned successfully.")

            # Detect programming language (only allow PHP)
            try:
                language = detect_language(repo_dir)
                if language != 'PHP':
                    return jsonify({'status': 'error', 'message': 'Only PHP repositories are supported'}), 400
                print(f"Detected language: {language}")
            except Exception as e:
                return jsonify({'status': 'error', 'message': str(e)}), 500

            # Run Infection and PHPUnit
            print("Running mutation tests...")
            infection_output = run_mutation_tests(repo_dir)
            print("Mutation tests completed.")
            print("Infection Output:")
            print(infection_output)


            # Analyze mutants and suggest test cases
            print("Analyzing mutants...")
            surviving_mutants = analyze_mutants(infection_output)
            print(f"Surviving mutants: {surviving_mutants}")

            print("Suggesting test cases...")
            test_cases = suggest_test_cases("Mutant analysis details", language)
            print(f"Suggested test cases: {test_cases}")

            return jsonify({
                'status': 'success',
                'message': 'Mutation testing complete',
                'test_cases': test_cases
            }), 200

        except git.exc.GitCommandError as e:
            return jsonify({'status': 'error', 'message': f'Git error: {str(e)}'}), 500
        except subprocess.CalledProcessError as e:
            return jsonify({'status': 'error', 'message': f'Subprocess error: {str(e)}'}), 500
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500

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
    app.run(debug=True, port=9002)
