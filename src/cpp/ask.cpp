#ifndef ask_class
#define ask_class
#include <string>
#include <stdlib.h>
#include <time.h>
#include "offer.cpp"
using namespace std;

class ask : public offer
{
	public:

		ask(float a, float b, string c, time_t d) : offer(a, b, c, d) {}
		ask(string);
		ask() : offer() {}

		ask load_sql(string);
		void insert_sql(MYSQL *);
};

ask::ask(string call) 
{ 
	this->type = "ask";
	this->load_sql(call);
}

ask ask::load_sql(string call)
{
	call = call.substr(17);
	this->rate = atoi(call.substr(call.find('\'')).c_str());

	call = call.substr(call.find(": \'") + 1);
	this->amount = atoi(call.substr(call.find('\'')).c_str());

	time(&(this->date));

	return *this;
}

void ask::insert_sql(MYSQL *sqlconnection)
{
	string query = "INSERT INTO `trader`(`amount`,`rate`,`type`,`date`) VALUES ('" + to_string(this->amount) + "', '" + to_string(this->rate) + "', 'ask', NOW());";
	int state = mysql_query(sqlconnection, query.c_str());
	if (state !=0)
	{
		printf(mysql_error(sqlconnection));
		return;
	}

}


#endif