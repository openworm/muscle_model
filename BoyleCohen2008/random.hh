/**
 * \file random.h
 * \author Dave Cliff
 * \date May 1991
 * \addtogroup utilities
 * Some general random routines, and some useful #defines
 * Modified by Dave Gordon 2002
 * Moved the #defines elsewhere and turned everything into C++ templates
 */

#ifndef _RANDOM_H_
#define _RANDOM_H_

#include <cmath>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <functional>

/**
 * \addtogroup utilities
 * @{
 */

/*Real may be double or float*/
//#define Real double
// DG: This has been replaced with C++ template syntax. Where real numbers are
// involved, make calls using the type you want returning as parameters, or if
// there are no parameters, include the desired output type in <>'s, e.g.
// gaussrand<float>();

/*ran1 from the numerical recipes in c book -- it's the slowest but (?) best*/

#define M1 259200
#define IA1 7141
#define IC1 54773
#define RM1 (1.0/M1)
#define M2 134456
#define IA2 8121
#define IC2 28411
#define RM2 (1.0/M2)
#define M3 243000
#define IA3 4561
#define IC3 51349

/********************* ran1 *******************/

inline float ran1(int* idum)
{
    static long ix1,ix2,ix3;
    static float r[98];
    float temp;
    static int iff=0;
    int j;
    void nrerror();

    if (*idum < 0 || iff == 0) {
        iff=1;
        ix1=(IC1-(*idum)) % M1;
        ix1=(IA1*ix1+IC1) % M1;
        ix2=ix1 % M2;
        ix1=(IA1*ix1+IC1) % M1;
        ix3=ix1 % M3;
        for (j=1;j<=97;j++) {
            ix1=(IA1*ix1+IC1) % M1;
            ix2=(IA2*ix2+IC2) % M2;
            r[j]=static_cast<float>((ix1+ix2*RM2)*RM1);
        }
        *idum=1;
    }
    ix1=(IA1*ix1+IC1) % M1;
    ix2=(IA2*ix2+IC2) % M2;
    ix3=(IA3*ix3+IC3) % M3;
    j=1 + ((97*ix3)/M3);
    if (j > 97 || j < 1)
    /* nrerror("RAN1: This cannot happen."); */
		std::cerr << "RAN1: This cannot happen." << std::endl;
    temp=r[j];
    r[j]=static_cast<float>((ix1+ix2*RM2)*RM1);
    return temp;
}

#undef M1
#undef IA1
#undef IC1
#undef RM1
#undef M2
#undef IA2
#undef IC2
#undef RM2
#undef M3
#undef IA3
#undef IC3

/************************************************/

/* Reseeds the random number generator from the system clock.
 * if the argument is zero then the system clock is used, otherwise the
 * argument is the seed
 */
inline int rseed(int *s, bool verbose = false)
{
	time_t tseed;
	int    seed;

	if((*s)==0)
	{
		time(&tseed);
		seed=static_cast<int>(tseed%32767);
		*s=seed;
	}
	else seed=*s;

	if(verbose) std::cout << "\n: Seed is " << seed << std::endl;
	/* srandom(seed); */
	seed=seed*-1;
	ran1(&seed);
	return(*s);
}

/**
 * Returns a (near) uniform distributed random number in the range
 * 0..limit, as a Real
 */
template <typename Real>
inline Real randval(Real limit)
{
	float  rv;
	int    i=1;
	/*get a random value in the range 0..1*/
	/*rv=random()/MAX_RAND*/
	rv=ran1(&i);
	return(limit*(static_cast<Real>(rv)));
}


/**
 * Returns a random integer in [0..limit-1]
 */
inline int irand(int limit)
{
	int ir;
	/*while loop is used to trap the exceptional case where
	the underlying deviate in [0,1] actually returns 1.00*/
	ir=limit;
	while(ir==limit)
	{
		ir=static_cast<int>(floor(randval(static_cast<double>(limit))));
	}
	return(ir);
}

inline bool brand(double p)
{
	return randval(1.0) <= p;
}

inline bool brand(float p)
{
	return randval(1.0f) <= p;
}

/**
 * Template specialisation to stop randval from being called with ints
 */
template <>
inline int randval(int limit)
{
	return irand(limit + 1);
}

template <>
inline bool randval(bool)
{
	return brand(0.5);
}

/**
 * Returns a normally distributed variable with zero mean and unit
 * variance. Recall that the absolute value will be >3 about once in 400
 * trials (the three-sigma rule). This is adapted from the "Numerical recipies
 * in C" book by Press, Flannery, Teukolsky, and Vetterling, p.217
 */
template <typename Real>
inline Real gaussrand(void)
{
  static int iset=0;
  static Real gset;
  Real fac,r,v1,v2;
  
  if(iset==0)
    {
      do {
	v1=2.0*randval(1.0)-1.0;
	v2=2.0*randval(1.0)-1.0;
	r=(v1*v1)+(v2*v2);
      } while (r>=1.0);
      
      fac=sqrt(-2.0*log(r)/r);
      gset=v1*fac;
      iset=1;
      return(v2*fac);
    }
  else {
    iset=0;
    return(gset);
  }
}

/**
 * Returns a random deviate from a normal distribution with specified
 * mean and standard distribution
 */
template <typename Real>
Real normrand(Real mean,Real sd)
{ 
	return((sd*gaussrand<Real>())+mean);
}

/**
 * Function object version of randval
 * \see randval
 */
template <typename _Type>
struct Random : public std::unary_function<_Type, _Type> {
	Random(): limit(static_cast<_Type>(1.0)){}
	Random(_Type l): limit(l){}
	_Type operator()(_Type n) {
		return randval(n);
	}
	_Type operator()() {
		return randval(limit);
	}
	_Type limit;
};

/**
 * @}
 */

#endif
