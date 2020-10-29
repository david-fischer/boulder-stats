.PHONY: docs

help:
	@#echo "test - run the test py.test suite"
#	@echo "coverage - generate a coverage report and open it"
	@echo "docs - generate Sphinx HTML documentation and open it"
	@echo "rpi_push - transfer project folder to raspberry pi via ssh"

#test:
#	python setup.py test

# coverage:
#	 python setup.py test -a '--cov={{cookiecutter.repo_name}} --cov-report=html'
#	 xdg-open htmlcov/index.html

docs:
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	xdg-open docs/_build/html/index.html

rpi_push:
	ssh pi@nextcloudpi.local mv /home/pi/boulder-stats "/home/pi/bs_$(shell date +%F_%T)"
	scp -r ${CURDIR} pi@nextcloudpi.local:/home/pi/boulder-stats

update_readme:
	python .utils/render_readme.py
	git commit README.md -m "update: README"
	git push origin master

docker:
	sudo docker build -t boulder . -f Dockerfile

run_docker:
	sudo docker run --rm -d -v boulder_vol:/boulder-stats/ -t boulder:latest bot start
	sudo docker run --rm -d -v boulder_vol:/boulder-stats/ -t boulder:latest data schedule
