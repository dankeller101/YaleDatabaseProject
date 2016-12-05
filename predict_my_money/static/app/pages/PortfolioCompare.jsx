// pages/Portfolio.jsx

import React from 'react'
import { findDOMNode } from 'react-dom'
import _ from 'lodash'
import { plotData, plotMultipleData } from '../lib/plot'

import CsrfToken from '../lib/csrf.jsx'

export default class PortfolioCompareView extends React.Component {
  constructor(props) {
    super(props)
    this.state = {}
    // this.state.
  }

  componentDidMount() {
    $.getJSON("/predictor/api/get_portfolio_plot?id="+this.props.data1.id, (data) => {
      var points1 = []
      for (var i=0; i<data.data.length; ++i) {
        if (i%5 == 0) {
          points1.push(data.data[i])
        }
      }

			$.getJSON("/predictor/api/get_portfolio_plot?id="+this.props.data2.id, (data) => {
	      var points2 = []
	      for (var i=0; i<data.data.length; ++i) {
	        if (i%5 == 0) {
	          points2.push(data.data[i])
	        }
	      }

			  plotMultipleData(points1, points2, findDOMNode(this.refs.plot))
			})
    })
  }

  render() {

    var stockList1 = _.map(this.props.data1.stocks, (el, i) => {
		return (
			<tr>
				<td>{ i+1 }</td>
				<td>{ el.name }</td>
				<td>{ el.owned }</td>
				<td>${ el.price }</td>
				<td>${ el.price_then }</td>
			</tr>
		)
    })

    var stockList2 = _.map(this.props.data2.stocks, (el, i) => {
		return (
			<tr>
				<td>{ i+1 }</td>
				<td>{ el.name }</td>
				<td>{ el.owned }</td>
				<td>${ el.price }</td>
				<td>${ el.price_then }</td>
			</tr>
		)
    })

    return (
      <div className="StockView container">
        <br />
        <h1>Compare <abbr>portfolio '{this.props.data1.portfolio_name}'</abbr> and <abbr>portfolio '{this.props.data2.portfolio_name}'</abbr></h1>
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
              {stockList1}
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
              {stockList2}
              </tbody>
            </table>
          </div>
        </div>

        <div id="data-dump" ref="plot" data-prices="{{ data }}"></div>
      </div>
    )
  }
}

export class PortfolioView extends React.Component {
  constructor(props) {
    super(props)
    this.state = {}
  }

  componentDidMount() {
    $.getJSON("/predictor/api/get_portfolio_plot?id="+this.props.data.id, (data) => {
      plotData(data.data, findDOMNode(this.refs.plot))
    })
  }

  render() {

    var stockList = _.map(this.props.data.stocks, (el, i) => {
		return (
			<tr>
				<td>{ i+1 }</td>
				<td>{ el.name }</td>
				<td>{ el.owned }</td>
				<td>${ el.price }</td>
				<td>${ el.price_then }</td>
			</tr>
		)
    })

    return (
      <div className="StockView">
        <h1>Portfolio '{this.props.data.portfolio_name}'</h1>
        <h6>Created 3 days ago by Daniel Keller.</h6>

        <div className="row">
          <div className="col-sm-4">
            <hr />
            <pre>
            <code>
              Diversity: {this.props.data.current_diversity.toFixed(2)}
              <br />
              Current Value: {this.props.data.current_value.toFixed(2)}
              <br />
              Total Invested: {this.props.data.total_invested.toFixed(2)}
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
