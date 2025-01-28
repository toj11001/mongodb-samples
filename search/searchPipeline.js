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

    if (!movies) {
      throw new Error("Collection 'movies' not found");
    }

    const cursor = movies.aggregate([
      {
        $search: {
          index: "autocomplete_index",
          autocomplete: {
            path: "title",
            tokenOrder: "sequential",
            query: "Star Wars: Episode VI - Return of the Jedi",
          },
        },
      },
      {
        $project: {
          _id: 0,
          title: 1,
          score: { $meta: "searchScore" },
        },
      },
    ]);
    const resultsArray = await cursor.toArray();
    console.log("Results:", resultsArray);

    // Use the Compound Operator to Boost the Score of Exact Matches
    const autocomplete = {
      autocomplete: {
        path: "title",
        tokenOrder: "sequential",
        query: "Star Wars: Episode VI - Return of the Jedi",
      },
    };

    const text = {
      text: {
        query: "Star Wars: Episode VI - Return of the Jedi",
        path: "title",
      },
    };

    cursor = db.movies.aggregate([
      {
        $search: {
          index: "autocomplete_index",
          compound: {
            should: [autocomplete, text],
            minimumShouldMatch: 1,
          },
        },
      },
      {
        $project: {
          _id: 0,
          title: 1,
          score: { $meta: "searchScore" },
        },
      },
    ]);

    console.log(`Results with compound operator: ${await cursor.toArray()}`);
  } catch (err) {
    console.error("Error connecting to MongoDB:", {
      message: err.message,
      name: err.name,
      stack: err.stack,
      code: err.code,
    });
  }
}

main().catch(console.error);
