const fs = require("fs");
const path = require("path");
const FileType = require("file-type");
const { v4: uuidv4 } = require("uuid");

const express = require("express");
const router = express.Router();

const multer = require("multer");


const {
  registerAgent,
  updateAgentDetails,
  createRecording,
} = require("./../utils/database");

const authAgent = require("../middleware/authagent");

const storage = multer.diskStorage({
  
  filename: (req, file, cb) => {
    console.log("holi voy a crear un fichero UwU");
    cb(null, uuidv4());
  },
  destination: (req, file, cb) => {
    cb(null, "./uploads");
  },
});

const multerUpload = multer({
  storage: storage,
  fileFilter: (req, file, cb) => {
    if (
      file.mimetype === "audio/wave" &&
      path.extname(file.originalname) === ".wav"
    ) {
      console.log("=====AQUIIII===");
      cb(null, true);
    } else {
      return cb(null, false);
    }
  },
});

router.get("/agents/register", async (req, res) => {
  res.status(200).json(await registerAgent());
});

router.get("/agents/check/:identifier/:token", authAgent, (req, res) => {
  res.sendStatus(200);
});

router.post(
  "/agents/details/:identifier/:token",
  authAgent,
  async (req, res) => {
    const { hostname, platform, arch } = req.body;
    if (!hostname || !platform || !arch) return res.sendStatus(400);
    await updateAgentDetails(req.params.identifier, hostname, platform, arch);
    res.sendStatus(200);
  }
);

router.post(
  "/agents/upload/:identifier/:token",
  authAgent,
  multerUpload.single("recording"),
  async (req, res) => {
    console.log(req.file);
    if (!req.file) return res.sendStatus(400);
    console.log("Magooo: ", req.file.filename);
    const filepath = path.join("./uploads/", req.file.filename);
    const fileInfo = await FileType.fromFile(filepath)

    try {
      console.log(fileInfo);

      if(fileInfo.ext != 'wav') {
        fs.unlinkSync(filepath);
        return res.sendStatus(400);
      }
      console.log("holi");
      
      await createRecording(req.params.identifier, req.file.filename);
      res.send(req.file.filename);
    }
    catch {
      fs.unlinkSync(filepath);
      return res.sendStatus(400);
    }

    
  }
);

module.exports = router;
