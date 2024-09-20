PYTHON = python3
PROJECT_NAME = grokgemini

SOURCE_DIR = $(PROJECT_NAME)
TEST_DIR = test
DOC_DIR = doc

.PHONY: all clean

# targets
all: format check test

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

check-tests:
	@echo "Checking $(PROJECT_NAME)..."
	$(PYTHON) -m mypy $(TEST_DIR)

test:
	@echo "Testing $(PROJECT_NAME)..."
	$(PYTHON) -m pytest $(TEST_DIR)

test-verbose:
	@echo "Testing $(PROJECT_NAME)..."
	$(PYTHON) -m pytest --verbose $(TEST_DIR)

run:
	@echo "Running $(PROJECT_NAME)..."
	$(PYTHON) -m $(SOURCE_DIR).main 

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  all:          Format, check, and test the project"
	@echo "  clean:        Clean the project"
	@echo "  format:       Format the project"
	@echo "  check:        Check implementation"
	@echo "  check-tests:  Check tests"
	@echo "  test:         Test the project"
	@echo "  test-verbose: Test the project with verbose output"
	@echo "  run:          Run the project"
	@echo "  help:         Show this help message"
