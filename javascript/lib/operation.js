import fs from 'fs';

const inputPath = new URL('../input.json', import.meta.url);
let Operation = [{operation:'', unitCost: 0, quantity: 0, assetClass: []}];

try {
    const raw = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
    if (Array.isArray(raw.operations)) Operation = raw.operations;

    
} catch (e) {

    Operation = [];
}

function executeOperation (){
    console.log('Operation executed');
}

export { Operation, executeOperation };