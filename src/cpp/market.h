#ifndef market_h
#define market_h


#include <autobahn/autobahn.hpp>
#include <boost/asio.hpp>	
#include <autobahn/autobahn.hpp>
#include <autobahn/wamp_websocketpp_websocket_transport.hpp>
#include <websocketpp/config/asio_no_tls_client.hpp>
#include <websocketpp/client.hpp>
#include <boost/version.hpp>
#include <map>
#include <thread>
#include <mutex>
#include <iostream>
#include <memory>
#include <tuple>
#include <mysql/mysql.h>
#include <websocketpp/config/asio_client.hpp>
#include "parameters.hpp"
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

		static market & instance();

		int market_connect();
		void setup();

	private:
		market(market const&);
        void operator=(market const&);
		market() {};
};

#endif
