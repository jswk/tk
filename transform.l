%option noyywrap

%{
#include "transform.tab.hh"
%}

%%
void|char|short|int|long|float  yylval.str = strdup(yytext); return TYPE;
struct|enum                     yylval.str = strdup(yytext); return STRUCTURE;
[a-zA-Z][a-zA-Z0-9_]*           yylval.str = strdup(yytext); return ID;
[0-9]+                          yylval.str = strdup(yytext); return NUM;
[ \t\n]+  /* eat up whitespaces */
.                               return(*yytext);
"{".*"}"                          yylval.str = strdup(yytext); return BODY;
