# Turn echoing commands off
.SILENT:

PROJECT_PACKAGE=asyncdynamo

clean:
	echo "Cleaning up build and *.pyc files..."
	find . -name '*.pyc' -exec rm -rf {} \;
	rm -rf build

functional: clean
	echo "Running asyncdynamo functional tests..."
	export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/$PROJECT_PACKAGE  &&  \
		nosetests -s --verbose --with-coverage --cover-package=$PROJECT_PACKAGE tests/functional/*