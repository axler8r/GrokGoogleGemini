# Contribute
By following these guidelines, you'll be able to contribute to
_GrokGoogleGemini_ outlines the steps to get started and the guidelines for
submitting contributions.

### Getting Started
+ Run `code GrokGoogleGemini.code-workspace` to open the project in VS Code
+ Start the devcontainer
+ Select the Python interpreter, `Ctrl+Shift+P` > `Python: Select Interpreter` > `.venv/bin/python`
+ Open a terminal in the devcontainer
+ Install dependencies: `make activate`, `make init`
+ Familiarize yourself with our codebase
+ Run the application: `python -m grokgemini.main --help`
+ Explore `make` targets: `make help`

### Code Conventions
+ Run `make format` to apply code formatting

### Issue Reporting
+ Report bugs and feature requests using _GitHub Issues_
+ Include a clear description of the issue and any relevant code snippets

### Pull Request Guidelines
+ Create a new branch for your changes: `git flow feature start <YOUR_FEATURE_NAME>`
+ Write a clear and concise commit message
+ Include `pytest` tests for your changes
+ Submit your pull request for review

### License and Copyright
+ _GrokGoogleGemini_ is licensed under MIT license
+ Contributors must agree to the terms of the license and copyright

By following these guidelines, you'll be able to contribute to
_GrokGoogleGemini_ effectively and efficiently. Thank you for your
contributions!
