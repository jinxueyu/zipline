.PHONY: pip_compile

PIP_DEPENDENCY_DIR=.
PIP_DEPENDENCY_SOURCES=$(wildcard $(PIP_DEPENDENCY_DIR)/requirements*.in)
PIP_DEPENDENCY_TARGETS=$(PIP_DEPENDENCY_SOURCES:.in=.txt.out)

pip_compile: $(PIP_DEPENDENCY_TARGETS)

$(PIP_DEPENDENCY_DIR)/requirements.txt.out: $(PIP_DEPENDENCY_DIR)/requirements.in
	pip-compile --output-file=$(PIP_DEPENDENCY_DIR)/requirements.txt.out $(PIP_DEPENDENCY_DIR)/requirements.in

$(PIP_DEPENDENCY_DIR)/requirements_blaze.txt.out: $(PIP_DEPENDENCY_DIR)/requirements_blaze.in $(PIP_DEPENDENCY_DIR)/requirements.txt.out
	pip-compile --output-file=$@ ${ARGS} $^

$(PIP_DEPENDENCY_DIR)/requirements_dev.txt.out: $(PIP_DEPENDENCY_DIR)/requirements_dev.in $(PIP_DEPENDENCY_DIR)/requirements_blaze.txt.out $(PIP_DEPENDENCY_DIR)/requirements_talib.txt
	pip-compile --output-file=$@ ${ARGS} $^

# All `pip` dependency files depend on their corresponding `.in` file and the base `requirements.in`.
#$(PIP_DEPENDENCY_DIR)/requirements_%.txt.out: $(PIP_DEPENDENCY_DIR)/requirements_%.in $(PIP_DEPENDENCY_DIR)/requirements.txt.out
#	CUSTOM_COMPILE_COMMAND="make -C pip_compile etc" pip-compile --output-file=$@ ${ARGS} $^
