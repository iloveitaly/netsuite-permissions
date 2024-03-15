.PHONY: setup generate

SHELL = zsh

setup:
	if ! brew list csvkit > /dev/null; then \
		brew install csvkit; \
	fi

	pip install lxml pandas html5lib beautifulsoup4

# - for all sheets
# TODO change columna to notes
generate: setup
	in2csv --write-sheets "-" -f xls ./NetSuitePermissionsUsage_2024.1.xls

RAW_CATALOG_JSON ?= data/raw_record_catalog.json
CATALOG_JSON ?= data/record_catalog.json
ENRICHED_CATALOG_JSON ?= data/enriched_record_catalog.json
TIM_TABLE_JSON ?= data/tim_table.json

# output files
OUTPUT_CATALOG_CSV ?= output/netsuite_record_catalog.csv
OUTPUT_TIM_TABLE_CSV ?= output/tim_table.csv

$(ENRICHED_CATALOG_JSON):
	@if [ -z "$$NETSUITE_ACCOUNT" ]; then \
			echo "NETSUITE_ACCOUNT is not set"; \
			exit 1; \
	fi

	@if [ -z "$$NETSUITE_COOKIE" ]; then \
			echo "NETSUITE_COOKIE is not set"; \
			exit 1; \
	fi

	@http GET https://$$NETSUITE_ACCOUNT.app.netsuite.com/app/recordscatalog/rcendpoint.nl action==getRecordTypes data=='{"structureType":"FLAT"}' "Cookie: $(NETSUITE_COOKIE)" > $(RAW_CATALOG_JSON) | \
		zq -f json -o $(RAW_CATALOG_JSON) 'yield data | over this | where not grep(/^CUSTOMLIST/, id) | where not grep(/^CUSTOMRECORD/, id) | collect(this)' -

	@zq -f json -o $(CATALOG_JSON) 'over this | yield {id,label:grep("Missing label", this.label) ? null : this.label} | collect(this)' $(RAW_CATALOG_JSON)
	@python records_catalog.py $(CATALOG_JSON) > $(ENRICHED_CATALOG_JSON)

$(TIM_TABLE_JSON):
	@python tim_table.py > $(TIM_TABLE_JSON)

# normalize the tim table to same columns as the netsuite catalog
$(OUTPUT_TIM_TABLE_CSV): $(TIM_TABLE_JSON)
	zq -f csv -o $(OUTPUT_TIM_TABLE_CSV) 'over this | yield {tableName:this["Table Name"],tableId:this["Table ID"],permission:this["Permission Needed"]}' $(TIM_TABLE_JSON)

$(OUTPUT_CATALOG_CSV): $(ENRICHED_CATALOG_JSON)
	@zq -f csv -o $(OUTPUT_CATALOG_CSV) -I netsuite_catalog_simplify.zed $(ENRICHED_CATALOG_JSON)

all:
	@$(MAKE) $(OUTPUT_CATALOG_CSV)
	@$(MAKE) $(OUTPUT_TIM_TABLE_CSV)
