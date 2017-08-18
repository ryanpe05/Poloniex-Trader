#ifndef bid_h
#define bid_h
#include <string>
#include <stdlib.h>
#include <time.h>
#include <mysql/mysql.h>
using namespace std;
#include "offer.h"

class bid : public offer
{
	public:
		float rate;
		float amount;
		time_t date;
		string type;

		bid(float a, float b, string c, time_t d) : offer(a, b, c, d) {};
		bid(string);
		bid() : offer() {}

		bid load_sql(string);
		void insert_sql(MYSQL *);
};

#endif
