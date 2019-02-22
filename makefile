CFLAGS = -g

run: build
	./valgreen ./ejemplo

build: ejemplo pipinstall

pipinstall: valgreen
	pip3 install .
