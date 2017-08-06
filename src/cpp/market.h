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
#include "offer.cpp"
using namespace std;

class market
{
	map<string, float> balances;
	
	list<offer> mytrades;
	list<offer> offers;


	int market_connect();
	void ticker_event(const autobahn::wamp_event& event);
	void bid_event(const autobahn::wamp_event& event);
	void ask_event(const autobahn::wamp_event& event);

};
#endif