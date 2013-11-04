/* This is a program that translates ascii text into plain TeX
   output. */

#include <stdio.h>
#include <string.h>

int main ()
{
  int zero1 = 0;
  char c;
  int zero2 = 0;

  puts ("{\\tt");
  puts ("\\noindent");

  while ((c = getchar ()) != EOF)
    {
      switch (c)
	{
	case ' ':
	  printf ("{\\kern0.500em}");
	  break;
	case '\t':
	  printf ("{\\kern4.000em}");
	  break;
	case '\n':
	  puts ("\\hfill\n");
	  puts ("\\noindent");
	  break;
	default:
	  if (strstr ("\"^~#_%${}&\\", &c))
	    printf ("\\char%d", c);
	  else
	    putchar (c);
	  break;
	}
    }

  puts ("}");

  return 0;
}
