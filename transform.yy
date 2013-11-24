%{
#include <cstdio>
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <sstream>

extern "C"  {int yyparse(void); int yywrap() { return 1; }}

using namespace std;

int yylex(void); 
int yyerror(const char* s); 


struct declarator {
  declarator(int type) : type(type), next(NULL), param_list(NULL), identifier_list(NULL) {}
  struct wrappedstring *id;
  int type;
  struct wrappedstring *decl_specifier;
  struct wrappedstring *pointer;
  struct declarator *next;
  int array;
  struct param_list *param_list;
  struct identifier_list *identifier_list;
};

struct function {
  function() : decl_specifier(NULL), declarator(NULL), declarations(NULL) {}
  struct wrappedstring *decl_specifier;
  struct declarator *declarator;
  struct declaration_list* declarations; // map parameter name to type
  vector<string> parameters;
  char* body;
};

struct identifier_list {
  vector<string> identifiers;
};

struct declarator_list {
  vector<struct declarator*> declarators;
  struct wrappedstring* decl_specifier;
};

struct declaration_list {
  declaration_list() : duplicate(false) {}
  map<string, string> declarations;
  bool duplicate;
};

struct param_list {
  set<string> param_names;
  vector<struct param_declaration *> declarations;
};

struct wrappedstring {
  wrappedstring(const char *val) : value(val) {}
  wrappedstring(string val) : value(val) {}
  string value;
};

struct param_declaration {
  struct wrappedstring *decl_specifier;
  struct declarator *declarator;
};

vector<function *> functions;

string getDeclarationString(struct declarator* decl, struct wrappedstring* decl_specifier) {
    string out;
    struct declarator* curr = decl;
    ostringstream oss;
    
    out += decl_specifier->value;
    out += " ";
    while (curr != NULL) {
        bool del = false;
        switch (curr->type) {
            case 0:
                if (curr->pointer != NULL) {
                    out += curr->pointer->value;
                }
                out += curr->id->value;
            break;
            case 1:
                if (curr->array == -1) {
                    out += "[]";
                } else {
                    oss << curr->array;
                    out += '[';
                    out += oss.str();
                    out += ']';
                    oss.flush();
                }
            break;
            case 2:
                out += " (";
                for (vector<struct param_declaration*>::iterator it = curr->param_list->declarations.begin(); it != curr->param_list->declarations.end(); ++it) {
                    if (del) out += ", ";
                    out += getDeclarationString((*it)->declarator, (*it)->decl_specifier);
                    del = true;
                }
                out += ")";
            break;
            case 3:
                // this should throw syntax error or something
            break;
        }
        curr = curr->next;
    }

    return out;
}

string getParamListAsString(struct param_list *param_list) {
  string out = "";
  for (vector<struct param_declaration *>::iterator declaration = param_list->declarations.begin(); declaration != param_list->declarations.end(); ++declaration) {
    out += getDeclarationString((*declaration)->declarator, (*declaration)->decl_specifier);
    out += ", ";
  }
  return out.substr(0, out.size() - 2); // remove last ,_ from out
}

void handleFunction(struct function* func) {
    printf("Funkcja %s %s\n", func->decl_specifier->value.c_str(), func->declarator->id->value.c_str());
    cout << getDeclarationString(func->declarator, func->decl_specifier) << endl;
 //   map<string, string>* mp = &func->declarations->declarations;
 //   map<string, string>::iterator it;
 //   for (it = mp->begin(); it != mp->end(); ++it) {
 //       cout << it->first << ":" << it->second << "\n";
 //   }
    cout << func->body << '\n';
}

%}

%union {
  char *str;
  struct wrappedstring *nstr;
  struct function *function;
  struct declarator *declarator;
  struct declarator_list *declarator_list;
  struct declaration_list *declaration_list;
  struct identifier_list *identifier_list;
  struct param_list *param_list;
  struct param_declaration *param_declaration;
  int number;
};

%type <declarator> declarator
%type <declarator_list> declarator_list
%type <declarator_list> declaration
%type <declaration_list> declaration_list
%type <nstr> decl_specifier
%type <function> function
%type <declarator> direct_declarator
%type <nstr> pointer
%type <param_list> param_list
%type <identifier_list> identifier_list
%type <str> body
%type <param_declaration> param_declaration
%type <nstr> abstract_declarator
%type <nstr> direct_abstract_declarator

%token <str> TYPE
%token <str> STRUCTURE
%token <str> ID
%token <str> BODY
%token <number> NUM

%%
functions           :
                    |  functions function {
                        functions.push_back($2); 
                        handleFunction($2);
                    }
                    |  function { 
                        functions.push_back($1); 
                        handleFunction($1);
                    }
                    ;

function            :  decl_specifier declarator declaration_list body { 
                        $$ = new function();
                        $$->decl_specifier = $1;
                        $$->declarator = $2;
                        $$->declarations = $3;
                        $$->body = $4;
                    }
                    |  decl_specifier declarator body { 
                        $$ = new function();
                        $$->decl_specifier = $1;
                        $$->declarator = $2;
                    }
                    |  declarator declaration_list body { 
                        $$ = new function();
                        $$->decl_specifier = new wrappedstring("void");
                        $$->declarator = $1;
                        $$->declarations = $2;
                    }
                    |  declarator body { 
                        $$ = new function();
                        $$->decl_specifier = new wrappedstring("void");
                        $$->declarator = $1;
                    }
                		;

decl_specifier      :  TYPE { $$ = new wrappedstring($1); }
                    |  STRUCTURE ID { $$ = new wrappedstring($1); $$->value.append(" "); $$->value.append($2); }
		                ;

declaration_list    :  declaration_list declaration {
                        $$ = $1;

                        pair<map<string,string>::iterator,bool> ret;
                        for (vector<struct declarator*>::iterator it = $2->declarators.begin(); it != $2->declarators.end(); ++it) {
                            ret = $$->declarations.insert(pair<string,string>((*it)->id->value, getDeclarationString(*it, $2->decl_specifier)));
                            if (ret.second == false) {
                                $$->duplicate = true;
                            }
                        }
                    }
                    |  declaration {
                        $$ = new declaration_list();

                        pair<map<string,string>::iterator,bool> ret;
                        for (vector<struct declarator*>::iterator it = $1->declarators.begin(); it != $1->declarators.end(); ++it) {
                            ret = $$->declarations.insert(pair<string,string>((*it)->id->value, getDeclarationString(*it, $1->decl_specifier)));
                            if (ret.second == false) {
                                $$->duplicate = true;
                            }
                        }
                    }

declaration         :  decl_specifier declarator_list ';' {
                        $$ = $2;
                        $$->decl_specifier = $1;
                    }

declarator_list     :  declarator ',' declarator_list {
                        $$ = $3;
                        $$->declarators.push_back($1);
                    }
                    |  declarator {
                        $$ = new declarator_list();
                        $$->declarators.push_back($1);
                    }

declarator          :  pointer direct_declarator { $$ = $2; $$->pointer = $1; }
                    |  direct_declarator
                    ;

direct_declarator   :  ID {
                        $$ = new declarator(0);
                        $$->id = new wrappedstring($1);
                    }
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

param_list          :  param_list ',' param_declaration {
                        $1->declarations.push_back($3);

                    }
                    |  param_declaration {
                        $$ = new param_list();
                        $$->declarations.push_back($1);
                    }
                    ;

param_declaration   :  decl_specifier declarator {
                        $$ = new param_declaration();
                        $$->decl_specifier = $1;
                        $$->declarator = $2;
                    }
                    |  decl_specifier abstract_declarator
                    |  decl_specifier {
                        $$ = new param_declaration();
                        $$->decl_specifier = $1;
                        $$->declarator = NULL;
                    }
                    ;

abstract_declarator :  pointer
                    |  pointer direct_abstract_declarator {
                        $$ = new wrappedstring("");
                        $$->value.append($1->value);
                        $$->value.append($2->value);
                    }
                    |  direct_abstract_declarator
                    ;

direct_abstract_declarator  :  '(' abstract_declarator ')' {
                                $$ = new wrappedstring("(");
                                $$->value.append($2->value);
                                $$->value.append(")");
                            }
                            |  direct_abstract_declarator '[' NUM ']' {
                                char number[256];
                                sprintf(number, "%d", $3);
                                $1->value.append("[");
                                $1->value.append(number);
                                $1->value.append("]");
                            }
                            |  '[' NUM ']' {
                                char number[256];
                                sprintf(number, "%d", $2);
                                $$ = new wrappedstring("[");
                                $$->value.append(number);
                                $$->value.append("]");
                            }
                            |  direct_abstract_declarator '(' param_list ')' {
                                $1->value.append("(");
                                $1->value.append(getParamListAsString($3));
                                $1->value.append(")");
                            }
                            |  direct_abstract_declarator '[' ']' {
                                $1->value.append("[]");
                            }
                            |  direct_abstract_declarator '(' ')' {
                                $1->value.append("()");
                            }
                            |  '(' param_list ')' {
                                $$ = new wrappedstring("(");
                                $$->value.append(getParamListAsString($2));
                                $$->value.append(")");
                            }
                            |  '(' ')' {
                                $$ = new wrappedstring("()");
                            }
                            ;

pointer             :  pointer '*' { $1->value.append("*"); }
                    |  '*' { $$ = new wrappedstring("*"); }
                    ;

body                :  BODY 
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

 // for (vector<function *>::iterator iter = functions.begin(); iter != functions.end(); ++iter)
 // {
 //   function *fun = *iter;
 //   if (fun->decl_specifier == NULL) { cout << "int "; }
 //   else { cout << fun->decl_specifier->value << " "; }
 //   cout << fun->declarator->id->value;

 //   bool old_style = true;
 //   declarator *param_list_declarator = find_declarator_of_type(fun->declarator, 2);
 //   old_style = param_list_declarator == NULL;

 //   struct declaration_list *declaration_list = fun->declarations;
 //   bool declarations_present = declaration_list != NULL;


 //   if (old_style) {
 //     cout << "Old style";
 //   }

 //   if (!old_style && declarations_present) {
 //     cerr << "Warning: New style function with declaration list present" << endl;
 //   }

 //   cout << endl;
 // }

  return 0;
}
