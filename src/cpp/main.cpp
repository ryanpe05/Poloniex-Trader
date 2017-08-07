#include "market.h"
#include <iostream>
using namespace std;
int main()
{
	cout << "setup" << endl;
	market::instance().setup();
	cout << "connect" << endl;
	market::instance().market_connect();
	cout << "run" << endl;

	while (true)
	{

	}
}