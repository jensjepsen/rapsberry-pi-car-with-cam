PYTHON=$(shell echo `pwd`/venv/bin/python)
PIP=$(shell echo `pwd`/venv/bin/pip)
venv/touchfile: src/requirements.txt
	python -m venv --system-site-packages venv
	$(PIP) install -r src/requirements.txt
	touch venv/touchfile

run: venv/touchfile
	cd src && $(PYTHON) -m uvicorn "app:app" --host 0.0.0.0 --port 8881 --reload
	