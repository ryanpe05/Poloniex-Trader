#ifndef market_h
#define market_h


#include <ctime>
#include <iostream>

#include "wampcc/wampcc.h"



#include <map>
#include <thread>
#include <mutex>
#include <iostream>
#include <memory>
#include <tuple>
#include <list>
#include <mysql/mysql.h>
#include "bid.h"
#include "ask.h"

using namespace std;

class offer;
class bid;
class ask;


class market
{
	public:
		map<string, float> balances;
		
		list<offer> mytrades;
		list<offer> offers;
 	
		MYSQL_RES *result;
		MYSQL_ROW row;
		MYSQL *sqlconnection, mysql;
		
		const std::string realm = "cppwamp.demo.time";
		const std::string address = "localhost";
		const short port = 12345;

		static market & instance();

		int market_connect();
		void setup();

	private:
		market(market const&);
        void operator=(market const&);
		market() {};
};

#endif
