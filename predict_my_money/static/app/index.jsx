// index.jsx

import React from 'react';
import { render, findDOMNode } from 'react-dom';

import NewPortfolioView from './pages/NewPortfolio.jsx';
import HomeView from './pages/Home.jsx';
import CsrfToken from './lib/csrf.jsx';
import { plotData, plotMultipleData } from './lib/plot';

class App extends React.Component {
  render() {
    return <p> Hello React!</p>;
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


class PortfolioCompareView extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    // this.state.
  }

  componentDidMount() {
    $.getJSON("/predictor/api/get_portfolio_plot?stock=aapl", (data) => {
      var points0 = [], points1 = [];
      var lastprice0 = 0, lastprice1 = 0;
      for (var i=800; i<data.data.length; ++i) {
        if (i%5 == 0) {
          lastprice0 += (Math.random()-0.5);
          lastprice1 += (Math.random()-0.5);
          points0.push({ date: data.data[i].date, close: lastprice0 })
          points1.push({ date: data.data[i].date, close: lastprice1 })
        }
      }

      console.log(points0)
      console.log(points1)
      plotMultipleData(points0, points1, findDOMNode(this.refs.graph))
    })
  }

  render() {
    var _stockList0 = [
      { name: "AAPL", amount: "300", price_now: "120", price: "96" },
      { name: "YAHO", amount: "200", price_now: "40", price: "33" },
      { name: "MSFT", amount: "100", price_now: "60", price: "71" },
    ]

    var stockList0 = _stockList0.map((el, i) => {
      return <tr>
        <td>{ i+1 }</td>
        <td>{ el.name }</td>
        <td>{ el.amount }</td>
        <td>${ el.price_now }</td>
        <td>${ el.price }</td>
      </tr>
    })

    var _stockList1 = [
      { name: "YALE", amount: "300", price_now: "120", price: "96" },
      { name: "MSFT", amount: "60", price_now: "60", price: "71" },
    ]

    var stockList1 = _stockList1.map((el, i) => {
      return <tr>
        <td>{ i+1 }</td>
        <td>{ el.name }</td>
        <td>{ el.amount }</td>
        <td>${ el.price_now }</td>
        <td>${ el.price }</td>
      </tr>
    })

    return (
      <div className="StockView container">
        <br />
        <h1>Compare <abbr>portfolio #1</abbr> and <abbr>portfolio #2</abbr></h1>
        <h1>{this.props.stock}</h1>


        <div className="row">
          <div className="col-sm-6">
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
              {stockList0}
              </tbody>
            </table>
          </div>
          <div className="col-sm-6">
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
              {stockList1}
              </tbody>
            </table>
          </div>
        </div>

        <div id="data-dump" ref="graph" data-prices="{{ data }}"></div>

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

console.log(NewPortfolioView)

window.startPortfolioView = function() {
  render(<PortfolioView stock={window.data.stock} />, document.getElementById('app'));
}

window.startHomeView = function() {
  render(<HomeView />, document.getElementById('app'));
}

window.startNewPortfolioView = function() {
  render(<NewPortfolioView stock={window.data.stock} />, document.getElementById('app'));
}

window.startStockView = function() {
  render(<StockView stock={window.data.stock} />, document.getElementById('app'));
}

window.startPortfolioCompareView = function() {
  render(<PortfolioCompareView stock={window.data.stock} />, document.getElementById('app')); 
}
