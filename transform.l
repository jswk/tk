%option noyywrap

%{
#include "transform.tab.h"
%}

%%
void|char|short|int|long|float  yylval.str = strdup(yytext); return TYPE;
struct|enum                     yylval.str = strdup(yytext); return STRUCTURE;
[a-zA-Z][a-zA-Z0-9_]*           yylval.str = strdup(yytext); return ID;
[0-9]+                          yylval.num = atoi(yytext); return NUM;
[ \t]+  /* eat up whitespaces */
.|\n    return(*yytext);
