const { MongoClient } = require('mongodb');
const dotenv = require('dotenv');
const path = require('path');

// Load environment variables from .env file
dotenv.config({ path: path.resolve(__dirname, 'config', '.env') });

const uri = process.env.MONGO_URI;

if (!uri) {
    throw new Error("MONGO_URI is not defined in the .env file. Please check your configuration.");
}

let client;

async function connectToMongoDB() {
    if (!client) {
        try {
            client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
            await client.connect();
            console.log("Successfully connected to MongoDB.");
        } catch (error) {
            console.error("Failed to connect to MongoDB:", error);
            throw error; // Re-throw the error to ensure it is handled by the caller
        }
    }
    return client;
}

async function getDatabase(dbName) {
    try {
        const client = await connectToMongoDB();
        return client.db(dbName);
    } catch (error) {
        console.error(`Failed to get database '${dbName}':`, error);
        throw error; // Re-throw the error to ensure it is handled by the caller
    }
}

module.exports = {
    connectToMongoDB,
    getDatabase
};