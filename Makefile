build: docker/images

BOOKGROUP_IMAGE=bookgroup
BOOKGROUP_JUPYTER=bookgroup_jupyter

images:
	docker build -t $(BOOKGROUP_IMAGE) -f docker/Dockerfile .
	docker build -t $(BOOKGROUP_JUPYTER) -f docker/Dockerfile.jupyter .

bash:
	docker run --rm -v $(PWD):/src  -it $(BOOKGROUP_IMAGE) bash

jupyter:
	docker run --rm -v $(PWD):/src -p 8978:8978 $(BOOKGROUP_JUPYTER) jupyter notebook --allow-root --port=8978 --ip 0.0.0.0 --no-browser

bash-jupyter:
	docker exec   -it $(BOOKGROUP_JUPYTER) bash

download-datasets:
	docker run --rm -v $(PWD):/src  -it $(BOOKGROUP_IMAGE) python chapter2/download.py
