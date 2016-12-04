// pages/NewPortfolio.jsx

import React from 'react'
import { findDOMNode } from 'react-dom'
import _ from 'lodash'
import { plotData, plotMultipleData } from '../lib/plot';

import CsrfToken from '../lib/csrf.jsx';

class PortfolioEditor extends React.Component {
	constructor(props) {
		super(props)
		this.state = { stocks: [{ name: 'AAPL', amount: 3 }] }
	}

	resetStocks(rows) {
		var stocks = [];
		_.each(rows, (el) => {
			console.log(el)
			stocks.push({
				name: el[0].toUpperCase(),
				amount: el[1],
				price: el[2],
			})			
		})
		this.setState({ stocks: stocks })
	}

	getStocks() {
		return this.state.stocks
	}

	_onClickAdd() {
		var name = findDOMNode(this.refs.name).value.toUpperCase()
		var amount = parseInt(findDOMNode(this.refs.amount).value)

		if (name.length == 0) {
			alert('Invalid stock name.')
			return
		}

		if (amount < 0) {
			alert('Invalid amount.')
			return
		}

		findDOMNode(this.refs.name).value = findDOMNode(this.refs.amount).value = ''

		var found = _.find(this.state.stocks, { name: name })
		if (found) {
			found.amount += amount
			this.setState({ stocks: this.state.stocks })
			this.props.onUpdate(this.state.stocks)
			return
		}

		$.getJSON("/predictor/api/get_stock?name="+name, (data) => {
			if (data.error) {
				alert('Stock not found.')
				return;
			}

			this.state.stocks.push({
				name: name,
				amount: amount,
				price: data.current_adjusted_close
			})

			this.props.onUpdate(this.state.stocks)
		})
	}

	render() {
		var stockList = this.state.stocks.map((e, i) => {
			var remove = () => {
				_.remove(this.state.stocks, { name: e.name })
				console.log(this.state.stocks)
				this.setState({ stocks: _.remove(this.state.stocks, { name: e.name })})
				console.log(this.state.stock)
			}

			return (
				<tr key={ e.name }>
					<td>{ i+1 }</td>
					<td>{ e.name }</td>
					<td>{ e.amount }</td>
					<td>${ e.price }</td>
					<td><button className="btn btn-danger" onClick={remove}>Remove</button></td>
				</tr>
			)
		})

		return (
			<div className="PortfolioEditor">
				<h1>Portfolio manager</h1>

				<form id="add-stock" className="FormAddStock form-inline">
					<div className="form-group">
						<label for="exampleInputName2">Add to portfolio stock</label>
						<input type="text" ref="name" className="form-control" id="exampleInputName2" placeholder="stock name" />
					</div>

					<div className="form-group">
						<label for="exampleInputName2">with amount</label>
						<input type="number" ref="amount" className="form-control" id="exampleInputName2" placeholder="amount of stock" />
					</div>

					<div className="form-group">
						<button className="btn btn-info" onClick={this._onClickAdd.bind(this)}>Add</button>
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
			</div>
		)
	}
}

class Plot extends React.Component {
	updateStocks(_stocks) {
		var stocks = _.keyBy(_stocks, 'name');

		$.getJSON("/predictor/api/gen_portfolio_price_plot?stocks="+encodeURIComponent(JSON.stringify(stocks)),
		 (data) => {
			if (!data) {
				return;
			}

			var points = [];
			for (var i=0; i<data.data.length; ++i) {
				var row = data.data[i];
				console.log(row);
				// points.push({
				// 	// name: "",
				// 	// name: "",
				// 	// name: "",
				// });
			}

			// var points = []
			// var lastprice = 36000
			// for (var i=800; i<data.data.length; ++i) {
			// 	if (i%5 == 0) {
			// 		lastprice += (Math.random()-0.5)*100
			// 		data.data[i].close = lastprice
			// 		points.push(data.data[i])
			// 	}
			// }

			plotData(points, findDOMNode(this.refs.plot))
		})

	}

	render() {
		return (
			<div className="NewPortfolioPlot">
				<div ref="plot" id="data-dump"></div>
			</div>
		)
	}
}

export default class NewPortfolioView extends React.Component {
	constructor(props) {
		super(props)
		this.state = { stocks: [] }
	}

	_onUpdateStocks() {
		var stocks = this.refs.pmanager.getStocks()
		this.setState({ stocks: stocks })
		this.refs.plot.updateStocks(stocks)
	}

	_onClickSave() {
		let data = {
			name: findDOMNode(this.refs.fname).value,
			_stocks: JSON.stringify(this.state.stocks)
		}

		if (data.name.replace(/\s/, '').length == 0) {
			alert('Please choose a name for this portfolio')
			return
		}

		$.post("/predictor/api/portfolios", data, (data) => {
			if (data.error) {
				alert(data.message)
				return
			}

			location.href = "/predictor/"
		})
	}

	_onClickGetRecom() {
		this.refs.pmanager.resetStocks()
		let data = {
			type: findDOMNode(this.refs.ftype).value,
			total_spend: parseInt(findDOMNode(this.refs.fbconst).value)
		}

		$.getJSON("/predictor/api/get_recommendation", data, (data) => {
			if (data.error) {
				alert(data.message)
				return
			}

			this.refs.pmanager.resetStocks(data.data)
		})
	}

	componentDidMount() {
	}

	render() {
		return (
			<div className="container">
				<br />
				<h1>New Portfolio</h1>

				<div className="row">
					<div className="col-sm-6">
						<div className="form-group">
							<label for="inputName">Name</label>
							<input type="text" ref="fname" className="form-control" id="inputName" aria-describedby="nameHelp" placeholder="Identify your portfolio" />
							<small id="nameHelp" className="form-text text-muted">Identify your portfolio.</small>
						</div>

						<hr />

						<div className="form-group">
							<label for="exampleInputName2">Get Recommendation for</label>
							<input type="text" className="form-control" ref="fbconst" id="exampleInputName2" placeholder="how many dollars" />
						</div>

						<div className="form-group">
							<label for="exampleInputName2">of type</label>

							<select className="form-control" ref='ftype' id="exampleSelect1">
								<option value='random'>Control</option>
								<option value='high_return'>Best Expected Return</option>
								<option value='diverse'>Best Expected Return + Diversity</option>
							</select>
						</div>

						<div className="form-group">
							<button className="btn btn-info" onClick={this._onClickGetRecom.bind(this)}>Suggest</button>
						</div>

						<hr />

						<button onClick={this._onClickSave.bind(this)} className="btn btn-primary btn-lg">
							Create Portfolio
						</button>
					</div>

					<div className="col-sm-6">
						<p>Predicted fluctuation</p>
						<Plot ref='plot' />
					</div>

				</div>

				<PortfolioEditor ref='pmanager' onUpdate={this._onUpdateStocks.bind(this)} />
			</div>
		)
	}
}

