const { json } = require('express')
const fs=require('fs')
const path = require('path')

const express=require('express')

const app =express()
const Shopify = require('shopify-api-node')

const shopify = new Shopify({
    shopName:'onstoreproject.myshopify.com',
    accessToken:'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'
})

const data = async () =>{
    try{
        const jsonfile = await shopify.product.list({limit:5}).then((products) => console.log(products)).catch ((err)=> console.log(err))
        console.log(jsonfile)
    }catch (err){
        console.log(err)
    }
}

data()

// Api new access key - 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

// // Api inte link sytx : https://apikey:apitoken@storename/admin/api/2022-10/orders.json

// fs.readFile(path.join(__dirname,'DataFiles','data.json'),'utf-8',(err, data) =>{
//     if (err) throw err;
//     try{
//         const JsonData = JSON.parse(data);
//         console.log(JsonData.name);
//     }
//     catch (err){
//         console.error("Error in parse",err)
//     }

// })


// const newData ={
//     "name":"Karthick",
//     "orders":20,
//     "address":"Karpagam Academy of Higher Education",
// }

// fs.appendFile(path.join(__dirname,'DataFiles','data.json'),JSON.stringify(newData ,null,2), err=>{
//     if (err) throw err;
//     console.log("file Writed...")
// })

// fs.readFile(path.join(__dirname,'DataFiles','data.json'),'utf-8',(err,data)=>{
//     if (err) throw err
//     const jsondata=JSON.parse(data)
//     console.log(jsondata.order)
//     jsondata.order+=1
//     fs.writeFile(path.join(__dirname,'DataFiles','data.json'),JSON.stringify(jsondata, null ,4),err=>{
//         if(err) throw err;
//         console.log("data writed...")
//     })
// })

process.on('uncaughtException',err=>{
    console.error("Erroer",err);
    process.exit(1);
})