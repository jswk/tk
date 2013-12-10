%option noyywrap

%{
#include "transform.tab.hh"
#include <string>

std::string strbody;
bool comment;
bool bcomment;
bool string_decl;
int parens;

%}

%x BODY_BLOCK

%%
void|char|short|int|long|float  yylval.str = strdup(yytext); return TYPE;
struct|enum                     yylval.str = strdup(yytext); return STRUCTURE;
[a-zA-Z][a-zA-Z0-9_]*           yylval.str = strdup(yytext); return ID;
[0-9]+                          yylval.number = atoi(yytext); return NUM;
[ \t\n]+  /* eat up whitespaces */
"{"                             {BEGIN(BODY_BLOCK);
                                parens = 0;
                                comment = false;
                                string_decl = false;
                                strbody = yytext;}
.                               return(*yytext);
<BODY_BLOCK>\"                   {
                                    if (!comment) {
                                        string_decl = !string_decl;
                                    }
                                    strbody += yytext;
                                }
<BODY_BLOCK>\\\"              strbody += yytext;
<BODY_BLOCK>"/*"                {
                                    if (!string_decl) {
                                        comment = true;
                                        bcomment = true;
                                    }
                                    strbody += yytext;
                                }
<BODY_BLOCK>"*/"                comment = false; strbody += yytext;
<BODY_BLOCK>"//"                {
                                    if (!string_decl) {
                                        comment = true;
                                        bcomment = false;
                                    }
                                    strbody += yytext;
                                }
<BODY_BLOCK>"{"                 if (!comment && !string_decl) parens++; strbody += yytext;
<BODY_BLOCK>"}"                 {
                                    strbody += yytext;
                                    if (!comment && !string_decl) {
                                        if (parens > 0) {
                                            parens--;
                                        } else {
                                            BEGIN(INITIAL); yylval.str = (char*) strbody.c_str(); return BODY;
                                        }
                                    }
                                }
<BODY_BLOCK>\n                 if (!bcomment) comment = false; strbody += yytext;
<BODY_BLOCK>.                  strbody += yytext;
