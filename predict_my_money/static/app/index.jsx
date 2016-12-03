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


class NewPortfolioView extends React.Component {
  constructor(props) {
    super(props);

    this.state = {}
    this.state.stocks = [
      { name: "AAPL", amount: "300", price_now: "120", price: "96" },
      { name: "YAHO", amount: "200", price_now: "40", price: "33" },
      { name: "MSFT", amount: "100", price_now: "60", price: "71" },
    ]
  }

  componentDidMount() {
    $.getJSON("/predictor/api/get_portfolio_plot?stock=aapl", (data) => {
      var points = [];
      var lastprice = 36000;
      for (var i=800; i<data.data.length; ++i) {
        if (i%5 == 0) {
          lastprice += (Math.random()-0.5)*100;
          data.data[i].close = lastprice;
          points.push(data.data[i])
        }
      }
      plotData(points, findDOMNode(this.refs.plot))
    })
  }

  render() {

    var stockList = this.state.stocks.map((e, i) => {
      return (
        <tr>
          <td>{ i+1 }</td>
          <td>{ e.name }</td>
          <td>{ e.amount }</td>
          <td>${ e.price }</td>
          <td><button className="btn btn-danger">Remove</button></td>
        </tr>
      )
    })

    return (
      <div className="container">
        <br />
        <h1>New Portfolio</h1>
        <form>
          <CsrfToken />

          <div className="row">
            <div className="col-sm-6">
              <div className="form-group">
                <label for="inputName">Name</label>
                <input type="email" className="form-control" id="inputName" aria-describedby="nameHelp" placeholder="Identify your portfolio" />
                <small id="nameHelp" className="form-text text-muted">Identify your portfolio.</small>
              </div>

              <hr />

              <form className="form-inline">
                <div className="form-group">
                  <label for="exampleInputName2">Get Recommendation for&nbsp;</label>
                  <input type="text" className="form-control" id="exampleInputName2" placeholder="how many dollars" />
                </div>

                <div className="form-group">
                  <label for="exampleInputName2">of type&nbsp;</label>

                  <select className="form-control" id="exampleSelect1">
                    <option>Control</option>
                    <option>Best Expected Return</option>
                    <option>Best Expected Return + Diversity</option>
                  </select>
                </div>
                &nbsp;

                <div className="form-group">
                  <button className="btn btn-info">Suggest</button>
                </div>
              </form>

              <hr />

              <button className="btn btn-primary btn-lg">
                Create Portfolio
              </button>
            </div>

            <div className="col-sm-6">
              <p>Predicted fluctuation</p>
              <div ref="plot" id="data-dump" data-prices="{{ data }}"></div>
            </div>

          </div>

          <br />

          <h3>Stocks currently in portolio</h3>

          <form id="add-stock" className="FormAddStock form-inline">
            <div className="form-group">
              <label for="exampleInputName2">Add to portfolio stock&nbsp;</label>
              <input type="text" className="form-control" id="exampleInputName2" placeholder="stock name" />
            </div>

            <div className="form-group">
              <label for="exampleInputName2">with amount&nbsp;</label>
              <input type="number" className="form-control" id="exampleInputName2" placeholder="amount of stock" />
            </div>

            <div className="form-group">
              <button className="btn btn-info">Add</button>
            </div>
          </form>

          <table className="table table-striped">
            <thead>
              <tr>
                <th>#</th>
                <th>Name</th>
                <th>Amount</th>
                <th>Price</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
            {stockList}
            </tbody>
          </table>
        </form>
      </div>
    )
  }
}

function plotData(data, el) {

  var margin = {top: 20, right: 50, bottom: 30, left: 50},
    width = $(el).width() - margin.left - margin.right,
    height = $(el).width()/2 - margin.top - margin.bottom;

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
    .y(function(d) { return y(d.close); })
    .curve(d3.curveBasis);

  var svg = d3.select(el).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  data.forEach(function(d) {
      d.date = parseDate(d.date);
      d.close = +d.close;
    });

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
    .attr("y", 4)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Price ($)");

  var path = svg.append("path")
    .datum(data)
    .attr("class", "line")
    .attr("d", line);

  var focus = svg.append("g")
    .attr("class", "focus")
    .style("display", "none");

  focus.append("circle")
    .attr("r", 4.5);

  focus.append("text")
    .attr("x", 9)
    .attr("dy", ".35em");

  svg.append("rect")
    .attr("class", "overlay")
    .attr("width", width)
    .attr("height", height)
    .on("mouseover", function() { focus.style("display", null); })
    .on("mouseout", function() { focus.style("display", "none"); })
    .on("mousemove", mousemove);

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
      var points = [];
      for (var i=0; i<data.data.length; ++i) {
        if (i%100) {
          points.push(data.data[i])
        }
      }
      plotData(points, findDOMNode(this))
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

class PortfolioView extends React.Component {
  constructor(props) {
    super(props);

    this.state = {};
  }

  componentDidMount() {
    $.getJSON("/predictor/api/get_portfolio_plot?stock=aapl", (data) => {
      var points = [];
      var lastprice = 36000;
      for (var i=800; i<data.data.length; ++i) {
        if (i%5 == 0) {
          lastprice += (Math.random()-0.5)*100;
          data.data[i].close = lastprice;
          points.push(data.data[i])
        }
      }
      plotData(points, findDOMNode(this.refs.plot))
    })
  }

  render() {
    var _stockList = [
      { name: "AAPL", amount: "300", price_now: "120", price: "96" },
      { name: "YAHO", amount: "200", price_now: "40", price: "33" },
      { name: "MSFT", amount: "100", price_now: "60", price: "71" },
    ]

    var stockList = _stockList.map((el, i) => {
      return <tr>
        <td>{ i+1 }</td>
        <td>{ el.name }</td>
        <td>{ el.amount }</td>
        <td>${ el.price_now }</td>
        <td>${ el.price }</td>
      </tr>
    })

    return (
      <div className="StockView">
        <h1>Portfolio #4</h1>
        <h6>Created 3 days ago by Daniel Keller.</h6>

        <div className="row">
          <div className="col-sm-4">
            <hr />
            <pre>
            <code>
              Diversity: .49
              <br />
              Current Value: $66,321
              <br />
              Original Value: $60,783
            </code>
            </pre>
            <hr />
          </div>
          <div className="col-sm-8">
            <div ref="plot" id="data-dump" data-prices="{{ data }}"></div>
          </div>
        </div>

        <hr />
        <div>
          <h2>Stocks in this portfolio</h2>
          <p>Here are the stocks that belong to this portfolio.</p>
          <table className="table table-striped">
            <thead>
              <tr>
                <th>#</th>
                <th>Name</th>
                <th>Amount</th>
                <th>Price</th>
                <th>Bought Price</th>
              </tr>
            </thead>
            <tbody>
            {stockList}
            </tbody>
          </table>
        </div>
      </div>
    )
  }
}


window.startPortfolioView = function() {
  render(<PortfolioView stock={window.data.stock} />, document.getElementById('app'));
}

window.startNewPortfolioView = function() {
  render(<NewPortfolioView stock={window.data.stock} />, document.getElementById('app'));
}

window.startStockView = function() {
  render(<StockView stock={window.data.stock} />, document.getElementById('app'));
}
