#ifndef ask_h
#define ask_h

#include <string>
#include <stdlib.h>
#include <time.h>
#include <mysql/mysql.h>
using namespace std;

#include "offer.h"

class ask : public offer
{
	public:

		ask(float a, float b, string c, time_t d) : offer(a, b, c, d) {}
		ask(string);
		ask() : offer() {}

		ask load_sql(string);
		void insert_sql(MYSQL *);
};

#endif
