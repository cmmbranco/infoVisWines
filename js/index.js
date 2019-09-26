//Elementos manipuladores basicos

//
// d3.select();
// d3.selectAll();
//
// d3.select('h1').style('color','red')
// .attr('class','heading')
// .text('Updated h1 tag');
//

// d3.select('body').append('p').text('First paragraph');
// d3.select('body').append('p').text('Second paragraph');
// d3.select('body').append('p').text('Third paragraph');

// d3.selectAll('p').style('color','blue');


// var dataset = [1,2,3,4,5];
//
// d3.select('body')
//     .selectAll('p')
//     .data(dataset)
//     .enter()
//     .append('p') // appends paragraph for each data element
//     .text('D3 is awesome');
//     //.text(function(d) {return d;});



/////// Fazer um barchart
//d3.select('.jumbotron').node().getBoundingClientRect().width

var dataset = [80,100,56,120,180,30,40,120,160];

var svgWidth = d3.select('.jumbotron').node().getBoundingClientRect().width*0.9;
var svgHeight = d3.select('.jumbotron').node().getBoundingClientRect().height*0.9;
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
