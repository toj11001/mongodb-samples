#!/usr/bin/env python3

import mysql.connector
from mysql.connector import errorcode
import mysql.connector.cursor

def addUser(connection, user):
	cursor = connection.cursor()

	customerInsert = (
		"INSERT INTO customer (first_name, last_name, email, "
		"DOB, annual_spend) VALUES "
		"(%(first)s, %(last)s, %(email)s, %(dob)s, %(spend)s)")

	customerData = {
		'first': user['name']['first'],
		'last': user['name']['second'],
		'email': user['email'],
		'dob': user['dob'],
		'spend': user['annualSpend']
	}

	cursor.execute(customerInsert, customerData)
	customerId = cursor.lastrowid

	cityQuery = ("SELECT city_id FROM city WHERE city = %(city)s")
	for address in user['address']:
		cursor.execute(cityQuery, {'city': address['city']})
		city_id = cursor.fetchone()[0]

		addressInsert = (
			"INSERT INTO address (address, address2, district, "
			"city_id, postal_code, customer_id, location) "
			"VALUES (%(add)s, %(add2)s, %(dist)s, %(city)s, %(post)s, %(cust)s, %(loc)s)")
		
		addressData = {
			'add': address['number'],
			'add2': address['street'],
			'dist': address['state'],
			'city': city_id,
			'post': address['postalCode'],
			'cust': customerId,
			'loc':	address['location']
		}
		
		cursor.execute(addressInsert, addressData)
		
	topicQuery = ("SELECT topics_id FROM topics WHERE subject = %(subj)s")
	interestInsert = (
		"INSERT into interests (topic_id, customer_id) "
		"VALUES (%(topic)s, %(cust)s)")

	# For each interest, see if it already exists in the topic table; if not then
	# add it. In either case, record the id from the topics table and use that to add
	# an entry to the interests table for the customer.

	for interest in user['interests']:
		topicId = 0
		topicData = {
			'subj': interest['interest']
		}

		cursor.execute(topicQuery, topicData)
		row = cursor.fetchone()
		if row is None:
			topicInsert = ("INSERT INTO topics (subject) VALUES (%(subj)s)")
			cursor.execute(topicInsert, topicData)
			topicId = cursor.lastrowid
		else:
			topicId = row[0]

		interestData = {
			'topic': topicId,
			'cust': customerId
		}
		cursor.execute(interestInsert, interestData)

	phoneInsert = (
		"INSERT INTO `phone numbers` (customer_id, phone_number, `Phone number_type`) "
		"VALUES (%(cust)s, %(num)s, %(type)s)")
	for phoneNumber in user['phone']:
		phoneData = {
			'cust': customerId,
			'num': phoneNumber['number'],
			'type': phoneNumber['location']
		}
		cursor.execute(phoneInsert, phoneData)

	connection.commit()
	cursor.close()
	return customerId


def addSimpleUser(connection, user):
	cursor = connection.cursor()
	customerInsert = (
		"INSERT INTO customer (first_name, last_name, email, "
		"home_address_id, work_address_id, DOB, annual_spend) VALUES "
		"(%(first)s, %(last)s, %(email)s, %(dob)s, %(spend)s)")
	customerData = {
		'first': user['name']['first'],
		'last': user['name']['second'],
		'email': user['email'],
		'dob': user['dob'],
		'spend': user['annualSpend']
	}
	cursor.execute(customerInsert, customerData)
	customerId = cursor.lastrowid
	connection.commit()
	cursor.close()
	return customerId


def addStillSimpleUser(connection, user):
	homeId = 0
	workId = 0
	cursor = connection.cursor()
	cityQuery = ("SELECT city_id FROM city WHERE city = %(city)s")
	for address in user['address']:
		cursor.execute(cityQuery, {'city': address['city']})
		city_id = cursor.fetchone()[0]
		addressInsert = (
			"INSERT INTO address (address, address2, district, "
			"city_id, postal_code) "
			"VALUES (%(add)s, %(add2)s, %(dist)s, %(city)s, %(post)s)")
		addressData = {
			'add': address['number'],
			'add2': address['street'],
			'dist': address['state'],
			'city': city_id,
			'post': address['postalCode']
		}
		cursor.execute(addressInsert, addressData)
		addressID = cursor.lastrowid
		if address['location'] == "home":
			homeId = addressID
		elif address['location'] == "work":
			workId = addressID
		
	customerInsert = (
		"INSERT INTO customer (first_name, last_name, email, "
		"home_address_id, work_address_id, DOB, annual_spend) VALUES "
		"(%(first)s, %(last)s, %(email)s, %(home)s, %(work)s, %(dob)s, %(spend)s)")
	customerData = {
		'first': user['name']['first'],
		'last': user['name']['second'],
		'email': user['email'],
		'home': homeId,
		'work': workId,
		'dob': user['dob'],
		'spend': user['annualSpend']
	}
	cursor.execute(customerInsert, customerData)
	customerId = cursor.lastrowid

	connection.commit()
	cursor.close()
	return customerId


try:
	cnx = mysql.connector.connect(user="user", password="password",
		host="localhost",
		database="testdb")
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
else:
	customer = {
		"name" : {
			"first" : "Eartha",
			"second" : "Thompson"
		},
		"address" : [
			{
				"location" : "home",
				"number" : 23,
				"street" : "Twin Pines",
				"city" : "New York",
				"state" : "New York",
				"postalCode" : "O83 1F1"
			},
			{
				"location" : "work",
				"number" : 1,
				"street" : "Holy Cross",
				"city" : "New York",
				"state" : "New York",
				"postalCode" : "513 8U5"
			}
		],
		"phone" : [
			{
				"location" : "mobile",
				"number" : "+48-675-560-3029"
			},
						{
				"location" : "work",
				"number" : "+48-887-222-1234"
			}
		],
		"email" : "eandrzejak0@yellowpages.com",
		"annualSpend" : 916305.32,
		"dob" : "1985-02-28 07:32:58",
		"interests" : [
			{
				"interest" : "XML Schema Design"
			},
			{
				"interest" : "Glazing"
			}
		]
	}
	customer = addUser(cnx, customer)
	print(f"Added customer# {customer} to the database")
	cnx.close()