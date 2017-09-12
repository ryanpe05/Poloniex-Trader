#ifndef market_cpp
#define market_cpp
#include "market.h"

market &market::instance()
{
	static market inst;
	return inst;	
}

void market::setup()
{
	cout << "setting up" << endl;
	mysql_init(&(this->mysql));
	cout << "setting up" << endl;
	this->sqlconnection = mysql_real_connect(&(this->mysql),"localhost","trader","Immabigfatjuicypassword","trades",0,0,0);
	/*int state = mysql_query(this->sqlconnection, "select * from `trades` where date BETWEEN DATE_SUB(NOW(), INTERVAL 14 DAY)  AND NOW()");

	if (state !=0)
	{
		printf(mysql_error(sqlconnection));
	}
	result = mysql_store_result(sqlconnection);
	while ( ( row=mysql_fetch_row(result)) != NULL )
	{
		cout << row << endl;
     and hello Ryan
	}	*/
}


void trade_event(string update)
{

	cout << "Type casting the mother fucker" << endl;
	cout << update << endl;
	cout << "Done type casting the mother fucker" << endl;
	/*if(update.size() > 75)
	{
	    bid bidevent(update);  
	    market::instance().offers.push_front(bidevent);
	    market::instance().offers.pop_back();
	    cout << "bid " << bidevent.rate << endl;
	}                                                                                                                                                                          
	else
	{
		ask askevent(update);
	    market::instance().offers.push_front(askevent);
	    market::instance().offers.pop_back();
	    cout << "ask " << askevent.rate << endl;
	}*/
}

int market::market_connect()
{
    cout << "Starting connection" << endl;
	using namespace wamp;
    AsioService iosvc;
    auto tcp = connector<Json>(iosvc, TcpHost("api.poloniex.com", 443));
    cout << "Made a connector" << endl;
    auto session = CoroSession<>::create(iosvc, tcp);
    cout << "Made a sesison" << endl;
    boost::asio::spawn(iosvc, [&](boost::asio::yield_context yield)
    {

        cout << "Starting to connect" << endl;
        session->connect(yield);
        cout << "Joining realm" << endl;
        session->join(Realm("pioniex"), yield);
        auto result = session->call(Rpc("USDT_ETH"), yield);
        session->subscribe(Topic("USDT_ETH"),
                           wamp::basicEvent<std::string>(&trade_event),
                           yield);
    });
    iosvc.run();
    return 0;
}


#endif
