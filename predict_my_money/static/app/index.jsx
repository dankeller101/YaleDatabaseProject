// index.jsx

import React from 'react';
import { render, findDOMNode } from 'react-dom';

class App extends React.Component {
  render() {
    return <p> Hello React!</p>;
  }
}

function CsrfToken() {
  let token = document.getElementsByTagName('meta')._csrf.getAttribute('content');
  return <input type='hidden' name='csrfmiddlewaretoken' value={token} />
}

// using jQuery
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(
          cookie.substring(name.length + 1)
          );
        break;
      }
    }
  }
  return cookieValue;
}

class NewPortfolioView extends React.Component {
  render() {
    return (
      <div>
        <h1>Create a Portfolio</h1>

        <h2>Recommendations</h2>
        <h3>Total spend</h3>
        <form action="recommend" method="post" id="recommend-form">
          <CsrfToken />
          <input type="text" name="total_spend" id="total_spend"/>
              <input type="hidden" name='type' id="type-recommend"/>
          <button id="control" value="control" class="recommend">
              Create A Control
          </button>
          <button id="tsr" value="tsr" class="recommend">
              Best Expected Return
          </button>
          <button id="diversity" value="diversity" class="recommend">
              Best Expected Return with Best Diversity
          </button>
        </form>

        <form action="{% url 'predictor:make_portfolio' %}" method="post">
            <CsrfToken />
            <h4>name</h4>
            <input type="text" name="name" />
            <h4>stock tickers and number</h4>
            <div id="stocks">
                <table id="stock-table">
                    <thead>
                        <tr><td>Ticker</td><td>Amount</td><td>Delete</td></tr>
                    </thead>
                    <tbody id="stock-table-body"></tbody>
                </table>
                <div id="add-stocks">
                    <h5>stock ticker</h5>
                    <input type="text" id="add-stock-ticker"/>
                    <h5>amount of stock</h5>
                    <input type="text" id="add-stock-amount"/>
                    <button id="add-stock">Add Stock</button>
                </div>
                <input type="hidden" name="stock-tickers" id="stock-tickers"/>
            </div>

            <input type="submit" value="create_portfolio" />
        </form>
      </div>
    )
  }
}

function doit(data, el) {
	console.log(data)

  var margin = {top: 20, right: 50, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

  var parseDate = d3.timeParse("%d-%b-%y"),
    bisectDate = d3.bisector(function(d) { return d.date; }).left,
    formatValue = d3.format(",.2f"),
    formatCurrency = function(d) { return "$" + formatValue(d); };

  var x = d3.scaleTime().range([0, width]);
  var y = d3.scaleLinear().range([height, 0]);

  var xAxis = d3.axisBottom().scale(x);
  var yAxis = d3.axisLeft().scale(y);

  var line = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.close); });

  var svg = d3.select(el).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  data.forEach(function(d) {
    d.date = parseDate(d.date);
    d.close = +d.close;
  }
  );

  data.sort(function(a, b) {
    return a.date - b.date;
  });

  x.domain([data[0].date, data[data.length - 1].date]);
  y.domain(d3.extent(data, function(d) { return d.close; }));

  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

  svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Price ($)");

  svg.append("path")
    .datum(data)
    .attr("class", "line")
    .attr("d", line);

  // var focus = svg.append("g")
  //   .attr("class", "focus")
  //   .style("display", "none");

  // focus.append("circle")
  //   .attr("r", 4.5);

  // focus.append("text")
  //   .attr("x", 9)
  //   .attr("dy", ".35em");

  // svg.append("rect")
  //   .attr("class", "overlay")
  //   .attr("width", width)
  //   .attr("height", height)
  //   .on("mouseover", function() { focus.style("display", null); })
  //   .on("mouseout", function() { focus.style("display", "none"); })
  //   .on("mousemove", mousemove);

  function mousemove() {
    var x0 = x.invert(d3.mouse(this)[0]),
        i = bisectDate(data, x0, 1),
        d0 = data[i - 1],
        d1 = data[i],
        d = x0 - d0.date > d1.date - x0 ? d1 : d0;
    focus.attr("transform", "translate(" + x(d.date) + "," + y(d.close) + ")");
    focus.select("text").text(formatCurrency(d.close));
  }
}

class StockView extends React.Component {
  constructor(props) {
    super(props);
    
    this.state = {};
    // this.state.
  }

	componentDidMount() {
		$.getJSON("/predictor/api/get_stock_plot?stock=aapl", (data) => {
      doit(data.data, findDOMNode(this))
    })
	}

	render() {
		return (
			<div className="StockView">
				<h1>{this.props.stock}</h1>

				<div id="data-dump" data-prices="{{ data }}"></div>

			</div>
		)
	}
}


window.startNewPortfolioView = function() {
  render(<NewPortfolioView stock={window.data.stock} />, document.getElementById('app'));
}

window.startStockView = function() {
  render(<StockView stock={window.data.stock} />, document.getElementById('app'));
}
