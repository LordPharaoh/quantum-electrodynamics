CC = gcc
SWIG = swig
SWIG_DIR = swig/
SRC = src/
INCLUDE = -Iinclude/
PYTHON = -I/usr/include/python2.7/
BUILD = build/
SOURCES = $(shell find $(SRC) -name '*.c')

SWIG_CFLAGS = -c -fPIC

all: binary vector circle calc_norm

binary:
	$(CC) $(INCLUDE) $(PYTHON) $(SOURCES) -o vecout -lm

vector:
	$(SWIG) -python $(SWIG_DIR)/vector.i
	mv $(SWIG_DIR)/vector_wrap.c $(BUILD)
	mv $(SWIG_DIR)/vector.py .
	$(CC) $(SWIG_CFLAGS) $(INCLUDE) $(PYTHON) $(BUILD)/vector_wrap.c $(SRC)/vector.c $(SRC)/except.c
	mv *.o build
	gcc -shared build/*.o -o _vector.so

circle:
	$(SWIG) -python $(SWIG_DIR)/circle.i
	mv $(SWIG_DIR)/circle_wrap.c $(BUILD)
	mv $(SWIG_DIR)/circle.py .
	$(CC) $(SWIG_CFLAGS) $(INCLUDE) $(PYTHON) $(BUILD)/circle_wrap.c $(SRC)/circle.c $(SRC)/except.c $(SRC)/vector.c
	mv *.o build
	gcc -shared build/*.o -o _circle.so

calc_norm:
	$(SWIG) -python $(SWIG_DIR)/calc_norm.i
	mv $(SWIG_DIR)/calc_norm_wrap.c $(BUILD)
	mv $(SWIG_DIR)/calc_norm.py .
	$(CC) $(SWIG_CFLAGS) $(INCLUDE) $(PYTHON) $(BUILD)/calc_norm_wrap.c $(SRC)/plane.c $(SRC)/circle.c $(SRC)/calc_norm.c $(SRC)/except.c $(SRC)/vector.c 
	mv *.o build
	gcc -shared build/*.o -o _calc_norm.so

clean:
	rm build/*
