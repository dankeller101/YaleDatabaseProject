// pages/Home.jsx

import React from 'react'
import { findDOMNode } from 'react-dom'
import _ from 'lodash'

import CsrfToken from '../lib/csrf.jsx';


class PortfoliosList extends React.Component {
	constructor(props) {
		super(props)
		this.state = { stocks: [] }
	}
	
	componentDidMount() {
	}

	_onClickCompare() {
		var opt1 = findDOMNode(this.refs.compare1).value;
		var opt2 = findDOMNode(this.refs.compare2).value;
		location.href = '/predictor/portfolios/compare/'+opt1+'/'+opt2;
	}

	render() {
		var _list = this.props.items.map((el, i) => {
			var access = () => {
				location.href = "/predictor/portfolios/"+el.id
			}
			return (
				<tr className="PortfolioListItem">
					<td>{ i+1 }</td>
					<td>{ el.portfolio_name }</td>
					<td>
					<button className="btn btn-info" onClick={access}>See portfolio</button>
					</td>
				</tr>
			)
		})

		var portOptions = this.props.items.map((el, i) => {
			return <option value={el.id}>{ el.portfolio_name }</option>
		})

		return (
			<div className="PortfoliosList">
				<table className="table table-striped">
					<thead>
						<th>#</th>
						<th>Name</th>
						<th>Control</th>
					</thead>
					<tbody>
					{_list}
					</tbody>
				</table>
				<br/>
				<h2>Compare portfolios</h2>
				<div className="form form-inline" onSubmit={this._onClickCompare.bind(this)}>
					<select className="form-control" ref="compare1">{portOptions}</select> with
					<select className="form-control" ref="compare2">{portOptions}</select>&nbsp;
					<button className="btn btn-info" onClick={this._onClickCompare.bind(this)}>Compare</button>
				</div>
			</div>
		)
	}
}


export default class HomeView extends React.Component {
	constructor(props) {
		super(props)
	}

	render() {

		return (
			<div className="container">
				<h1>Home</h1>
				<PortfoliosList items={window.portfolios}/>
			</div>
		)
	}
}

