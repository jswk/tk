all: transform

transform: transform.tab.cc lex.yy.c
	$(CXX) -o transform transform.tab.cc lex.yy.c

transform.tab.cc:
	bison -d transform.yy

lex.yy.c:
	flex transform.l

clean:
	rm -Rf transform.tab.cc transform.tab.hh lex.yy.c transform
