const path = require('path')
const { loadData } = require(path.join(__dirname,'src','data_load.js'));
const { calculateTotalLifeSpan, calculateTotalSalesOrder } = require(path.join(__dirname,'src','module.js'));

const data = loadData(path.join(__dirname, 'DataFiles', 'data.json'));

const avgLifeSpan = calculateTotalLifeSpan(data) / data.length / (30 * 2);
console.log("AVG_LIFE_SPAN:", avgLifeSpan);

const [totalSales, orderCount] = calculateTotalSalesOrder(data);
const avgOrderValue = totalSales / orderCount;
console.log("AVG_ORDER_VALUE:", avgOrderValue);

const avgPurchaseFrequency = orderCount / data.length;
console.log("AVG_PURCHASE_FREQUENCY:", avgPurchaseFrequency);

const LTV = avgLifeSpan * avgOrderValue * avgPurchaseFrequency;
console.log("LTV:", Math.round(LTV));
