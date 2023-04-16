SHEDSKIN_LIBDIR=/home/ubuntu/.local/lib/python3.10/site-packages/shedskin/lib
CC=g++
CCFLAGS=-O2 -std=c++17 -march=native -Wno-deprecated $(CPPFLAGS) -I. -I${SHEDSKIN_LIBDIR}
LFLAGS=-lgc -lgccpp $(LDFLAGS) -lutil

CPPFILES=/media/ubuntu/Windows/Users/tzema/Documents/GitHub/pyfs/fs.cpp \
	${SHEDSKIN_LIBDIR}/sys.cpp \
	${SHEDSKIN_LIBDIR}/struct.cpp \
	${SHEDSKIN_LIBDIR}/stat.cpp \
	${SHEDSKIN_LIBDIR}/os/path.cpp \
	${SHEDSKIN_LIBDIR}/os/__init__.cpp \
	${SHEDSKIN_LIBDIR}/builtin.cpp

HPPFILES=/media/ubuntu/Windows/Users/tzema/Documents/GitHub/pyfs/fs.hpp \
	${SHEDSKIN_LIBDIR}/sys.hpp \
	${SHEDSKIN_LIBDIR}/struct.hpp \
	${SHEDSKIN_LIBDIR}/stat.hpp \
	${SHEDSKIN_LIBDIR}/os/path.hpp \
	${SHEDSKIN_LIBDIR}/os/__init__.hpp \
	${SHEDSKIN_LIBDIR}/builtin.hpp

all:	fs

fs:	$(CPPFILES) $(HPPFILES)
	$(CC)  $(CCFLAGS) $(CPPFILES) $(LFLAGS) -o fs

fs_prof:	$(CPPFILES) $(HPPFILES)
	$(CC) -pg -ggdb $(CCFLAGS) $(CPPFILES) $(LFLAGS) -o fs_prof

fs_debug:	$(CPPFILES) $(HPPFILES)
	$(CC) -g -ggdb $(CCFLAGS) $(CPPFILES) $(LFLAGS) -o fs_debug

clean:
	rm -f fs fs_prof fs_debug

.PHONY: all clean

