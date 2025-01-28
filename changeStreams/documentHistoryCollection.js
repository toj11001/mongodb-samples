const MongoClient = require("mongodb").MongoClient;
const dotenv = require("dotenv");

dotenv.config(); // Load environment variables from .env file

const uri = process.env.MONGO_URI;

async function main() {
  const client = new MongoClient(uri, { useUnifiedTopology: true });

  try {
    await client.connect();

    const db = client.db("DEMO");
    const collection = db.collection("EBalance");
    const historyCollection = db.collection("EBalanceHistory");

    // Ensure pre-image option is enabled on the collection
    await db.command({
      collMod: "EBalance",
      changeStreamPreAndPostImages: { enabled: true }
    });
    
    const changeStream = collection.watch([], {
      changeStreamOptions: { preAndPostImages: { expireAfterSeconds: 100 } },
      fullDocument: 'updateLookup',
      fullDocumentBeforeChange: "required"
    });

    changeStream.on("change", async (change) => {
      console.log("A change occurred: ", change);

      const { documentKey, fullDocumentBeforeChange, updateDescription } =
        change;

      if (updateDescription) {
        const historyDocument = {
          _id: documentKey._id,
          updatedFields: updateDescription.updatedFields,
          removedFields: updateDescription.removedFields,
          operationType: change.operationType,
          timestamp: new Date(),
        };

        try {
          const insertResult = await historyCollection.insertOne(
            historyDocument
          );

          console.log(
            `Successfully created history document with _id: ${insertResult.insertedId}`
          );
        } catch (err) {
          console.error(err);
        }
      }
    });
  } catch (err) {
    console.error("An error occurred connecting to MongoDB: ", err);
  }
}

main().catch(console.error);
