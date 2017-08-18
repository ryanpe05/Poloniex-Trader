#ifndef offer_class
#define offer_class
#include "offer.h"
offer::offer(float rate1, float amount1, string type1, time_t date1) :
	rate(rate1), amount(amount1), date(date1), type(type1)
	{ }	

offer::offer() :
	rate(0), amount(0), date(0), type("")
	{ }
#endif
