import fs from 'fs';

const inputPath = new URL('../input.json', import.meta.url);
let Tax = [{ tax:0.0, name: '', scope: '', assetClassScope: [] }];
try {
    const raw = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
    const rawTaxes = Array.isArray(raw.taxes) ? raw.taxes : [];
    Tax = rawTaxes.map(rawTax => {
        const tax = (typeof rawTax.tax === 'number') ? rawTax.tax : 0.0;
        const scope = (typeof rawTax.scope === 'string') ? rawTax.scope : '';
        const assetClassScope = Array.isArray(rawTax.assetClassScope) ? rawTax.assetClassScope : [];
        const name = (typeof rawTax.name === 'string') ? rawTax.name : '';

        return { tax, scope, assetClassScope, name };
    });
} catch (e) {
    console.error('Failed to load taxes from input.json:', e);
}

function executeTax(){
    console.log('Tax something');
}

export {Tax, executeTax};