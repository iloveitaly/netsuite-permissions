SHELL = zsh

setup:
	if ! brew list csvkit > /dev/null; then \
		brew install csvkit; \
	fi

# - for all sheets
generate: setup
	in2csv --write-sheets "-" -f xls ./NetSuitePermissionsUsage_2024.1.xls