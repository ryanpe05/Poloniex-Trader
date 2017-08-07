#include <sys/time.h>
#include <stdio.h>
#include <mysql.h>
#include <iostream>
using namespace std;
#include <cstdlib>


int main()
{
	MYSQL_RES *result;
	MYSQL_ROW row;
	MYSQL *connection, mysql;
	int state;

	mysql_init(&mysql);
	connection = mysql_real_connect(&mysql,"kostakonstas.com","kostakon_me","Z(9s_t[m}_-","kostakon_students",0,0,0);
	char dat[1024];

	cin.getline(dat, 1024);
	string data = dat;

	int userID = atoi(data.substr(data.find("id") + 3).c_str());

	if (connection == NULL)
	{
		printf(mysql_error(&mysql));
		return 1;
	}

	string prompt = "SELECT * FROM `queue` WHERE 1 ORDER BY ID ASC";
	state = mysql_query(connection, prompt.c_str());
	if (state !=0)
	{
		printf(mysql_error(connection));
		return 1;
	}
	result = mysql_store_result(connection);
	int smallest = -1;
	if ( ( row=mysql_fetch_row(result)) != NULL )
	{
		smallest = atoi(row[1]);
	}
	int place = -1;

	if (userID > smallest && smallest != -1)
		place = userID - smallest;
	
	if(userID == smallest)
		place = 0;
	int used_id = mysql_insert_id(&mysql);
	cout << "content-type: text/html\r\n\r\n" << endl;
	cout << "<data><place>" << place + 1 << "</place></data>"<< endl;

	mysql_close(connection);

return 0;

};


/*


Now we make a simple query like “SELECT * FROM mytable” and check if it has no errors, where “mytable” is the name of wished table:


After the successful execution of the query, we must store the results somewhere:

result = mysql_store_result(connection);

Using mysql_num_rows function, we can get number of rows from result:

printf(“Rows:%d\n”,mysql_num_rows(result));

Using while statement and mysql_fetch_row functions, it possible to process each row in the result set:

while ( ( row=mysql_fetch_row(result)) != NULL )

{

printf(” %s, %s\n”, (row[0] ? row[0] : “NULL”), (row[1] ? row[1] : “NULL” ));

}

At the end, we must free the memory:

mysql_free_result(result);

mysql_close(connection);*/
