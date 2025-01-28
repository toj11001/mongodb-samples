const MongoClient = require("mongodb").MongoClient;
const dotenv = require("dotenv");

dotenv.config({ path: "../.env" }); // Load environment variables from .env file in the parent directory

const uri = process.env.MONGO_URI;

async function main() {
  const client = new MongoClient(uri, { useUnifiedTopology: true });

  try {
    await client.connect();

    const db = client.db("sample_mflix");
    const movies = db.collection("movies");
    
    movies.updateSearchIndex("autocomplete_index", {
      mappings: {
        dynamic: false,
        fields: {
          title: [
            {
              type: "autocomplete",
              analyzer: "lucene.standard",
              tokenization: "edgeGram",
              minGrams: 4,
              maxGrams: 7,
              foldDiacritics: true,
            },
            {
              type: "string",
            },
          ],
        },
      },
    });
  } catch (err) {
    console.error("An error occurred connecting to MongoDB: ", err);
  }
}

main().catch(console.error);
