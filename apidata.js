const Shopify = require('shopify-api-node')
const {extract_data:ed} = require('./server.js')
const fs = require('fs');
const path = require('path');
const shopify = new Shopify({
    shopName: 'da7000.myshopify.com',
    accessToken: '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',
});
// api acess tokern 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
// key 032a85d3237ea1804e1240396a8458ab
// password 37c36588d6ea871ccece44f881ca45d4

const data_fetch = async () => {
    await shopify.order
        .list({ limit: 5 })
        .then((orders) => {
            ed(orders);
        
        })
        .catch((err) => {
            console.error("Error at data retrive", err)
        });
}

data_fetch()

// function load_data(file_name){
//     const loaded_data = fs.readFileSync(path.join(__dirname,'DataFiles',file_name),'utf-8')
//     return JSON.parse(loaded_data)
// }

// function save_data(file_name,json_data){
//     fs.writeFileSync(path.join(__dirname,'DataFiles',file_name),JSON.stringify(json_data,null,4))
//     console.log("content_saved");
// }

// const customer_data_json = (id,f_name,l_name,email,order_count,total_spent)=>{
//     var customer_data = {
//         "Customer_name":f_name+l_name,
//         "Customer_id":id,
//         "Email":email,
//         "Order_count":order_count,
//         "Total_spent":total_spent,
//         "Order_detials":[]
//     }
//     return customer_data
// }
// const order_data_json =(id,created_at,amount,order_number,discount)=>{
//     var order_data = {
//         "Order_id":id,
//         "Created_at":created_at,
//         "Total_cost":amount,
//         "Order_number":order_number,
//         "Discount":discount,
//     }
//     return order_data

// }
// const extract_data = (raw_data)=>{
//     data = raw_data.orders
//     index=0
//     console.log("process start")
//     const database = load_data('data.json')
//     try{
//         console.log("try_block")
//         console.log(data.length)
//         for(i=0;i<data.length;i++){
//             console.log(data[i])
//             var flag=true;
//             for(j=0;j<database.length;j++){
//                 if(data[i].Customer_id ==database[j].Customer_id){
//                     flag=false
//                     index=j
//                 }
//             }
//             console.log(flag)
//             if(flag){
//                 const customer_data = customer_data_json(data[i].Customer_id,data[i].Customer_name,
//                     data[i].Email,data[i].Order_count,data[i].Total_spent)
//                 const order_data = order_data_json(data[i].Order_id,data[i].Created_at,
//                     data[i].Total_cost,data[i].Order_number,data[i].Discount)
//                 database.push(customer_data)
//                 save_data('data.json', database)
//                 // database.Order_detials[index].push(order_data)
//                 // save_data('data.json', database)
//                 database[index].Order_detials.push(order_data)
//                 save_data('data.json',database)
//                 console.log(typeof database[index].Order_detials)
//                 console.log("data writen in data.json file")
            
//             }
//             else{
//                 const order_data = order_data_json(data[i].Order_id,data[i].Created_at,
//                     data[i].Total_cost,data[i].Order_number,data[i].Discount)
//                 database[index].Order_detials.push(order_data)
//                 save_data('data.json',database)
//                 console.log("data writen in data.json file")
//             }

//         }
//     }
//     catch (err){
//         console.error("Error at extract_data",err);
//     }
// }

