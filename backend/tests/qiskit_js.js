const qasm = require("@qiskit/qasm");
const fs = require("fs");
const util = require("util");

console.log("Version");
console.log(qasm.version);

const parser = new qasm.Parser();

const circuit = fs.readFileSync("./example.qasm", "utf8");

console.log(util.inspect(parser.parse(circuit), { depth: null }));
