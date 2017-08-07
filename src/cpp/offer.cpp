#ifndef offer_class
#define offer_class
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

offer::offer(float rate1, float amount1, string type1, time_t date1) :
	rate(rate1), amount(amount1), date(date1), type(type1)
	{ }	

offer::offer() :
	rate(0), amount(0), date(0), type("")
	{ }
#endif