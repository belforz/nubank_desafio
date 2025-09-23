import path from "node:path";
import fs, { read } from "node:fs";
import { compute } from "./lib/compute.js";
import { validate } from "./lib/validation.js";

function readJson(inputPath){
    const p = path.resolve(process.cwd(), inputPath);
    return JSON.parse(fs.readFileSync(p, 'utf-8'));
}

function main(){
    const inputPath = process.argv[2] || 'input.json'
    const input = readJson(inputPath);
    console.log("input antes da validação", input);

    validate(input);
    console.log("input depois da validação", input);


    const out = compute(input);
    console.log(JSON.stringify(out, null, 2));
}

main();