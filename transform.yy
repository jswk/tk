%{
#include <stdio.h>
#include <string>
#include <vector>
#include <map>

extern "C"  {int yyparse(void); int yywrap() { return 1; }}

using namespace std;

int yylex(void); 
int yyerror(const char* s); 

typedef struct node {
  string value;
  vector<struct node *> children;
} *pnode;

struct decl_specifier {
  decl_specifier() : type(0), structure(0), structure_id(0) {}
  char *type;
  char *structure;
  char *structure_id;
};

struct direct_declarator {
  
};

struct function {
  struct decl_specifier *decl_specifier;
  map<string, string> parameter_declarations; // map parameter name to type
  vector<string> parameters;
};

struct function current_function;

struct wrappedstring {
  wrappedstring(const char *val) : value(val) {}
  string value;
};

%}

%union {
  char *str;
  struct wrappedstring *nstr;
  struct node *nd;
  struct decl_specifier *decl_spec;
};

%type <str> declarator 
%type <decl_spec> decl_specifier
%type <str> function
%type <nd> direct_declarator
%type <nstr> direct_abstract_declarator
%type <nstr> pointer

%token <str> TYPE
%token <str> STRUCTURE
%token <str> ID
%token <str> BODY
%token <str> NUM

%%
functions           :
                    |  function 
                    ;

function            :  decl_specifier declarator declaration_list body { printf("Funkcja %s %s %s -> %s\n", $1->type, $1->structure, $1->structure_id, $2); $$ = $2; }
                    |  decl_specifier declarator body { printf("Funkcja %s %s %s -> %s\n", $1->type, $1->structure, $1->structure_id, $2); $$ = $2; }
                    |  declarator declaration_list body { printf("3\n"); }
                    |  declarator body { printf("Znaleziono deklarator %s\n", $1); }
                		;

decl_specifier      :  TYPE { $$ = new decl_specifier(); $$->type = $1; }
                    |  STRUCTURE ID { $$ = new decl_specifier(); $$->structure = $1; $$->structure_id = $2; }
		                ;

declaration_list    :  declaration_list declaration
                    |  declaration

declaration         :  decl_specifier declarator_list ';'
                    |  decl_specifier ';'

declarator_list     :  declarator ',' declarator_list
                    |  declarator

declarator          :  pointer direct_declarator 
                    |  direct_declarator
                    ;

direct_declarator   :  ID { $$ = new node(); $$->value = $1; }
                    |  '(' declarator ')'
                    |  direct_declarator '[' NUM ']'
                    |  direct_declarator '[' ']'
                    |  direct_declarator '(' param_list ')'
                    |  direct_declarator '(' identifier_list ')'
                    |  direct_declarator '(' ')'
                    ;

identifier_list     :  ID ',' identifier_list { current_function.parameters.push_back($1); }
                    |  ID { current_function.parameters.push_back($1); }
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

pointer             :  pointer '*' { $1->value.append("*"); }
                    |  '*' { $$ = new wrappedstring("*"); }
                    ;

body                : BODY { printf("Body\n"); }
                    ;

%%

int yyerror(const char *s) {
  printf("blad: %s\n", s);
}

int main()
{
  yyparse();
  for (int i = 0; i < current_function.parameters.size(); ++i)
  {
    printf("p %s\n", current_function.parameters[i].c_str());
  }
  return 0;
}
