install:
	uv pip install -r requirements.txt

run-local:
	uv run src/main_local.py "$(FILE)" "$(DOCID)"

run-azure:
	uv run src/main_azure.py "$(FILE)" "$(DOCID)"
