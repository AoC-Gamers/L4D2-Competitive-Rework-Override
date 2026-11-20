.DEFAULT_GOAL := help

ifeq ($(OS),Windows_NT)
PYTHON ?= python
SMX_PLATFORM ?= windows
SPCOMP_NAME := spcomp.exe
else
PYTHON ?= $(shell command -v python3 >/dev/null 2>&1 && echo python3 || echo python)
SMX_PLATFORM ?= linux
SPCOMP_NAME := spcomp
endif

SOURCEMOD_VERSION ?= 1.12
SPCOMP ?= .deps/smx/sourcemod-$(SMX_PLATFORM)/addons/sourcemod/scripting/$(SPCOMP_NAME)
SMX_BUILD_DIR ?= .build/smx
SMX_PACKAGE_DIR ?= .build/package-smx
SMX_COMPILE_LOG ?= .build/build-smx-compile.log
SOURCEMOD_ARTIFACT_DIR ?= dist/sourcemod/artifact
RELEASE_BASENAME ?= l4d2-competitive-rework-override-local

.PHONY: help deps-smx build-smx package-smx stage-smx release validate-artifact clean clean-all
help:
	@$(PYTHON) -c "print('deps-smx, build-smx, package-smx, release, validate-artifact, clean, clean-all')"

deps-smx:
	$(PYTHON) scripts/deps/fetch-sourcemod.py --root . --platform "$(SMX_PLATFORM)" --version "$(SOURCEMOD_VERSION)"

build-smx:
	$(PYTHON) scripts/build/build-local.py --root . --spcomp "$(SPCOMP)" --output-root "$(SMX_BUILD_DIR)" --compile-log "$(SMX_COMPILE_LOG)"

package-smx:
	$(PYTHON) scripts/package/stage-artifact.py . "$(SMX_BUILD_DIR)" "$(SMX_COMPILE_LOG)" "$(SMX_PACKAGE_DIR)"

stage-smx:
	$(PYTHON) scripts/package/stage-artifact.py . "$(SMX_PACKAGE_DIR)" "$(SMX_COMPILE_LOG)" "$(SOURCEMOD_ARTIFACT_DIR)"

release: stage-smx
	$(PYTHON) scripts/package/package-release.py --root . --artifact "$(SOURCEMOD_ARTIFACT_DIR)" --basename "$(RELEASE_BASENAME)"

validate-artifact:
	$(PYTHON) scripts/package/artifact_contract.py --root . --artifact "$(SOURCEMOD_ARTIFACT_DIR)"

clean:
	$(PYTHON) -c "import shutil; shutil.rmtree('.build', ignore_errors=True); shutil.rmtree('dist', ignore_errors=True)"

clean-all: clean
	$(PYTHON) -c "import shutil; shutil.rmtree('.deps', ignore_errors=True)"
