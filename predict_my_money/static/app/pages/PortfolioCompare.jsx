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
    $.getJSON("/predictor/api/get_portfolio_tsr_plot?id="+this.props.data1.id, (data) => {
      var points1 = [], divpoints1 = []
      for (var i=0; i<data.data.length; ++i) {
        if (i%5 == 0) {
          points1.push(data.data[i])
          divpoints1.push({ close: data.data[i].diversity, date: data.data[i].date})
        }
      }

			$.getJSON("/predictor/api/get_portfolio_tsr_plot?id="+this.props.data2.id, (data) => {
	      var points2 = [], divpoints2 = []
	      for (var i=0; i<data.data.length; ++i) {
	        if (i%5 == 0) {
	          points2.push(data.data[i])
            divpoints2.push({ close: data.data[i].diversity, date: data.data[i].date})
	        }
	      }

			  plotMultipleData(points1, points2, findDOMNode(this.refs.plotTSR), "TSR")

        plotMultipleData(divpoints1, divpoints2, findDOMNode(this.refs.plotDiversity), "Diversity")
			})
    })

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

        plotMultipleData(points1, points2, findDOMNode(this.refs.plotPrice), "price")
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
        <h1>Compare <abbr>portfolio '{this.props.data1.portfolio_name}'</abbr> and <abbr>portfolio '{this.props.data2.portfolio_name}'</abbr></h1>
        <h1>{this.props.stock}</h1>

        <div className="row">
          <div id="data-dump" ref="plotTSR" data-prices="{{ data }}"></div>
        </div>

        <br />
        <div className="row">
          <div className="col-sm-6">
            <div id="data-dump" ref="plotPrice" data-prices="{{ data }}"></div>
          </div>
          <div className="col-sm-6">
            <div id="data-dump" ref="plotDiversity" data-prices="{{ data }}"></div>
          </div>
        </div>
        <br />

        <div className="row">
          <div className="col-sm-6">
            <h2 className='portfolio1'>{this.props.data1.portfolio_name}</h2>
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
          <h2 className='portfolio2'>{this.props.data2.portfolio_name}</h2>
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

      </div>
    )
  }
}
