const fs = require('fs')
const path = require('path')
const fspromise = require('fs').promises

function loadjson_data(file_name){
    try{
        const data = fs.readFileSync(path.join(__dirname,'DataFiles',file_name),'utf-8')
        return JSON.parse(data)
    }
    catch(err){
        console.log("Error in loadjson",err)
    }
}

function savejson(file_name,dataline){
    try{
        fs.writeFileSync(path.join(__dirname,'DataFiles',file_name),JSON.stringify(dataline))
        console.log("data wrired")
    }
    catch (err){
        console.error(err);
    }
}
const fileOps = ()=>{  
    try{
        const rawdata=loadjson_data('raw.json').orders
        const database=loadjson_data('data.json')
        for(i=0;i<rawdata.length;i++){
            const specified_data={}
            specified_data['Name']=rawdata.first_name+rawdata.last_name;
            specified_data['Customer_id']=rawdata.customer.id;
            specified_data['Email']=rawdata.customer.email;
            specified_data['Order_count']=rawdata.customer.orders_count;
            specified_data['Total_spend']=rawdata.customer.total_spend
            specified_data['Order_detials']={}
            specified_data.Order_detials['Order_id']=rawdata.id;
            specified_data.Order_detials['Created_at']=rawdata.created_at;
            specified_data.Order_detials['Total_price']=rawdata.current_total_price;
            specified_data.Order_detials['Order_Number']=rawdata.order_Number;
            specified_data.Order_detials['Discount']=rawdata.discount;

            database.push(specified_data);
        }
        savejson('data.json', database);
    }
    catch (err){
        console.error("Error in fileOps",err);
    }
}

fileOps()

process.on('uncaughtException',err=>{
    console.log("Error",err);
    process.exit(0);
})