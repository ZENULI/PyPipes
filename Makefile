all:
    # install tools locally
	python setup.py build_ext --inplace
	rm -rf build

install:
	# install tools
	python setup.py build_ext install
	rm -rf build