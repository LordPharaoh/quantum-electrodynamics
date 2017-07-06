CC = gcc
SWIG = swig
SWIG_DIR = swig/
SRC = src/
INCLUDE = -Iinclude/
VECTOR_INTERFACES = $(SWIG_DIR)/vector.i
CIRCLE_INTERFACES = $(SWIG_DIR)/circle.i
PYTHON = -I/usr/include/python2.7/
BUILD = build/
SOURCES = $(shell find $(SRC) -name '*.c')

SWIG_CFLAGS = -c -fPIC

all: binary

binary:
	$(CC) $(INCLUDE) $(PYTHON) $(SOURCES) -o vecout -lm

vector:
	$(SWIG) -python $(VECTOR_INTERFACES)
	mv $(SWIG_DIR)/vector_wrap.c $(BUILD)
	mv $(SWIG_DIR)/vector.py .
	$(CC) $(SWIG_CFLAGS) $(INCLUDE) $(PYTHON) $(BUILD)/vector_wrap.c $(SRC)/vector.c $(SRC)/except.c
	mv *.o build
	gcc -shared build/*.o -o _vector.so

circle:
	$(SWIG) -python $(CIRCLE_INTERFACES)
	mv $(SWIG_DIR)/circle_wrap.c $(BUILD)
	mv $(SWIG_DIR)/circle.py .
	$(CC) $(SWIG_CFLAGS) $(INCLUDE) $(PYTHON) $(BUILD)/circle_wrap.c $(SRC)/circle.c $(SRC)/except.c $(SRC)/vector.c
	mv *.o build
	gcc -shared build/*.o -o _circle.so

clean:
	rm build/*
