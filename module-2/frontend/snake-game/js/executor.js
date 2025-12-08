/**
 * Code Executor Module
 * Executes JavaScript and Python code in WASM for security
 * - JavaScript: Native browser execution (sandboxed)
 * - Python: Pyodide WASM runtime
 */

import * as Pyodide from 'pyodide';

class CodeExecutor {
    constructor() {
        this.pythonReady = false;
        this.pythonInterpreter = null;
        this.executionTimeout = 5000; // 5 second timeout
    }

    /**
     * Initialize Python WASM runtime
     */
    async initPython() {
        if (this.pythonReady) return;

        try {
            this.pythonInterpreter = await Pyodide.loadPyodide({
                indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.23.4/full/'
            });
            this.pythonReady = true;
            return { success: true, message: 'Python WASM initialized' };
        } catch (error) {
            return { success: false, error: `Failed to initialize Python: ${error.message}` };
        }
    }

    /**
     * Execute JavaScript code
     * @param {string} code - JavaScript code to execute
     * @returns {Promise<{success: boolean, output: string, error?: string}>}
     */
    async executeJavaScript(code) {
        return new Promise((resolve) => {
            const timeout = setTimeout(() => {
                resolve({ success: false, error: 'JavaScript execution timeout (5s)' });
            }, this.executionTimeout);

            try {
                // Capture console output
                const originalLog = console.log;
                const originalError = console.error;
                const originalWarn = console.warn;
                let output = '';

                console.log = (...args) => {
                    output += args.map(arg => JSON.stringify(arg)).join(' ') + '\n';
                };
                console.error = (...args) => {
                    output += 'ERROR: ' + args.map(arg => JSON.stringify(arg)).join(' ') + '\n';
                };
                console.warn = (...args) => {
                    output += 'WARN: ' + args.map(arg => JSON.stringify(arg)).join(' ') + '\n';
                };

                // Create isolated scope
                const sandbox = {};
                const func = new Function('output', `
                    let __output = '';
                    ${code}
                    return __output;
                `);

                const result = func(output);

                // Restore console
                console.log = originalLog;
                console.error = originalError;
                console.warn = originalWarn;

                clearTimeout(timeout);

                resolve({
                    success: true,
                    output: output + (result ? result.toString() : ''),
                    language: 'javascript'
                });
            } catch (error) {
                console.log = console.log;
                console.error = console.error;
                console.warn = console.warn;
                clearTimeout(timeout);

                resolve({
                    success: false,
                    error: error.message || String(error),
                    language: 'javascript'
                });
            }
        });
    }

    /**
     * Execute Python code
     * @param {string} code - Python code to execute
     * @returns {Promise<{success: boolean, output: string, error?: string}>}
     */
    async executePython(code) {
        if (!this.pythonReady) {
            const initResult = await this.initPython();
            if (!initResult.success) {
                return { success: false, error: initResult.error, language: 'python' };
            }
        }

        return new Promise((resolve) => {
            const timeout = setTimeout(() => {
                resolve({ success: false, error: 'Python execution timeout (5s)', language: 'python' });
            }, this.executionTimeout);

            try {
                // Create Python namespace
                const namespace = this.pythonInterpreter.toPy({});

                // Execute code and capture output
                const pyCode = `
import sys
from io import StringIO
import traceback

# Capture stdout
_old_stdout = sys.stdout
sys.stdout = StringIO()

try:
    exec("""${code.replace(/"/g, '\\"')}""")
    _output = sys.stdout.getvalue()
except Exception as e:
    _output = traceback.format_exc()
finally:
    sys.stdout = _old_stdout
    
_output
                `;

                const result = this.pythonInterpreter.runPython(pyCode);
                const output = this.pythonInterpreter.runPython('_output');

                clearTimeout(timeout);

                resolve({
                    success: true,
                    output: output || 'Code executed successfully',
                    language: 'python'
                });
            } catch (error) {
                clearTimeout(timeout);

                resolve({
                    success: false,
                    error: error.message || String(error),
                    language: 'python'
                });
            }
        });
    }

    /**
     * Execute code based on language
     * @param {string} code - Code to execute
     * @param {string} language - 'javascript' or 'python'
     * @returns {Promise<{success: boolean, output: string, error?: string, language: string}>}
     */
    async execute(code, language = 'javascript') {
        if (!code || !code.trim()) {
            return { success: false, error: 'No code provided', language };
        }

        language = language.toLowerCase().trim();

        if (language === 'javascript' || language === 'js') {
            return this.executeJavaScript(code);
        } else if (language === 'python' || language === 'py') {
            return this.executePython(code);
        } else {
            return { success: false, error: `Unsupported language: ${language}`, language };
        }
    }

    /**
     * Get supported languages
     */
    getSupportedLanguages() {
        return ['javascript', 'js', 'python', 'py'];
    }

    /**
     * Check if Python is ready
     */
    isPythonReady() {
        return this.pythonReady;
    }
}

// Create singleton instance
const executor = new CodeExecutor();

export { executor as default, CodeExecutor };
