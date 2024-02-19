const express = require('express')
const path = require('path')
const fs = require('fs')
const fspromise = require('fs').promises
const Shopify = require('shopify-api-node')

const app = express();
const shopify = new Shopify({
    shopName: 'da7000.myshopify.com',
    accessToken: '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',
    apiVersion:'2024-10'
})
// madhanprasath 

const funOps = async () => {
    try {
        const data = await shopify.product.list({limit:5})
        seprate_json(data)
    }
    catch (err) {
        console.error("Error in data fetching", err)
    }

}


funOps();


// Api new access key - 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
// password - f8006e1c39b7e2abe13334873db4feb7
// api key - 7a03cd3e8beecc741cf79ff783cd102a

// da7000.myshopify.com

//https://038099fc9e63fd9c3a5150e01315288e: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@da7000.myshopify.com/admin/api/2022-10/orders.json



// specified_data['Name']=rawdata.first_name+rawdata.last_name;
//             specified_data['Customer_id']=rawdata.customer.id;
//             specified_data['Email']=rawdata.customer.email;
//             specified_data['Order_count']=rawdata.customer.orders_count;
//             specified_data['Total_spend']=rawdata.customer.total_spend
//             specified_data['Order_detials']=[]
//             specified_data.Order_detials['Order_id']=rawdata.id;
//             specified_data.Order_detials['Created_at']=rawdata.created_at;
//             specified_data.Order_detials['Total_price']=rawdata.current_total_price;
//             specified_data.Order_detials['Order_Number']=rawdata.order_Number;
//             specified_data.Order_detials['Discount']=rawdata.discount;
