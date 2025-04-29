#!/usr/bin/env python3
from pymongo import MongoClient
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import argparse
import pymongo.database
import pymongo.errors


def connectToDatabase():
	# Load environment variables from .env file
	load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

	# Get the MongoDB connection details from environment variables
	mongo_uri = os.getenv("MONGO_URI")

	# Create the MongoDB client and connect to MongoDB
	client = MongoClient(mongo_uri)

	# Connect to the database
	db = client.get_database("demo")
	return db



# This is the object that the application would be working with anyway and
# so you wouldn't actually need to create it just to add it to the DB
customer = {
		"name" : {
			"first" : "Max",
			"second" : "Mustermann"
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

# Employee objects
employee1 = {
  "emp_no": 1012,
  "first_name": "Bart",
  "last_name": "Davis",
  "gender": "M",
  "annual_salary": 66766,
  "hire_date": {
    "$date": "2012-03-06T00:00:00.000Z"
  }
}   

employee2 = {
  "emp_no": 1028,
  "first_name": "Max",
  "last_name": "Mustermann",
  "gender": "M",
  "annual_salary": 64431,
  "hire_date": {
    "$date": "2008-07-04T00:00:00.000Z"
  }
}

def addUser(database:pymongo.database.Database, user):
	# add the user to the collection customers
	try:
		return database.customers.insert_one(user).inserted_id
	except pymongo.errors.DuplicateKeyError:
		print("Duplicate key error: The user already exists in the database.")
		return None


if __name__ == "__main__":
	# Set up argument parser
	parser = argparse.ArgumentParser(description="MongoDB Insert Script")
	parser.add_argument("--add_user", action="store_true", help="Add a user to the database")
	parser.add_argument("--increase_salary", action="store_true", help="Increase salary of Michael Anderson by 10%")
	parser.add_argument("--sabbatical", action="store_true", help="Mark employee 1012 as on sabbatical")
	parser.add_argument("--delete_employee", action="store_true", help="Delete employee 1012 from the database")
	parser.add_argument("--clear_collection", action="store_true", help="Clear the complete collection")
	parser.add_argument("--create_index", action="store_true", help="Create a unique compound index on first_name and last_name")
	args = parser.parse_args()

	db = connectToDatabase()

	if args.add_user:
		customerId = addUser(db, customer)
		customerId1 = addUser(db, employee1)
		customerId2 = addUser(db, employee2)
		print(f"CustomerId: {customerId}\nCustomerId1: {customerId1}\nCustomerId2: {customerId2} added to the database")
	elif args.increase_salary:
		result = db.customers.update_one(
			{"first_name": "Max", "last_name": "Mustermann"},
			[{"$set": {"annual_salary": {"$multiply": ["$annual_salary", 1.10]}}}]
		)
		print(f"Updated {result.modified_count} document(s) for salary increase.")
	
	elif args.sabbatical:
		result = db.customers.update_one(
			{"emp_no": 1012},
			{"$set": {"permanent_leave": True}}
		)
		print(f"Updated {result.modified_count} document(s) for sabbatical.")
	
	elif args.delete_employee:
		result = db.customers.delete_one({"emp_no": 1012})
		print(f"Deleted {result.deleted_count} document(s).")
	
	elif args.clear_collection:
		result = db.customers.delete_many({})
		db.customers.drop_indexes()
		print(f"Cleared {result.deleted_count} document(s) from the collection.")
	
	elif args.create_index:
		try:
			result = db.customers.create_index(
				[("first_name", pymongo.ASCENDING), ("last_name", pymongo.ASCENDING)],
				unique=True
			)
			print(f"Created index: {result}")
		except pymongo.errors.DuplicateKeyError as e:
			print(f"Duplicate key error: KeyPattern {e.details['keyPattern']}")
	
	else:
		print("No action specified. Use --add_user, --increase_salary, --sabbatical, --delete_employee, --clear_collection, or --create_index.")