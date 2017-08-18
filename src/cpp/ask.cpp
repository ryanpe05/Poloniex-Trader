#ifndef ask_class
#define ask_class

#include "ask.h"

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
