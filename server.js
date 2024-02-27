const fs = require('fs')
const path = require('path')
//const { loadData } = require(path.join(__dirname,'src','data_load.js'));
function load_data(file_name){
    const loaded_data = fs.readFileSync(path.join(__dirname,'DataFiles',file_name),'utf-8')
    return JSON.parse(loaded_data)
}

function save_data(file_name,json_data){
    fs.writeFileSync(path.join(__dirname,'DataFiles',file_name),JSON.stringify(json_data,null,4))
    console.log("content_saved");
}

const customer_data_json = (id,created_at,total_spent)=>{
    var customer_data = {
        "Customer_id":id,
        "Created_at":created_at,
        "Total_spent":total_spent,
        "Order_detials":[]
    }
    return customer_data
}
const order_data_json =(id,created_at,amount,discount)=>{
    var order_data = {
        "Order_id":id,
        "Created_at":created_at,
        "Total_cost":amount,
        "Discount":discount,
    }
    return order_data

}
const extract_data = (data)=>{
    index=0
    total_spent=0
    console.log("process start")
    const database = load_data('data.json')
    try{
        console.log("try_block")
        console.log(data.length)
        for(i=0;i<data.length;i++){
            var flag=true;
            for(j=0;j<database.length;j++){
                if(data[i].customer.id == database[j].Customer_id){
                    flag=false
                    index=j
                }
            }
            console.log(flag)
            if(flag){
                const customer_data = customer_data_json(
                    data[i].customer.id,
                    data[i].customer.created_at,
                    total_spent
                );
                const order_data = order_data_json(
                    data[i].id,
                    data[i].created_at,
                    data[i].current_subtotal_price,
                    data[i].current_total_discounts
                );
            
                database.push(customer_data)
                save_data('data.json', database)

                database[index].Order_detials.push(order_data)
                save_data('data.json',database)
                console.log("data writen in data.json file")
            
            }
            else{
                const order_data = order_data_json(
                    data[i].id,
                    data[i].created_at,
                    data[i].current_subtotal_price,
                    data[i].current_total_discounts
                );
                database[index].Order_detials.push(order_data);
                
                save_data('data.json',database);
                console.log("data writen in data.json file");
                database[index].Order_count += database[index].Order_detials.length;
            }
            total_spent+= parseInt(data[i].current_subtotal_price)
            database[index].Order_count = database[index].Order_detials.length
            database[index].Total_spent = total_spent;
            console.log(database[index].Order_detials.length)
            console.log(total_spent)
        }
    }
    catch (err){
        console.error("Error at extract_data",err);
    }
}

module.exports = {extract_data}

