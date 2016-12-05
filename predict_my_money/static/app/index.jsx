// index.jsx

import React from 'react';
import { render, findDOMNode } from 'react-dom';

import NewPortfolioView from './pages/NewPortfolio.jsx';
import PortfolioView from './pages/Portfolio.jsx';
import PortfolioCompareView from './pages/PortfolioCompare.jsx';
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
		$.getJSON("/predictor/api/get_stock_plot?name="+this.props.stock.name, (data) => {
      if (data.error) {
        alert('Stock not found.')
        return;
      }
      var points = [];
      for (var i=0; i<data.data.length; ++i) {
        if (i%5) {
          points.push(data.data[i])
        }
      }
      plotData(points, findDOMNode(this.refs.plot))
    })
	}

	render() {
		return (
			<div className="StockView">
				<h1>Plotting stock '{this.props.stock.name}'</h1>

				<div id="data-dump" ref='plot' data-prices="{{ data }}"></div>
			</div>
		)
	}
}



window.startPortfolioCompareView = function() {
  render(<PortfolioCompareView data1={window.data.portfolio1} data2={window.data.portfolio2}/>,
    document.getElementById('app'));
}

window.startPortfolioView = function() {
  render(<PortfolioView data={window.data.portfolio} />, document.getElementById('app'));
}

window.startHomeView = function() {
  render(<HomeView />, document.getElementById('app'));
}

window.startNewPortfolioView = function() {
  render(<NewPortfolioView />, document.getElementById('app'));
}

window.startStockView = function() {
  render(<StockView stock={window.data.stock} />, document.getElementById('app'));
}
