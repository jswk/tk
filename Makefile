all: transform

transform: transform.tab.cc lex.yy.c
	$(CXX) -o transform transform.tab.cc lex.yy.c

transform.tab.cc: transform.yy
	bison -d transform.yy

lex.yy.c: transform.l
	flex transform.l

clean:
	rm -Rf transform.tab.cc transform.tab.hh lex.yy.c transform
