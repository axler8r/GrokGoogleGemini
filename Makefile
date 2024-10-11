# command aliases
PYTHON = python3

# location aliases
PROJECT_NAME = grokgemini
SOURCE_DIR = $(PROJECT_NAME)
TEST_DIR = test
DOC_DIR = doc

# phony targets
.PHONY: all activate deactivate reactivate clean check check-test test test-verbose run help

# targets
all: format check test

activate:
	@echo "Activating poetry shell..."
	poetry shell

reactivate:
	@echo "Reactivating existing poetry shell..."
	bash -c "source $(shell poetry env info --path)/bin/activate"

deactivate:
	@echo "Deactivating existing poetry shell..."
	deactivate

clean:
	rm -rf __pycache__

format:
	@echo "Formatting $(PROJECT_NAME)..."
	$(PYTHON) -m autoflake \
		--remove-all-unused-imports \
		--remove-unused-variables \
		--in-place \
		--recursive $(SOURCE_DIR) $(TEST_DIR)
	$(PYTHON) -m isort $(SOURCE_DIR) $(TEST_DIR)
	$(PYTHON) -m black $(SOURCE_DIR) $(TEST_DIR)

check:
	@echo "Checking $(PROJECT_NAME)..."
	$(PYTHON) -m mypy --check-untyped-defs $(SOURCE_DIR)

check-test:
	@echo "Checking $(PROJECT_NAME)..."
	$(PYTHON) -m mypy $(TEST_DIR)

test:
	@echo "Testing $(TEST_DIR)..."
	$(PYTHON) -m pytest $(TEST_DIR)

test-verbose:
	@echo "Testing $(TEST_DIR)..."
	$(PYTHON) -m pytest --verbose $(TEST_DIR)

run:
	@echo "Running $(PROJECT_NAME)..."
	$(PYTHON) -m $(SOURCE_DIR).main 

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  all:          Format, check, and test the project"
	@echo "  activate:     Activate poetry shell"
	@echo "  reactivate:   Reactivate the existing poetry shell"
	@echo "  deactivate:   Deactivate the existing poetry shell"
	@echo "  clean:        Clean the project"
	@echo "  format:       Format the project"
	@echo "  check:        Check implementation"
	@echo "  check-tests:  Check tests"
	@echo "  test:         Test the project"
	@echo "  test-verbose: Test the project with verbose output"
	@echo "  run:          Run the project"
	@echo "  help:         Show this help message"
