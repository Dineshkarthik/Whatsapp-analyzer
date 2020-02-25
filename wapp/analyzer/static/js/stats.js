var divWidth = 500;
var divHeight = 200;

function readFile (masterData) {
  d3.json(masterData, function(error, data) {
    var spotLightObj = {};
    spotLightObj.activeDate = masterData.most_active_date;
    spotLightObj.activeDay = masterData.active_day_of_week;
    spotLightObj.activeHour = masterData.active_hour_of_day;
    spotLightObj.messageRate = masterData.avg_no_of_msgs_per_day;
    spotLightObj.mediaFreek = masterData.media_share_freak;
    spotLightObj.silentSpectator = masterData.the_silent_spectator;
    spotLightObj.theTalker = masterData.the_talker;

    tagCloud(masterData.word_cloud, 'tag-cloud');
    groupActivity(masterData.date_chart, 'group-activity');
    mediaShare(masterData.media_count, 'media-share');
    messageShare(masterData.message_count, 'message-share');
    spotLight(spotLightObj);
  });
}

function tagCloud(data, div_id) {

  var divWidth = 400;
  var divHeight = 250;
  
  var margin = {
        top: divHeight*0.05,
        right: divWidth*0.2,
        bottom: divHeight*0.3,
        left: divWidth*0.12
      },
  width = divWidth - margin.left - margin.right,
  height = divHeight - margin.top - margin.bottom;

  var color = d3.scale.category10();
  var dataset = d3.entries(data);

  var values = dataset.map(function (d) { return +d.value });
  var textScale = d3.scale.linear().range([15, 50]).domain(d3.extent(values));

  d3.layout.cloud()
      .size([width, height])
      .words(dataset)
      .padding(5)
      .rotate(0)
      .fontSize(function(d) { return textScale(+d.value); })
      .text(function (d) { return d.key})
      .padding(5)
      .on("end", plotWords)
      .start();

  function plotWords(words) {

    var svgContainer = d3.select('#' + div_id).append("svg")
        .attr("width", width)
        .attr("height", height)
        .call(responsivefy)
      .append("g")
        .attr("transform", "translate("+ width*0.5 +","+ height*0.5 +")")
        .attr('class', 'container-g')

    var cloudTags = svgContainer.selectAll("text")
        .data(words)
        .enter().append("text");

    cloudTags.style("font-size", function(d){ return d.size + "px"; })
        .style("fill", function(d, i) { return color(i); })
        .attr('class', 'pointer')
        .attr('data-color', function(d, i) { return color(i); })
        .attr("text-anchor", "middle")
        .transition()
        .duration(1000)
        .attr("transform", function(d) { return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")"; })
        .text(function(d) { return d.text; });
  }
}

function spotLight(data) {
  var dataset = d3.entries(data);

  dataset.forEach(function (d) {
    $('li.'+ d.key +' span.stat-value').text(d.value);
    // switch(d.key){
    //   case 'activeDate': 
    //   break;
    //   case 'activeDay':
    //   break;
    //   case 'activeHour':
    //   break;
    //   case 'avgMsgRate':
    //   break;
    //   case 'silentSpectator':
    //   break;
    //   case 'theTalker':
    //   break; 
    // }
  });

}
function groupActivity(data, div_id) {
  var margin = {
        top: divHeight*0.05,
        right: divWidth*0.2,
        bottom: divHeight*0.3,
        left: divWidth*0.12
      },
  width = divWidth - margin.left - margin.right,
  height = divHeight - margin.top - margin.bottom;

  var xScale = d3.time.scale()
      .range([0, width]);

  var yScale = d3.scale.linear()
      .range([height, 0]);

  var gridScale = d3.scale.linear()
      .range([height, 0]);

  var xAxis = d3.svg.axis()
      .scale(xScale)
      .orient("bottom")
      .tickFormat(d3.time.format("%b %Y"))
      .tickSize(0)
      .outerTickSize(5)

  var yAxis = d3.svg.axis()
      .scale(yScale)
      .orient("left")
      .tickSize(0)
      .outerTickSize(5)

  function y_grid() {        
    return d3.svg.axis()
      .scale(gridScale)
      .orient("left")
      .ticks(10)
  }

  var line = d3.svg.line()
      .x(function(d) { return xScale(d.key); })
      .y(function(d) { return yScale(d.value); });

  var parseDate = d3.time.format("%d/%m/%Y").parse;

  assignData(data, div_id);

  function assignData(data, div_id) {

    dataset = d3.entries(data);

    dataset.forEach(function(d) {
      d.key = parseDate(d.key);
      d.value = d.value;
    });

    dataset.sort(function(a,b){ return d3.ascending(a.key, b.key);});

    xScale.domain(d3.extent(dataset, function(d) { return d.key; }));
    var yMax = d3.max(dataset, function(d) { return d.value; })
    yScale.domain([0, yMax*1.2]);

    plotLine(dataset, div_id);
  }

  function plotLine (dataset, div_id) {

    d3.select('#' + div_id + ' svg').remove();

    var svgContainer = d3.select('#' + div_id).append("svg")
      .attr("width", divWidth)
      .attr("height", divHeight)
      .call(responsivefy);

    var chartContainer = svgContainer.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      .attr("class", 'container-g');

    chartContainer.append("g")
          .attr("class", "grid")
          .call(y_grid().tickSize(-width, 0, 0).tickFormat(""));

    var x_axis = chartContainer.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height*1.1 + ")")
        .call(xAxis);

    x_axis.selectAll("text")
        .transition()
        .duration(500)
        // .attr("y", height*0.1)
        .attr("transform", "rotate(-45) translate(-10," + height*0.1 + ")")

    var x_label = x_axis.append("text")
        .attr("class", "label")
        .style("text-anchor", "middle")
        .attr("x", width*0.5)
        .attr("y", height*0.3)
        .text("Timescope");

    var y_axis = chartContainer.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + (-width*0.04) + ",0)")
        .call(yAxis);

    y_axis.selectAll("text")
        .transition()
        .duration(500)
        .attr('x', -width*0.02);

    var y_label = y_axis.append("text")
        .attr("class", "label")
        .attr("transform", "rotate(-90)")
        .attr("x", -height*0.5)
        .attr("y", -width*0.1)
        .style("text-anchor", "middle")
        .text("Message Count");

    var linePlot = chartContainer.append("path")
        .datum(dataset)
        .attr("class", "line")
        .attr("d", line)
  }
}

function mediaShare(data, div_id) {

  var margin = {
        top: divHeight*0.05,
        right: divWidth*0.05,
        bottom: divHeight*0.05,
        left: divWidth*0.05
      },
  width = divWidth - margin.left - margin.right,
  height = divHeight - margin.top - margin.bottom;

  var radius = width*0.2;

  var color = d3.scale.category20();
  var color2 = d3.scale.category20();

  var arc = d3.svg.arc()
      .outerRadius(radius)
      .innerRadius(0);

  var arc2 = d3.svg.arc()
      .outerRadius(radius * 1.2)
      .innerRadius(radius * 1.2);

  var arcAnimate = d3.svg.arc()
      .outerRadius(radius * 1.05)
      .innerRadius(0);

  var tip = d3.tip()
      .attr('class', 'd3-tip')
      .offset([-10, 0])
      .style("font-size", "12px")
      .html(function(d) { return d.value; });

  var pie = d3.layout.pie()
      .sort(null)
      .value(function(d) { return +d.value; });

  var toPercent = d3.format("1%");
  var dataset = d3.entries(data);
  var total = d3.sum(dataset, function(d){return parseInt(d.value);});
  dataset.sort(function(a,b){ return d3.descending(a.value, b.value);});
  
  piePlot(dataset, div_id);

  function piePlot(dataset, div_id){

    d3.select('#' + div_id + ' svg').remove();

    var svgContainer = d3.select('#' + div_id).append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("class", 'container-g')
        .call(responsivefy);

    var chartContainer = svgContainer.append("g")
        .attr('class', 'chartContainer')
        .attr("transform", "translate(" + width/3 + "," + height/2 + ")")
        .call(tip);

    var draw = chartContainer.selectAll(".arc")
        .data(pie(dataset))
        .enter().append("g")
        .attr("class", "arc");

    draw.append("path")
        .attr("d", arc)
        .style("fill", function(d) { return color(d.data.key); })
        .on('mouseover', function(d) { tip.show(d); d3.select(this).transition().duration(100).attr("d", arcAnimate); })
        .on("mousemove", function () { return tip
          .style("top", (d3.event.pageY + 16) + "px")
          .style("left", (d3.event.pageX + 16) + "px");
        })
        .on('mouseout', function(d) { tip.hide(d); d3.select(this).transition().ease("elastic").duration(1000).attr("d", arc) });

    draw.append("text")
        .attr("class", "chart-text")
        .transition()
        .duration(500)
        .attr("transform", function(d) { return "translate(" + arc2.centroid(d) + ")"; })
        .text(function(d) { return toPercent(d.value / total) });

    var legend = svgContainer.append('g')
        .attr('class', 'legendContainer')
        .selectAll(".legend")
        .data(dataset);

    legend.enter()
        .append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(" + width*0.7 + "," + (i*20-height*0.2) + ")"; });

    legend.append("rect")
        .attr("x", 0)
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", function(d, i) { return color2(i); });

    legend.append("text")
        .attr("x", 20)
        .attr("y", 5)
        .attr("dy", ".35em")
        .text(function(d) { return d.key; });
  }
}

function messageShare (data, div_id) {
  var divWidth = 400;
  var margin = {
        top: divHeight*0.05,
        right: divWidth*0.05,
        bottom: divHeight*0.05,
        left: divWidth*0.05
      },
  width = divWidth - margin.left - margin.right,
  height = divHeight - margin.top - margin.bottom;

  var xScale = d3.scale.linear()
      .range([0, divWidth]);

  var yScale = d3.scale.ordinal()
      .rangeRoundBands([0, divHeight], 0.8);

  var yAxis = d3.svg.axis()
      .scale(yScale)
      .orient("right")
      .tickSize(0);

  var dataset = d3.entries(data);
  dataset.sort(function(a,b){ return d3.descending(a.value, b.value);});
  var xMax = d3.max(dataset, function(d) { return d.value; });
  xScale.domain([0, xMax+xMax*0.20]);
  yScale.domain(dataset.map(function(d) { return d.key; }));

  barPlot(dataset, div_id);

  function barPlot(dataset, div_id){

    var yRangebandHalf = yScale.rangeBand()/2;

    var svgContainer = d3.select('#' + div_id).append("svg")
        .attr("width", divWidth + margin.left + margin.right)
        .attr("height", divHeight + margin.top + margin.bottom)
        .append("g")
        .attr("class", 'container-g')
        .call(responsivefy);

    var chartContainer = svgContainer.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .attr("class", 'container-g');

    var yAxisLine = svgContainer.append("g")
        .attr("class", "bar-y-axis")
        .call(yAxis);

    var yAxisText = yAxisLine.selectAll("text")
        .attr("y", -(yScale.rangeBand()*2));

    var bar = svgContainer.selectAll(".bar")
        .data(dataset)
        .enter().append("g")
        .attr("class", "bar-plot")
        .attr("transform", function(d) { return "translate(0," + yScale(d.key) + ")"; });
                
    var backBar = bar.append("rect")
        .attr("class", "back-bar")
        .attr("width", width)
        .attr("height", yScale.rangeBand()+yRangebandHalf)
        .attr("rx", yRangebandHalf)
        .attr("ry", yRangebandHalf);

    var frontBar = bar.append("rect")
        .attr("class", "front-bar")
        .attr("width", function(d) { return xScale(d.value); })
        .attr("height", yScale.rangeBand())
        .attr("transform", function(d) { return "translate(" + divWidth*0.01 + "," + yRangebandHalf/2 + ")"; })
        .attr("rx", yRangebandHalf)
        .attr("ry", yRangebandHalf)

    var barText = bar.append("text")
        .attr("text-anchor", "end")
        .attr("x", width*1.1)
        .attr("y", yScale.rangeBand())
        .attr("alignment-baseline", "middle")
        .text(function(d) { return d.value});
  }

}
function responsivefy(svg) {
    // get container + svg aspect ratio
    var container = d3.select(svg.node().parentNode),
        width = parseInt(svg.style("width")),
        height = parseInt(svg.style("height")),
        aspect = width / height;

    svg.attr("viewBox", "0 0 " + width + " " + height)
        .attr("perserveAspectRatio", "xMinYMid")
        .call(resize);

    d3.select(window).on("resize." + container.attr("id"), resize);

    // get width of container and resize svg to fit it
    function resize() {
        var targetWidth = parseInt(container.style("width"));
        svg.attr("width", targetWidth);
        svg.attr("height", Math.round(targetWidth / aspect));
    }
}