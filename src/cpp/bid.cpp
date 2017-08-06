#ifndef bid_class
#define bid_class
#include <string>
#include <stdlib.h>
#include <time.h>
#include "offer.cpp"

class bid : public offer
{
	public:
		float rate;
		float amount;
		time_t date;
		string type;

		bid(float, float, time_t) : offer(float, float, time_t) {this.type = "bid";};
		bid(string);
		bid() : offer() {this.type = "bid";};

		bid load_sql(string);
};

bid::bid(string call) 
{
	this.type = "bid";
	this.load_sql(call);
}

bid bid::load_sql(string call)
{
	call = call.substr(17);
	this.rate = atoi(call.substr(call.find('\'')));

	call = call.substr(call.find(": \'") + 1);
	this.amount = atoi(call.substr(call.find('\'')));

	time(&this.date)

	return this;
}


#endif