%{
#include <stdio.h>

%}

%union {
  char *str;
  int num;
};

%type <str> declarator 
%type <str> decl_specifier
%type <str> function
%type <str> direct_declarator

%token <str> TYPE
%token <str> STRUCTURE
%token <str> ID
%token <str> BODY
%token <num> NUM

%%

functions           :
                    |  functions function
                    |  function { printf("Znalazlem funkcje %s\n", $1); }
	                  ;

function            :  decl_specifier declarator declaration_list body { printf("Funkcja %s -> %s\n", $1, $2); }
                    |  decl_specifier declarator body { printf("2\n"); }
                    |  declarator declaration_list body { printf("3\n"); }
                    |  declarator body { printf("Znaleziono deklarator %s\n", $1); }
                		;

decl_specifier      :  TYPE { printf("Znaleziono typ %s\n", $1); }
                    |  STRUCTURE ID { printf("Znaleziono struct %s, name %s\n", $1, $2); }
		                ;

declaration_list    :  declaration_list declaration
                    |  declaration

declaration         :  decl_specifier declarator_list ';'
                    |  decl_specifier ';'

declarator_list     :  declarator ',' declarator_list
                    |  declarator

declarator          :  pointer direct_declarator { printf("* %s\n", $2); }
                    |  direct_declarator
                    ;

direct_declarator   :  ID
                    |  '(' declarator ')'
                    |  direct_declarator '[' NUM ']'
                    |  direct_declarator '[' ']'
                    |  direct_declarator '(' param_list ')'
                    |  direct_declarator '(' identifier_list ')'
                    |  direct_declarator '(' ')'
                    ;

identifier_list     :  ID ',' identifier_list
                    |  ID
                    ;

param_list          :  param_declaration ',' param_list
                    |  param_declaration
                    ;

param_declaration   :  decl_specifier declarator
                    |  decl_specifier abstract_declarator
                    |  decl_specifier
                    ;

abstract_declarator :  pointer
                    |  pointer direct_abstract_declarator
                    |  direct_abstract_declarator
                    ;

direct_abstract_declarator  :  '(' abstract_declarator ')'
                            |  direct_abstract_declarator '[' NUM ']'
                            |  '[' NUM ']'
                            |  direct_abstract_declarator '(' param_list ')'
                            |  direct_abstract_declarator '[' ']'
                            |  direct_abstract_declarator '(' ')'
                            |  '(' param_list ')'
                            |  '(' ')'
                            ;

pointer             :  pointer '*'
                    |  '*'
                    ;

body                : '{' '}' { printf("Body\n"); }
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
