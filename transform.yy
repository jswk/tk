%{
#include <cstdio>
#include <iostream>
#include <string>
#include <vector>
#include <map>

extern "C"  {int yyparse(void); int yywrap() { return 1; }}

using namespace std;

int yylex(void); 
int yyerror(const char* s); 


struct declarator {
  declarator(int type) : type(type), next(NULL), param_list(NULL), identifier_list(NULL) {}
  const char *id;
  int type;
  int pointer;
  struct declarator* next;
  int array;
  struct param_list* param_list;
  struct identifier_list* identifier_list;
};

struct declaration {
  declaration() : next(NULL), declarator(NULL) {}
  struct wrappedstring *decl_specifier;
  struct declarator *declarator;
  struct declaration *next;
};

struct function {
  function() : decl_specifier(NULL), declarator(NULL), declaration(NULL) {}
  struct wrappedstring *decl_specifier;
  struct declarator *declarator;
  struct declaration *declaration;
  const char *body;
  map<string, string> parameter_declarations; // map parameter name to type
  vector<string> parameters;
};

struct identifier_list {
  vector<string> identifiers;
};

struct param_list {

};

struct wrappedstring {
  wrappedstring(const char *val) : value(val) {}
  string value;
};

vector<function *> functions;

%}

%union {
  char *str;
  struct wrappedstring *nstr;
  struct function *function;
  struct declarator *declarator;
  struct declaration *declaration;
  struct identifier_list *identifier_list;
  struct param_list *param_list;
  int number;
};

%type <declarator> declarator 
%type <nstr> decl_specifier
%type <function> function
%type <declarator> direct_declarator
%type <declarator> declarator_list
%type <declaration> declaration
%type <declaration> declaration_list
%type <nstr> direct_abstract_declarator
%type <nstr> pointer
%type <param_list> param_list
%type <identifier_list> identifier_list

%token <str> TYPE
%token <str> STRUCTURE
%token <str> ID
%token <str> BODY
%token <number> NUM

%%
functions           :
                    |  functions function { functions.push_back($2); }
                    |  function { functions.push_back($1); }
                    ;

function            :  decl_specifier declarator declaration_list body { 
                        printf("Funkcja %s %s\n", $1->value.c_str(), $2->id); 
                        $$ = new function();
                        $$->decl_specifier = $1;
                        $$->declarator = $2;
                    }
                    |  decl_specifier declarator body { 
                        printf("Funkcja %s %s\n", $1->value.c_str(), $2->id);
                        $$ = new function();
                        $$->decl_specifier = $1;
                        $$->declarator = $2;
                    }
                    |  declarator declaration_list body { 
                        printf("3\n"); 
                        $$ = new function();
                        $$->decl_specifier = NULL;
                        $$->declarator = $1;
                    }
                    |  declarator body { 
                        printf("Znaleziono deklarator %s\n", $1->id); 
                        $$ = new function();
                        $$->decl_specifier = NULL;
                        $$->declarator = $1;
                    }
                		;

decl_specifier      :  TYPE { $$ = new wrappedstring($1); }
                    |  STRUCTURE ID { $$ = new wrappedstring($1); $$->value.append(" "); $$->value.append($2); }
		                ;

declaration_list    :  declaration_list declaration { $1->next = $2; }
                    |  declaration 
                    ;

declaration         :  decl_specifier declarator_list ';' { 
                        $$ = new declaration(); 
                        $$->decl_specifier = $1;
                        $$->declarator = $2;
                      }
                    |  decl_specifier ';' {
                        $$ = new declaration();
                        $$->decl_specifier = $1;
                      }
                    ;

declarator_list     :  declarator ',' declarator_list {
                        $1->next = $3;
                      }
                    |  declarator

declarator          :  pointer direct_declarator 
                    |  direct_declarator
                    ;

direct_declarator   :  ID { $$ = new declarator(0); $$->id = $1; }
                    |  '(' declarator ')' { $$ = $2; }
                    |  direct_declarator '[' NUM ']' { 
                    $1->next = new declarator(1);
                    $1->next->array = $3; 
                    }
                    |  direct_declarator '[' ']' {
                    $1->next = new declarator(1);
                    $1->next->array = -1;
                    }
                    |  direct_declarator '(' param_list ')' {
                    $1->next = new declarator(2);
                    $1->next->param_list = $3;
                    }
                    |  direct_declarator '(' identifier_list ')' { 
                    $1->next = new declarator(3);
                    $1->next->identifier_list = $3;
                    }
                    |  direct_declarator '(' ')' {
                    $1->next = new declarator(3);
                    }
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

struct declarator *find_declarator_of_type(struct declarator *first, int type) {
  declarator *current = first;
  while (current != NULL) {
    if (current->type == type) {
      return current;
    }
    current = current->next;
  }
  return NULL;
}

int yyerror(const char *s) {
  printf("blad: %s\n", s);
}

int main()
{
  yyparse();

  for (vector<function *>::iterator iter = functions.begin(); iter != functions.end(); ++iter)
  {
    function *fun = *iter;
    if (fun->decl_specifier == NULL) { cout << "int "; }
    else { cout << fun->decl_specifier->value << " "; }
    cout << fun->declarator->id;

    bool old_style = true;
    declarator *param_list_declarator = find_declarator_of_type(fun->declarator, 2);
    old_style = param_list_declarator == NULL;

    if (old_style) {
      cout << "Old style";
    }

    cout << endl;
  }

  return 0;
}
