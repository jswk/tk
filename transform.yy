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

struct direct_declarator {
  
};

struct function {
  struct decl_specifier *decl_specifier;
  map<string, string> parameter_declarations; // map parameter name to type
  vector<string> parameters;
};

struct function current_function;

struct identifier_list {
  vector<string> identifiers;
};

struct wrappedstring {
  wrappedstring(const char *val) : value(val) {}
  string value;
};

%}

%union {
  char *str;
  struct wrappedstring *nstr;
  struct node *nd;
  struct identifier_list *identifier_list;
};

%type <str> declarator 
%type <nstr> decl_specifier
%type <str> function
%type <nd> direct_declarator
%type <nstr> direct_abstract_declarator
%type <nstr> pointer
%type <identifier_list> identifier_list

%token <str> TYPE
%token <str> STRUCTURE
%token <str> ID
%token <str> BODY
%token <str> NUM

%%
functions           :
                    |  function 
                    ;

function            :  decl_specifier declarator declaration_list body { printf("Funkcja %s %s\n", $1->value.c_str(), $2); $$ = $2; }
                    |  decl_specifier declarator body { printf("Funkcja %s %s\n", $1->value.c_str(), $2); $$ = $2; }
                    |  declarator declaration_list body { printf("3\n"); }
                    |  declarator body { printf("Znaleziono deklarator %s\n", $1); }
                		;

decl_specifier      :  TYPE { $$ = new wrappedstring($1); }
                    |  STRUCTURE ID { $$ = new wrappedstring($1); $$->value.append(" "); $$->value.append($2); }
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
                    |  direct_declarator '(' identifier_list ')' { 
                      printf("Found identifier list: \n");
                      for (int i = 0; i < $3->identifiers.size(); ++i) {
                        printf("%s\n", $3->identifiers[i].c_str());
                      }
                    }
                    |  direct_declarator '(' ')'
                    ;

identifier_list     :  identifier_list ',' ID { $1->identifiers.push_back($3); }
                    |  ID { $$ = new identifier_list(); $$->identifiers.push_back($1); }
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

body                :  BODY { printf("Body\n"); }
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
