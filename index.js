const express = require("express");
const fileUpload = require("express-fileupload");
const pdfParse = require("pdf-parse");

const app = express();

// Serve static files from the "public" directory
app.use("/", express.static("public"));

// Enable file upload functionality
app.use(fileUpload());

// Handle POST request to "/extract-text"
app.post("/extract-text", (req, res) => {
    // Check if the request contains a PDF file
    if (!req.files || !req.files.pdfFile) {
        // If no PDF file is provided, respond with 400 Bad Request
        res.status(400);
        res.end();
    }

    // Parse the content of the PDF file
    pdfParse(req.files.pdfFile).then(result => {
        // Send the extracted text as the response
        res.send(result.text);
    });
});

// Start the server on port 3000
app.listen(3000);
