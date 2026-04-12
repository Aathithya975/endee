const axios = require("axios") // npm install axios

// Recommendation route
app.get("/api/recommend/:product", async (req, res) => {
    const product = req.params.product
    const response = await axios.get(`http://localhost:8000/recommend/${product}`)
    res.json(response.data)
})