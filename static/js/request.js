function showMoreCards(productsLength) {
    for(var i=3; i<productsLength; i++){
        document.getElementById("card" + i).classList.remove("hide");
        document.getElementById("card" + i).classList.add("show-card");
    }
    document.getElementById("show-more").classList.remove("show-button");
    document.getElementById("show-more").classList.add("hide");
    document.getElementById("show-less").classList.remove("hide");
    document.getElementById("show-less").classList.add("show-button");
}

function showLessCards(productsLength) {
    for(var i=3; i<productsLength; i++){
        document.getElementById("card" + i).classList.remove("show-card");
        document.getElementById("card" + i).classList.add("hide");
    }
    document.getElementById("show-more").classList.remove("hide");
    document.getElementById("show-more").classList.add("show-button");
    document.getElementById("show-less").classList.remove("show-button");
    document.getElementById("show-less").classList.add("hide");
}

function setFrame() {     
    var keywords = document.getElementById("keywords").value;
    var minPrice = document.getElementById("from").value;
    var maxPrice = document.getElementById("to").value;

    if(maxPrice < minPrice){
        window.alert("Min price cannot be greater than max price. Please provide new values.");
        return false;
    }

    var conditionNew = document.getElementById("new").checked;
    var conditionUsed = document.getElementById("used").checked;
    var conditionVeryGood = document.getElementById("very good").checked;
    var conditionGood = document.getElementById("good").checked;
    var conditionAcceptable = document.getElementById("acceptable").checked;
    var returnAccepted = document.getElementById("return").checked;
    var freeShipping = document.getElementById("free").checked;
    var expeditedShipping = document.getElementById("expedited").checked;
    var sortOrder = document.getElementById("sortby").value;

    var queryParams = '?keywords='+keywords+'&min_price='+minPrice+'&max_price='+maxPrice

    if(typeof conditionNew !== 'undefined'){
        queryParams += '&condition_new=' + conditionNew;
    }

    if(typeof conditionUsed !== 'undefined'){
        queryParams += '&condition_used=' + conditionUsed;
    }

    if(typeof conditionVeryGood !== 'undefined'){
        queryParams += '&condition_very_good=' + conditionVeryGood;
    }

    if(typeof conditionGood !== 'undefined'){
        queryParams += '&condition_good=' + conditionGood;
    }

    if(typeof conditionAcceptable !== 'undefined'){
        queryParams += '&condition_acceptable=' + conditionAcceptable;
    }

    if(typeof returnAccepted !== 'undefined'){
        queryParams += '&return_accepted=' + returnAccepted;
    }

    if(typeof freeShipping !== 'undefined'){
        queryParams += '&free_shipping=' + freeShipping;
    }

    if(typeof expeditedShipping !== 'undefined'){
        queryParams += '&expedited_shipping=' + expeditedShipping;
    }

    if(typeof sortOrder !== 'undefined'){
        queryParams += '&sort_order=' + sortOrder;
    }


    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var json_response = JSON.parse(xhr.responseText);
            var items = json_response.searchResult.item;
            var totalEntries = json_response.paginationOutput.totalEntries;
            var productImage;
            var divId;
            var htmlCode = "";

            if(typeof items !== 'undefined'){
                htmlCode += '<div class="title">' + totalEntries + ' Results found for ' + keywords + '</div>';

                for (var i=0; i<items.length; i++) {

                    if(items[i].galleryURL == 'https://thumbs1.ebaystatic.com/pict/04040_0.jpg'){
                        productImage = '/static/img/ebay_default.jpg';
                    } else {
                        productImage = items[i].galleryURL;
                    }

                    if(i < 3){
                        divId = 'show-card';
                    } else {
                        divId = 'hide';
                    }

                    htmlCode += '<div id="card'+i+'" class="' + divId + '"><div class="image"><img src="' + productImage + '"></div><div id="description"><p><a href="' + items[i].viewItemURL[0] + '">' + items[i].title[0] + '</a></p><p>Category: ' + items[i].primaryCategory[0]['categoryName'] + '</p><p>Condition: ' + items[i].condition[0].conditionDisplayName[0] + '</p><p><b>Price: $' + items[i].sellingStatus[0].currentPrice[0].__value__ + '</b> From <i>' + items[i].location[0] + '</i></p></div></div>';
                }

                if(items.length > 3){
                    htmlCode += '<div class="show-button" id="show-more"><button type="button" onclick="showMoreCards('+ items.length +');">Show More</button></div> \
                                 <div class="hide" id="show-less"><button type="button" onclick="showLessCards('+ items.length +');">Show Less</button></div>'
                }

            } else {
                htmlCode += '<div class="title">No results found</div>'
            }

            document.getElementById("results").innerHTML = htmlCode;
        }
    }

    xhr.open("GET", "http://localhost:5000/api/v1.0/search" + queryParams, false);
    xhr.send();
}

function clearResults(){
    document.getElementById("results").innerHTML = "";
    return false;
}