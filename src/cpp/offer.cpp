#ifndef offer_class
#define offer_class
#include <string>
#include <stdlib.h>
#include <time.h>

class offer
{
	public:
		float rate;
		float amount;
		time_t date;

		offer(float, float, time_t);
		offer();
};

offer::offer(float rate1, float amount1, time_t date1) :
	rate(rate1), amount(amount1), date(date1)
	{ }	

offer::offer() :
	rate(0), amount(0), date(0)
	{ }
#endif