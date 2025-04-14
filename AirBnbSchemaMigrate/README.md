# AirBnb Schema Migration Example

This project demonstrates how to handle schema migrations in MongoDB using the `sample_airbnb` dataset, which is part of the sample data available in MongoDB Atlas. The example showcases how documents with different schemas can coexist in the same collection and how to manage them effectively using the versioning pattern.

## Prerequisites

1. **MongoDB Atlas Account**: Ensure you have access to a MongoDB Atlas cluster.
2. **Sample Data**: Load the `sample_airbnb` dataset into your Atlas cluster. This dataset is available as part of the sample data provided by MongoDB.

## Overview

The `sample_airbnb` dataset contains a collection of listings, where each document includes embedded reviews. This project demonstrates a schema migration where:

- **Original Schema**: Reviews are embedded within the listing documents.
- **Migrated Schema**: Reviews are moved to a separate `reviews` collection and referenced from the listing documents.

The migration is applied selectively to certain documents, allowing both schemas to coexist in the same collection. The code provided in this project ensures that both data models can be handled seamlessly using the versioning pattern.

## Key Features

- **Schema Coexistence**: Demonstrates how to manage collections with mixed schemas.
- **Versioning Pattern**: Implements a pattern to handle both embedded and referenced data models.
- **Selective Migration**: Applies schema changes only to specific documents.

## How It Works

1. **Original Schema**: 
   - Reviews are embedded directly in the `listings` collection.
   - Example:
     ```json
     {
       "_id": "listing_id",
       "name": "Sample Listing",
       "reviews": [
         { "reviewer": "John", "comment": "Great place!" },
         { "reviewer": "Jane", "comment": "Loved it!" }
       ]
     }
     ```

2. **Migrated Schema**:
   - Reviews are moved to a separate `reviews` collection and referenced in the `listings` collection.
   - Example:
     ```json
     {
       "_id": "listing_id",
       "name": "Sample Listing",
       "reviews": [
         { "review_id": "review1" },
         { "review_id": "review2" }
       ]
     }
     ```

     ```json
     {
       "_id": "review1",
       "listing_id": "listing_id",
       "reviewer": "John",
       "comment": "Great place!"
     }
     ```

3. **Code Implementation**:
   - The provided code handles both schemas by detecting the version of the document and processing it accordingly.

## Usage

1. Clone this repository.
2. Load the `sample_airbnb` dataset into your MongoDB Atlas cluster.
3. Run the migration script to apply the schema changes to selected documents.
4. Use the provided code to query and handle both schemas seamlessly.

## Conclusion

This project demonstrates how to manage schema migrations in MongoDB while maintaining compatibility with existing data. By using the versioning pattern, you can ensure that your application continues to function correctly during and after the migration process.
