const express = require("express");
const os = require("os");
const path = require("path");
const fs = require("fs");
const bodyParser = require("body-parser");

const hostname = os.hostname();
const app = express();
const port = 8000;

const config_file = path.resolve(__dirname, "../config.txt");

app.use(express.static("static"));
app.use(bodyParser.json());

function readConfig() {
  try {
    return fs.readFileSync(config_file, "utf-8");
  } catch (err) {
    console.log(err);
    return null;
  }
}

function writeConfig(contents) {
  try {
    return fs.writeFileSync(config_file, contents);
  } catch (err) {
    console.log(err);
    return null;
  }
}

app.get("/", (req, res) => {
  res.sendFile("./index.html", { root: __dirname });
});

app.get("/alarm", (req, res) => {
  const config = readConfig();
  res.send(config);
});

app.post("/alarm", (req, res) => {
  console.log("Got body:", req.body);
  writeConfig(req.body.time);
  res.send("OK");
});

app.listen(port, () => {
  console.log(`Listening at http://${hostname}.local:${port}`);
});
