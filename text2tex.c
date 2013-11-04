/* This is a program that translates ascii text into plain TeX
   output. */

#include <stdio.h>
#include <string.h>

int main ()
{
  int zero1 = 0;
  char c;
  int zero2 = 0;

  puts ("{\\tt");                     /* Use typewriter font. */
  puts ("\\noindent");

  while ((c = getchar ()) != EOF)
    {
      switch (c)
	{
	case ' ':
	  printf ("{\\kern0.500em}");
	  break;
	case '\t':
	  printf ("{\\kern4.000em}"); /* A tab is 8 spaces wide. */
	  break;
	case '\n':
	  puts ("\\hfill\n");
	  puts ("\\noindent");
	  break;
	default:
	  /* Certain characters aren't printed directly in TeX, so we
	     tell TeX to print them according to their ascii code. */
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
