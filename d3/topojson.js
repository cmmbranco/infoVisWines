$('#color-map').vectorMap({
  backgroundColor: '#573E8A',
  regionStyle: {
    initial: {
        fill: '#cbced4'
    }
  },
  series: {
    regions: [{
      values: {
          IN:'#5478ab',
          DK:'#88b7d6',
          PL:'#5478ab',
          IQ:'#98c6e5',
          PK:'#88b7d6',
          RU:'#95c9ed',
          CN:'#b6d4e9',
          AU:'#5478ab',
          AR:'#b6d4e9',
          FR:'#9ccbeb',
          NG:'#98c6e5',
          CA:'#5478ab',
          US:'#9ccbeb'
      }
    }]
  }
});
