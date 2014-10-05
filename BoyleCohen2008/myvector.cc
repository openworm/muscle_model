#include "myvector.hh"

vector2d create_vector2d(int x, int y)
{
   vector2d v(x);
   
   for (int i = 0; i < x; ++i) {
      v[i].resize(y);
      for (int j = 0; j < y; ++j) {
         v[i][j] = 0;
      }
   }

   return v;
}

