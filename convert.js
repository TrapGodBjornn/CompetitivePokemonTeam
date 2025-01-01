try {

const fs = require("fs");
// Import the Pokedex data from your newly edited JS file
const { Pokedex } = require("./pokedex.js");

// Convert the JavaScript object to JSON
const jsonData = JSON.stringify(Pokedex, null, 2);

// Write the JSON data to a file
fs.writeFileSync("pokedex.json", jsonData);

console.log("Conversion complete! Check pokedex.json");
} catch (error) {
    console.error("Error during conversion:", error);
}