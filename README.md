# mongodb-samples

Collection of different MongoDB sample implementations.

## Repository Structure

This repository contains various MongoDB sample projects. Each subfolder represents a specific use case or example:

- **AirBnbSchemaMigrate**: Demonstrates schema migration in the `sample_airbnb` dataset. See the [AirBnbSchemaMigrate README](./AirBnbSchemaMigrate/README.md) for more details.

## Configuration

1. Navigate to the `config` folder.
2. Copy the `.env.sample` file and rename it to `.env`.
3. Update the `MONGO_URI` variable in the `.env` file with your MongoDB connection string.

The `config/db.js` file is used across the projects to establish a connection to the MongoDB cluster.

## Usage

Refer to the README file in each subfolder for specific instructions on running the examples.
