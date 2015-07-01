$(document).ready(function () {
    $("#addCatg").click(function () {
        var catg_name = document.getElementById('inputTitle').value;
        
        if (catg_name.length == 0) {
            alert("Hey there - Category Name cannot be blank. Please name it ! ");
            return false;
        } 
    });
    $("#addProduct").click(function () {
        var product_name = document.getElementById('inputTitle').value;
        
        if (product_name.length == 0) {
            alert("Hey there - Category Name cannot be blank. Please name it ! ");
            return false;
        }
    });
});

