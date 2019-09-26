
var dataset = [80,100,56,120,180,30,40,120,160];

var svgWidth = d3.select('.jumbotron').node().getBoundingClientRect().width*0.7;
var svgHeight = d3.select('.jumbotron').node().getBoundingClientRect().height*0.5;
var barPadding = 5;
var barWidth = (svgWidth/dataset.length);

var svg = d3.select('svg')
            .attr('width', svgWidth)
            .attr('height', svgHeight);

var barchart = svg.selectAll("rect")
                  .data(dataset)
                  .enter()
                  .append("rect")
                  .attr("y",function(d) {return svgHeight - d;})
                  .attr("height", function(d) {return d;})
                  .attr("width", barWidth - barPadding)
                  .attr("transform", function(d,i) {
                    var translate = [barWidth*i,0];
                    return "translate(" + translate + ")"
                  });
