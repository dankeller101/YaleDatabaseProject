$(document).ready(function(){
    $("#add-stock").click(addStock);

    $('.recommend').click(getRecommendation);

    function getRecommendation(e)
    {
        e.preventDefault();
        var button = $(e.currentTarget);
        var type = $('#type-recommend');
        type.val(button.val());
        var form = $('#recommend-form');
        $.post(form.attr('action'), form.serialize(), function(json){
            $.each(json, function(stock, amount) {
                addStockDOM(stock, amount);
            });
        });
    }


    function addStockDOM(ticker, amount)
    {
        //Add new table row to table for stock
        var tableBody = $('#stock-table-body');
        var tablerow = $("<tr class='" + ticker + "-row'></tr>");
        var tickerfortable = $("<td>" + ticker + "</td>");
        var amountfortable = $("<td>" + amount + "</td>");
        var deletebuttonfortable = $("<td><button data-amount='" + amount + "' class='" + ticker + "'>Delete</button></td>");
        tablerow.append(tickerfortable);
        tablerow.append(amountfortable);
        tablerow.append(deletebuttonfortable);
        tableBody.append(tablerow);
        //activate new delete button
        $('.' + ticker + '').click(deleteStock);
    }


    function addStock(e)
    {
        e.preventDefault();
        var ticker = $('#add-stock-ticker').val();
        var amount = $('#add-stock-amount').val();
        var hidden = $('#stock-tickers');

        addStockDOM(ticker, amount);

        //update current value in hidden
        var currentvalue = hidden.val();
        currentvalue = currentvalue + " " + ticker + " " + amount;
        hidden.val(currentvalue);
    }

    function deleteStock(e)
    {
        e.preventDefault();

        //get info
        var target = $(e.currentTarget);
        var amount = target.attr('data-amount');
        var ticker = target.attr('class');

        //remove table row
        var row = $('.' + ticker + '-row');
        row.remove();

        //remove from hidden
        var hidden = $('#stock-tickers');
        var value = hidden.val()
        value = value.replace(ticker + ' ' + amount,'');
        hidden.val(value);
    }
});

