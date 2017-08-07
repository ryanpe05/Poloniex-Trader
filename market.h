#ifndef market_h
#define market_h


#include <autobahn/autobahn.hpp>
#include <boost/asio.hpp>
#include <list>
#include <map>
#include <thread>
#include <mutex>
#include <iostream>
#include <memory>
#include <tuple>
#include <mysql.h>
#include "offer.cpp"
using namespace std;

class market
{
	public:
		map<string, float> balances;
		
		list<offer> mytrades;
		list<offer> offers;

		MYSQL_RES *result;
		MYSQL_ROW row;
		MYSQL *sqlconnection, mysql;

		market();

		int market_connect();
		void ticker_event(const autobahn::wamp_event& event);
		void bid_event(const autobahn::wamp_event& event);
		void ask_event(const autobahn::wamp_event& event);
};

market::market() :
{
	mysql_init(&this.mysql);
	this.sqlconnection = mysql_real_connect(&this.mysql,"localhost","trader","Immabigfatjuicypassword","trades",0,0,0);
	int state = mysql_query(this.sqlconnection, "select * from `trades` where date BETWEEN DATE_SUB(NOW(), INTERVAL 14 DAY)  AND NOW()");

	if (state !=0)
	{
		printf(mysql_error(sqlconnection));
		return 1;
	}
	result = mysql_store_result(sqlconnection);
	while ( ( row=mysql_fetch_row(result)) != NULL )
	{
		cout << row << endl;
	}	
}
#endif