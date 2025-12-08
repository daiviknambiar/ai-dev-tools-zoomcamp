/**
 * Code Editor Controller
 * Provides UI for code input, execution, and output display
 */

import executor from './executor.js';

export class CodeEditorController {
    constructor() {
        this.currentCode = '';
        this.currentLanguage = 'javascript';
        this.isExecuting = false;
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Language selector
        const langSelect = document.getElementById('code-language');
        if (langSelect) {
            langSelect.addEventListener('change', (e) => {
                this.currentLanguage = e.target.value;
                this.updateLanguageTemplate();
            });
        }

        // Execute button
        const executeBtn = document.getElementById('execute-code-btn');
        if (executeBtn) {
            executeBtn.addEventListener('click', () => this.executeCode());
        }

        // Clear button
        const clearBtn = document.getElementById('clear-code-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.clearCode());
        }

        // Code textarea
        const codeInput = document.getElementById('code-input');
        if (codeInput) {
            codeInput.addEventListener('input', (e) => {
                this.currentCode = e.target.value;
            });
        }

        // Initialize Python on load
        this.initializePython();
    }

    async initializePython() {
        try {
            const result = await executor.initPython();
            const status = document.getElementById('python-status');
            if (status) {
                if (result.success) {
                    status.textContent = '✓ Python ready';
                    status.style.color = 'green';
                } else {
                    status.textContent = '✗ Python unavailable';
                    status.style.color = 'orange';
                }
            }
        } catch (error) {
            console.error('Error initializing Python:', error);
        }
    }

    updateLanguageTemplate() {
        const codeInput = document.getElementById('code-input');
        if (!codeInput) return;

        const templates = {
            javascript: `// JavaScript Example
console.log("Hello, World!");

// Simple function
function add(a, b) {
    return a + b;
}

console.log(add(5, 3));`,
            python: `# Python Example
print("Hello, World!")

# Simple function
def add(a, b):
    return a + b

print(add(5, 3))`
        };

        if (codeInput.value === '' || codeInput.value === templates[this.currentLanguage === 'js' ? 'javascript' : this.currentLanguage]) {
            codeInput.value = templates[this.currentLanguage === 'js' ? 'javascript' : this.currentLanguage];
            this.currentCode = codeInput.value;
        }
    }

    async executeCode() {
        if (this.isExecuting) return;
        if (!this.currentCode.trim()) {
            this.displayError('No code to execute');
            return;
        }

        this.isExecuting = true;
        const executeBtn = document.getElementById('execute-code-btn');
        const originalText = executeBtn?.textContent || 'Execute';

        if (executeBtn) {
            executeBtn.disabled = true;
            executeBtn.textContent = 'Executing...';
        }

        try {
            const result = await executor.execute(this.currentCode, this.currentLanguage);

            if (result.success) {
                this.displayOutput(result.output);
            } else {
                this.displayError(result.error);
            }
        } catch (error) {
            this.displayError(`Unexpected error: ${error.message}`);
        } finally {
            this.isExecuting = false;
            if (executeBtn) {
                executeBtn.disabled = false;
                executeBtn.textContent = originalText;
            }
        }
    }

    clearCode() {
        const codeInput = document.getElementById('code-input');
        if (codeInput) {
            codeInput.value = '';
            this.currentCode = '';
        }
        this.clearOutput();
    }

    displayOutput(output) {
        const outputDiv = document.getElementById('code-output');
        if (!outputDiv) return;

        outputDiv.style.backgroundColor = '#e8f5e9';
        outputDiv.style.borderLeft = '4px solid #4caf50';
        outputDiv.innerHTML = `<pre style="margin: 0; color: #333; white-space: pre-wrap; word-wrap: break-word;">${this.escapeHtml(output || '(no output)')}</pre>`;
    }

    displayError(error) {
        const outputDiv = document.getElementById('code-output');
        if (!outputDiv) return;

        outputDiv.style.backgroundColor = '#ffebee';
        outputDiv.style.borderLeft = '4px solid #f44336';
        outputDiv.innerHTML = `<pre style="margin: 0; color: #d32f2f; white-space: pre-wrap; word-wrap: break-word;">❌ ${this.escapeHtml(error || 'Unknown error')}</pre>`;
    }

    clearOutput() {
        const outputDiv = document.getElementById('code-output');
        if (outputDiv) {
            outputDiv.innerHTML = '<p style="color: #999;">Output will appear here...</p>';
            outputDiv.style.backgroundColor = '#f5f5f5';
            outputDiv.style.borderLeft = '4px solid #ddd';
        }
    }

    escapeHtml(text) {
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, (m) => map[m]);
    }

    show() {
        const codeSection = document.getElementById('code-section');
        if (codeSection) {
            codeSection.classList.remove('hidden');
        }
    }

    hide() {
        const codeSection = document.getElementById('code-section');
        if (codeSection) {
            codeSection.classList.add('hidden');
        }
    }
}
