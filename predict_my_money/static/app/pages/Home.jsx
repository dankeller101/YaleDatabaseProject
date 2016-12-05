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

	render() {
		var _list = this.props.items.map((el, i) => {
			var access = () => {
				location.href = "/predictor/portfolios/"+el.id
			}
			return (
				<div className="PortfolioListItem">
					<h3>{ el.portfolio_name }</h3>&nbsp;
					<button className="btn btn-info" onClick={access}>See portfolio</button>
				</div>
			)
		})
		return (
			<div className="PortfoliosList">
				{_list}
			</div>
		)
	}
}


export default class NewPortfolioView extends React.Component {
	constructor(props) {
		super(props)
		this.state = { stocks: [] }
	}
	componentDidMount() {
	}

	render() {

		return (
			<div className="container">
				<br />
				<h1>Home</h1>

				<PortfoliosList items={window.portfolios}/>
			</div>
		)
	}
}

