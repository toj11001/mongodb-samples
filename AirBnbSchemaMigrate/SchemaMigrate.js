const { getDatabase } = require('../config/db'); // Explicitly include the '.js' extension

async function getReviewsForListing(listingName) {
    const db = await getDatabase('sample_airbnb');
    const listings = db.collection('listingsAndReviews');
    const reviews = db.collection('reviews');

    const listing = await listings.findOne({ name: listingName });
    if (!listing) throw new Error('Listing not found');

    // If storageType is undefined, assume reviews are embedded
    if (!listing.storageType || listing.storageType === 'embedded') {
        return (listing.reviews || []).slice(-5); // Return the last 5 comments
    } else {
        return await reviews
            .find({ listingId: listing._id })
            .sort({ _id: -1 }) // Sort by _id in descending order to get the latest reviews
            .limit(5) // Limit to the last 5 comments
            .toArray();
    }
}

async function migrateEmbeddedToReferenced(listingName) {
    const db = await getDatabase('sample_airbnb');
    const listings = db.collection('listingsAndReviews');
    const reviews = db.collection('reviews');

    const listing = await listings.findOne({ name: listingName });
    // If storageType is already 'referenced', skip migration
    if (!listing || listing.storageType === 'referenced') return;

    const reviewDocs = (listing.reviews || []).map((review, index) => ({
        ...review, // Keep the original structure
        id: index + 1, // Add an `id` field (1-based index)
        listingId: listing._id,
    }));

    if (reviewDocs.length > 0) {
        await reviews.insertMany(reviewDocs);
    }

    await listings.updateOne(
        { _id: listing._id },
        {
            $set: {
                reviews: [],
                storageType: 'referenced', // Add storageType after migration
            }
        }
    );
}

async function main() {
    const listingName = 'Copacabana Apartment Posto 6';

    console.log('Before migration:', await getReviewsForListing(listingName));
    await migrateEmbeddedToReferenced(listingName);
    console.log('After migration:', await getReviewsForListing(listingName));
}

main()
    .then(() => {
        console.log("Schema migration completed.");
    })
    .catch(err => {
        console.error("Error during schema migration:", err);
    });
