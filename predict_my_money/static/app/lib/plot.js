
export function plotData(data, el) {
  // console.log('data', data)
  console.log('plotData')
  $(el).html('');

  var margin = {top: 20, right: 50, bottom: 30, left: 50},
    width = $(el).width() - margin.left - margin.right,
    height = $(el).width()/2 - margin.top - margin.bottom;

  var parseDate = d3.timeParse("%Y-%m-%d"), // %d-%b-%y"),
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


export function plotMultipleData(data1, data2, el) {

  var margin = {top: 20, right: 50, bottom: 30, left: 50},
    width = $(el).width() - margin.left - margin.right,
    height = $(el).width()/2 - margin.top - margin.bottom;

  var parseDate = d3.timeParse("%Y-%m-%d"), // %d-%b-%y"),
    bisectDate = d3.bisector(function(d) { return d.date; }).left,
    formatValue = d3.format(",.2f"),
    formatCurrency = function(d) { return formatValue(d); };

  var x = d3.scaleTime().range([0, width]);
  var y = d3.scaleLinear().range([height, 0]);

  var xAxis = d3.axisBottom().scale(x);
  var yAxis = d3.axisLeft().scale(y);

  var line1 = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.close); })
    .curve(d3.curveBasis);


  var line2 = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.close); })
    .curve(d3.curveBasis);


  var svg = d3.select(el).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  data1.forEach(function(d) {
      d.date = parseDate(d.date);
      d.close = +d.close;
    });

  data2.forEach(function(d) {
      d.date = parseDate(d.date);
      d.close = +d.close;
    });

  data1.sort(function(a, b) {
    return a.date - b.date;
  });

  data2.sort(function(a, b) {
    return a.date - b.date;
  });

  x.domain([data1[0].date, data1[data1.length - 1].date]);
  y.domain(d3.extent(data1.concat(data2), function(d) { return d.close; }));

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
    .text("TSR");

  var path2 = svg.append("path")
    .datum(data2)
    .attr("class", "line line2")
    .attr("d", line2);

  var path1 = svg.append("path")
    .datum(data1)
    .attr("class", "line")
    .attr("d", line1);

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
        i = bisectDate(data1, x0, 1),
        d0 = data1[i - 1],
        d1 = data1[i],
        d = x0 - d0.date > d1.date - x0 ? d1 : d0;
    focus.attr("transform", "translate(" + x(d.date) + "," + y(d.close) + ")");
    focus.select("text").text(formatCurrency(d.close));
  }
}