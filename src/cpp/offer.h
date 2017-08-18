#ifndef offer_h
#define offer_h

#include <string>
#include <stdlib.h>
#include <time.h>
using namespace std;

class offer
{
	public:
		float rate;
		float amount;
		time_t date;
		string type;

		offer(float, float, string, time_t);
		offer();
};

#endif
