#ifndef bid_class
#define bid_class
#include <string>
#include <stdlib.h>
#include <time.h>
#include "offer.cpp"
using namespace std;

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

bid::bid(string call) 
{
	this->type = "bid";
	this->load_sql(call);
}

bid bid::load_sql(string call)
{
	call = call.substr(17);
	this->rate = atoi(call.substr(call.find('\'')).c_str());

	call = call.substr(call.find(": \'") + 1);
	this->amount = atoi(call.substr(call.find('\'')).c_str());

	time(&(this->date));
	return *this;
}

void bid::insert_sql(MYSQL *sqlconnection)
{
	string query = "INSERT INTO `trader`(`amount`,`rate`,`type`,`date`) VALUES ('" + to_string(this->amount) + "', '" + to_string(this->rate) + "', 'bid', NOW())";
	int state = mysql_query(sqlconnection, query.c_str());
	if (state !=0)
	{
		printf(mysql_error(sqlconnection));
		return;
	}

}


#endif