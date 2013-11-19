all: transform

transform: transform.tab.c lex.yy.c
	$(CC) -o transform transform.tab.c lex.yy.c

transform.tab.c:
	bison -d transform.y

lex.yy.c:
	flex transform.l

clean:
	rm -Rf transform.tab.c lex.yy.c transform
