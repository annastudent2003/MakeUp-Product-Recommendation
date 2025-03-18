import express from "express";
import bodyParser from "body-parser";

const port = 3000;

const app = express();

app.use(bodyParser.urlencoded({ extended: true }));

const products = [
    {
        imageLink1:"https://i.pinimg.com/1200x/24/27/d9/2427d952652461311a38b0847137c7d6.jpg" ,
        prodName1: "Foundation",
        imageLink2:"https://i.pinimg.com/1200x/04/ee/b4/04eeb4c7bd9159ce82aa8d9b2d0c0bf8.jpg" ,
        prodName2: "Face-powder",
        imageLink3:"https://i.pinimg.com/1200x/a2/36/cf/a236cf7cf0705b0b99215919d21e83f0.jpg" ,
        prodName3: "Concealer",
        route: "/makerec"
    },
    {
        imageLink1:"https://i.pinimg.com/1200x/24/5d/18/245d18c2ecdd07cb3c2fd9b579137f3f.jpg" ,
        prodName1: "Face-cream",
        imageLink2:"https://i.pinimg.com/1200x/1e/9c/b7/1e9cb779b927673fd2a83de4130f69da.jpg" ,
        prodName2: "Sunscreen",
        imageLink3:"https://i.pinimg.com/1200x/24/2f/21/242f2122d36621c8d057613ad9ec062a.jpg" ,
        prodName3: "Body-lotion",
        route: "/skinrec"
    }
]

const inputImg = [
    {
        imageLink:"https://i.pinimg.com/1200x/2c/d3/fb/2cd3fbb75ade740992cda2da4badb5b0.jpg",
        prodName: "makeup Image"
    },
    {
        imageLink:"https://i.pinimg.com/1200x/63/5b/be/635bbef049c34c492a6b8c0bea0ca3ab.jpg",
        prodName:"skincare Image"
    }]

app.get("/", (req, res) => 
{
    res.render("index.ejs");
})

app.get("/aboutus", (req, res) => 
{
    res.render("aboutus.ejs");
})

app.get("/skincare", (req, res) => 
{
    res.render("product.ejs",
        {
            product: products[1]
        }
    );
})

app.get("/makeup", (req, res) => 
{
    res.render("product.ejs",
        {
            product: products[0]
        }
    );
})

app.get("/skinrec", (req, res) => 
{
    res.render("recommend.ejs",{
        look: inputImg[1]
    });
})

app.get("/makerec", (req, res) =>
{
    res.render("recommend.ejs",{
        look: inputImg[0]
    })
})

app.listen(port, () => {
    console.log(`Server started at port ${port}`);
})