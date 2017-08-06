#ifndef ask_class
#define ask_class
#include <string>
#include <stdlib.h>
#include <time.h>
#include "offer.cpp"

class ask : public offer
{
	public:
		float rate;
		float amount;
		time_t date;
		string type;

		ask(float, float, time_t) : offer(float, float, time_t) { this.type = "ask";};
		ask(string);
		ask() : offer() {this.type = "ask";;

		ask load_sql(string);
};

ask::ask(string call) :
{ 
	this.type = "ask";
	this.load_sql(call);
}

ask ask::load_sql(string call)
{
	call = call.substr(17);
	this.rate = atoi(call.substr(call.find('\'')));

	call = call.substr(call.find(": \'") + 1);
	this.amount = atoi(call.substr(call.find('\'')));

	time(&this.date);

	return this;
}


#endif