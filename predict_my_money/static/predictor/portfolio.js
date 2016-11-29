$(document).ready(function(){
    $("#add-stock").click(addStock);


    function addStock(e)
    {
        e.preventDefault();
        var ticker = $('#add-stock-ticker').val();
        var amount = $('#add-stock-amount').val();
        var hidden = $('#stock-tickers');

        //Add new table row to table for stock
        var tableBody = $('#stock-table-body');
        var tablerow = $("<tr id='" + ticker + "-row'></tr>");
        var tickerfortable = $("<td>" + ticker + "</td>");
        var amountfortable = $("<td>" + amount + "</td>");
        var deletebuttonfortable = $("<td><button class='delete-stock' data-amount='" + amount + "' id='" + ticker + "'>Delete</button></td>");
        tablerow.append(tickerfortable);
        tablerow.append(amountfortable);
        tablerow.append(deletebuttonfortable);
        tableBody.append(tablerow);
        //activate new delete button
        $('#' + ticker + '').click(deleteStock);

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
        var ticker = target.attr('id');

        //remove table row
        var row = $('#' + ticker + '-row');
        row.remove();

        //remove from hidden
        var hidden = $('#stock-tickers');
        var value = hidden.val()
        value = value.replace(ticker + ' ' + amount,'');
        hidden.val(value);
    }
});