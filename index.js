import express from "express";
import bodyParser from "body-parser";
import cors from "cors";
import { exec } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const port = process.env.PORT || 3000;
const app = express();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());
app.use(cors());

// Products Data
const products = [ 
    { 
        imageLink1: "https://i.pinimg.com/1200x/24/27/d9/2427d952652461311a38b0847137c7d6.jpg", 
        prodName1: "Foundation",
        imageLink2: "https://i.pinimg.com/1200x/04/ee/b4/04eeb4c7bd9159ce82aa8d9b2d0c0bf8.jpg", 
        prodName2: "Face Powder",
        imageLink3: "https://i.pinimg.com/1200x/a2/36/cf/a236cf7cf0705b0b99215919d21e83f0.jpg", 
        prodName3: "Concealer"
    },
    { 
        imageLink1: "https://i.pinimg.com/1200x/24/5d/18/245d18c2ecdd07cb3c2fd9b579137f3f.jpg", 
        prodName1: "Face Cream",
        imageLink2: "https://i.pinimg.com/1200x/1e/9c/b7/1e9cb779b927673fd2a83de4130f69da.jpg", 
        prodName2: "Sunscreen",
        imageLink3: "https://i.pinimg.com/1200x/24/2f/21/242f2122d36621c8d057613ad9ec062a.jpg", 
        prodName3: "Body Lotion"
    }
];

const inputImg = [ 
    { 
        imageLink: "https://i.pinimg.com/1200x/2c/d3/fb/2cd3fbb75ade740992cda2da4badb5b0.jpg", 
        prodName: "makeup Image" 
    },
    { 
        imageLink: "https://i.pinimg.com/1200x/63/5b/be/635bbef049c34c492a6b8c0bea0ca3ab.jpg", 
        prodName: "skincare Image" 
    }
];

// Routes
app.get("/", (req, res) => {
    res.render("index.ejs");
});

app.get("/aboutus", (req, res) => {
    res.render("aboutus.ejs");
});

app.get("/skincare", (req, res) => {
    res.render("product.ejs", {
        product: products[1]
    });
});

app.get("/input", (req, res) => {
    const productType = req.query.product_type || " ";
    res.render("input.ejs", {
        product_type: productType
    });
});


app.get("/makeup", (req, res) => {
    res.render("product.ejs", {
        product: products[0]
    });
});

app.get("/skinrec", (req, res) => {
    res.render("recommend.ejs", {
        look: inputImg[1]
    });
});

app.get("/makerec", (req, res) => {
    res.render("recommend.ejs", {
        look: inputImg[0]
    });
});

// POST Route for Recommendations
app.post("/recommend", (req, res) => {
    console.log("Request Body:", req.body);
    let { product_type, price, sensitivity, skinType } = req.body;

    let priceRange = [0,100];
    if(price === "0-20") priceRange = [0,20];
    else if(price === "20-40")priceRange = [20,40];
    else if(price === "40-60")priceRange = [40,60];
    else if(price === "60-80")priceRange = [60,80];
    else if(price === "80-100")priceRange = [80,100];

    // Convert input data to a JSON string
    const inputJSON = JSON.stringify({ 
        product_type, 
        priceRange, 
        sensitivity, 
        skinType 
    });


    // Execute Python script with JSON input as an argument
    exec(`python recommend.py "${inputJSON.replace(/"/g, '\\"')}"`, (error, stdout, stderr) => {
        if (error) {
            console.error("Exec Error:", error.message);
            return res.status(500).json({ error: "Error executing Python script" });
        }
    
        if (stderr) {
            console.warn("Python Stderr:", stderr);
        }
    
        console.log("Python Output:", stdout);  // Log Python's output to debug
    
        try {
            const recommendations = JSON.parse(stdout);
            console.log("Parsed Recommendations:", recommendations);  // Log parsed recommendations
    
            res.render("recommend.ejs", { recommendations }); // Pass recommendations to EJS
        } catch (err) {
            console.error("JSON Parsing Error:", err.message);
            res.status(500).json({ error: "Invalid JSON output from Python script" });
        }
    });
    
});

// Start the server
app.listen(port, () => {
    console.log(`Server started at port ${port}`);
});
