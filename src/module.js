function calculateDateDifference(date1, date2) {
    const differenceInMilliseconds = new Date(date2) - new Date(date1);
    return Math.floor(differenceInMilliseconds / (1000 * 60 * 60 * 24));
}

function calculateTotalLifeSpan(data){
    var Total_life_span=0;
    for(i=0;i<data.length;i++){
        var data_len = data[i].Order_detials.length;
        Total_life_span += calculateDateDifference(data[i].Order_detials[0].Created_at,data[i].Order_detials[data_len-1].Created_at);
        //console.log(avg_life_span)
    }
    return Total_life_span;
}

function calculateTotalSalesOrder(data){
    var total_sales=0,order_count=0;
    for(i=0;i<data.length;i++){
        order_count += data[i].Order_detials.length;
        for(j=0;j<data[i].Order_detials.length;j++){
            //console.log(data[i].Order_detials[j].Total_cost)
            total_sales += parseInt(data[i].Order_detials[j].Total_cost)
        }
    }
    return [total_sales,order_count];
}


module.exports = {
    calculateTotalLifeSpan,
    calculateTotalSalesOrder
};
