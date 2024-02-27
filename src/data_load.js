const fs = require('fs');
const path = require('path');

function loadData(filePath){
    const rawData = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(rawData);
}

function save_data(file_name,json_data){
    fs.writeFileSync(path.join(__dirname,'DataFiles',file_name),JSON.stringify(json_data,null,4))
    console.log("content_saved");
}

module.exports = {
    loadData,
    save_data
};
