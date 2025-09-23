function validate(input){
    if(!input || !Array.isArray(input.operations) || input.operations.length !==2){
        throw new Error("Invalid operations format")
    }

    const[buyOp, sellOp] = input.operations;
    if(buyOp.operation !== 'buy' || sellOp.operation !== 'sell'){
        throw new Error("Invalid operations format");
    }

    for(const tax of input.taxes){
        if(typeof tax.tax !== 'number' || tax.tax < 0){
            throw new Error("Invalid tax format");
        }
    }

}

export {validate};