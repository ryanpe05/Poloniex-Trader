#ifndef ticker_class
#define ticker_class
#include <string>
#include <stdlib.h>
#include <time.h>
using namespace std;

class ticker()
{
	public:
		string currency;
		float last;
		float lowest;
		float highest;
		float change;
		double baseVol;
		double quoteVol;
		time_t date;

		ticker(float, float, float, float, double, double, time_t);
		ticker(string)
		ticker();

		ticker load_sql(string);

};

ticker::ticker(float last1, float lowest1, float highest1, float change1, double baseVol1, double quoteVol1, time_t date1) :
	last(last1), lowest(lowest1), highest(highest1), change(change1), baseVol(baseVol1), quoteVol(quoteVol1), date(date1)
	{ }

ticker::ticker() :
	last(0), lowest(0), highest(0), change(0), baseVol(0), quoteVol(0), date(0)
	{ }

ticker::ticker(string call) :
{
	this.load_sql(call);	
}

ticker ticker::load_sql(string call) :
{
	call = call.substr(2);
	this.currency = call.substr(0, call.find('\''));

	call = call.substr(call.find('\'') + 1);
	this.lowest = atof(call.substr(0, call.find('')));

	call = call.substr(call.find('\'') + 1);
	this.highest = atof(call.substr(0, call.find('')));

	call = call.substr(call.find('\'') + 1);
	this.change = atof(call.substr(0, call.find('')));

	call = call.substr(call.find('\'') + 1);
	this.baseVol = atof(call.substr(0, call.find('')));


	call = call.substr(call.find('\'') + 1);
	this.quoteVol = atof(call.substr(0, call.find('')));

	call = call.substr(call.find('\'') + 1);
	this.date = atoi(call.substr(0, call.find('')));

	return this;
}

#endif