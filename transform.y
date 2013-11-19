%{
#include <stdio.h>
%}

%union {
  char *str;
};

%type <str> declarator 
%type <str> decl_specifier
%type <str> function

%token <str> TYPE
%token <str> STRUCTURE
%token <str> ID

%%

functions           :
                    |  functions function
                    |  function { printf("Znalazlem funkcje %s\n", $1); }
	                  ;

function            :  decl_specifier declarator { printf("Funkcja %s -> %s\n", $1, $2); }
                    |  declarator { printf("Znaleziono deklarator %s\n", $1); }
                		;

decl_specifier      :  TYPE { printf("Znaleziono typ %s\n", $1); }
                    |  STRUCTURE ID { printf("Znaleziono struct %s, name %s\n", $1, $2); }
		                ;

declarator          :  pointer direct_declarator
                    |  direct_declarator
                    ;

direct_declarator   :  ID
                    ;

pointer             :  pointer '*'
                    |  '*'
                    ;  

%%

int yyerror(char *s) {
  printf("blad: %s\n", s);
}

int main()
{
  yyparse();
  return 0;
}
