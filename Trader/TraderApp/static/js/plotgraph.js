Plotly.d3.csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv', 
	function(err, rows){

		function unpack(rows, key) {
			return rows.map(function(row) { 
				return row[key]; 
			});
		}

		var trace = {
			x:['2018-03-17 00:50:00','2018-03-17 00:55:00'], 
			close: [43950.03,43991.96], 
			high: [43992.34,44022.23],  
			low: [41385.71,43949.58], 
			open:[ 41397.09,44016.17],
			// cutomise colors 
			increasing: {line: {color: 'black'}},
			decreasing: {line: {color: 'red'}},

			type: 'candlestick', 
			xaxis: 'x', 
			yaxis: 'y'
		};

		var data = [trace];

		var layout = {
			dragmode: 'zoom', 
			showlegend: false, 
			xaxis: {
				autorange: true, 
				title: 'Date',
				rangeselector: {
					x: 0,
					y: 1.2,
					xanchor: 'left',
					font: {size:8},
					buttons: [{
						step: 'month',
						stepmode: 'backward',
						count: 1,
						label: '1 month'
					}, {
							step: 'month',
							stepmode: 'backward',
							count: 6,
							label: '6 months'
					}, {
							step: 'all',
							label: 'All dates'
					}]
				}
			}, 
			yaxis: {
				autorange: true, 
			}
		};

		Plotly.plot('myDiv', data, layout); 
	}
);