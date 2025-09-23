// import { Operation } from './operation.js';

// import { Tax } from './tax.js';

// function compute(outputFormatOnly = true) {
//     const operations = Operation;
//     console.log(operations);
//     const tax = Tax;
//     console.log(tax);


//     // Gross Profit
//     let grossProfit = 0.0;
//     for (let i = 0; i < operations.length; i++) {
//         const op = operations[i];
//         if (op.operation === 'buy') {
//             grossProfit = grossProfit - (op.unitCost * op.quantity);
//         } else if (op.operation === 'sell') {
//             grossProfit = grossProfit + (op.unitCost * op.quantity);
//         }
//     }

//     // Taxes
//     const minimalTax = grossProfit > 0;
//     let taxes = 0.0;
//     if (minimalTax) {
//         taxes = (grossProfit * tax.tax_value) + tax.fixedFee;

//     }

//     let liquidProfit = grossProfit - taxes;

//     //net profit
//     const netProfit = liquidProfit;
//     if (outputFormatOnly) {
//         return {
//             grossProfit: grossProfit,
//             taxes: taxes,
//             netProfit: netProfit,
//         }
//     } else {

//         throw new Error("Invalid output format")

//     }
// }

// export { compute };

import { Operation } from "./operation.js";
import { Tax } from './tax.js';

function compute(outputFormatOnly = true ){
    const operations = Operation;
    console.log("Operations",operations);
    const tax = Tax;
    console.log("Tax",tax);

    // Gross Profit
    let grossProfit = 0.0;
    let finalValue = 0.0;
    let finalValueBuy = 0.0;
    let finalValueSell = 0.0;
    for (let i = 0; i < operations.length; i++) {
        const op = operations[i];
        if (op.operation === 'buy') {
            grossProfit = grossProfit - (op.unitCost * op.quantity);
            finalValueBuy = (op.unitCost * op.quantity);



        } else if (op.operation === 'sell') {
            grossProfit = grossProfit + (op.unitCost * op.quantity);
            finalValueSell = op.unitCost ;
        }
        
    }
    //taxes
    let taxes = 0.0;
    let totalTaxes = 0.0;
    for(let i=0 ; i < tax.length; i++){
        const scope = tax[i].scope;
        if(scope === 'sell' && grossProfit > 0){
            taxes = (grossProfit * tax[i].tax) ;
            console.log("taxes dentro do scope sell", taxes)
            totalTaxes += taxes;
            

        } else if(scope == 'both' && grossProfit > 0){
            taxes = (operations.reduce((acc, op) =>{
                return acc + (op.unitCost * op.quantity);
            }, 0) * tax[i].tax);
            console.log("taxes dentro do scope both", taxes)
            totalTaxes += taxes;
        }
    }
    //liquid profit
    let netProfit = grossProfit - totalTaxes;
    finalValue = finalValueBuy + ((finalValueSell - operations[0].unitCost) * operations[0].quantity) - totalTaxes;

    // final value
   
    if (outputFormatOnly) {
        return {
            grossProfit: grossProfit,
            taxes: totalTaxes,
            netProfit: netProfit,
            finalValue: finalValue
        }
    }

}

export { compute };