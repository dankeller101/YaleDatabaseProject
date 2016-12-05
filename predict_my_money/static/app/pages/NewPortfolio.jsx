// pages/NewPortfolio.jsx

import React from 'react'
import { findDOMNode } from 'react-dom'
import _ from 'lodash'
import { plotData, plotMultipleData } from '../lib/plot';

import CsrfToken from '../lib/csrf.jsx';

class PortfolioEditor extends React.Component {
	constructor(props) {
		super(props)
		// this.state = { stocks: [{ name: 'AAPL', amount: 3, price: 20 }] }
		this.state = { stocks: [] }
	}

	resetStocks(stocks) {
		if (stocks == undefined) {
			stocks = [];
		}
		this.setState({ stocks: stocks })
	}

	componentWillUpdate() {
		// this.props.onUpdateStocks(this.state.stocks)
	}

	getStocks() {
		console.log(this.state.stocks)
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
			this.props.onUpdateStocks(this.state.stocks)
			return
		}

		$.getJSON("/predictor/api/get_stock?name="+name, (data) => {
			if (data.error) {
				alert('Stock not found.')
				return;
			}

			var stocks = _.clone(this.state.stocks)

			stocks.push({
				name: name,
				amount: amount,
				price: data.data.current_adjusted_close
			})

			this.setState({ stocks: stocks }, () => {
				this.props.onUpdateStocks(this.state.stocks)
			})
		})
	}

	render() {
		var stockList = this.state.stocks.map((e, i) => {
			var remove = () => {
				var cloned = _.cloneDeep(this.state.stocks)
				var stocks = _.filter(cloned, (i) => i.name != e.name)
				this.setState({ stocks: stocks }, () => {
					this.props.onUpdateStocks(this.state.stocks)
				})
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
						<label htmlFor="exampleInputName2">Add to portfolio stock</label>
						<input type="text" ref="name" className="form-control" id="exampleInputName2" placeholder="stock name" />
					</div>

					<div className="form-group">
						<label htmlFor="exampleInputName2">with amount</label>
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
				var sum = _.sumBy(row, (el) => {
					return stocks[el.name].amount*el.price;
				})
				points.push({ close: sum, date: row[0].date });
			}

			plotData(points, findDOMNode(this.refs.plot), "Price ($)")
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
		console.log("stocks are", JSON.stringify(stocks))
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
			total_spend: parseInt(findDOMNode(this.refs.fbconst).value),
			timehorizon: findDOMNode(this.refs.f_timehorizon).value,
			maxinvest: findDOMNode(this.refs.f_maxinvest).value,
		}

		$.getJSON("/predictor/api/get_recommendation", data, (data) => {
			if (data.error) {
				alert(data.message)
				return
			}

			var stocks = [];
			_.each(data.data, (el) => {
				stocks.push({
					name: el[0].toUpperCase(),
					amount: el[1],
					price: el[2],
				})
			})

			this.setState({ stocks: stocks }, () => {
				this.refs.pmanager.resetStocks(this.state.stocks)
				this.refs.plot.updateStocks(this.state.stocks)
			})
		})
	}

	render() {
		return (
			<div className="container">
				<br />
				<h1>New Portfolio</h1>

				<div className="row">
					<div className="col-sm-6">
						<div className="form-group">
							<label htmlFor="inputName">Name</label>
							<input type="text" ref="fname" className="form-control" id="inputName" aria-describedby="nameHelp" placeholder="Identify your portfolio" />
							<small id="nameHelp" className="form-text text-muted">Identify your portfolio.</small>
						</div>

						<hr />

						<div className="form-group">
							<label htmlFor="exampleInputName2">Get Recommendation for</label>
							<input type="text" className="form-control" ref="fbconst" id="exampleInputName2" placeholder="how many dollars" />
						</div>

						<div className="form-group">
							<label htmlFor="exampleInputName2">of type</label>

							<select className="form-control" ref='ftype' id="exampleSelect1">
								<option value='random'>Random</option>
								<option value='high_return'>Highest Return</option>
								<option value='diverse'>Diverse Option</option>
							</select>
						</div>

						<div className="form-group">
							<label htmlFor="exampleInputName2">and time horizon</label>
							<input type="text" className="form-control" ref="f_timehorizon" id="" placeholder="Integer" />
						</div>

						<div className="form-group">
							<label htmlFor="exampleInputName2">with Max investment</label>
							<input type="text" className="form-control" ref="f_maxinvest" id="" placeholder="Float" />
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

				<PortfolioEditor ref='pmanager' onUpdateStocks={this._onUpdateStocks.bind(this)} />
			</div>
		)
	}
}

