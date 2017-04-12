var main;

var update_data = function(){
    $.ajax({
      url: '/data',
      method: 'GET',
      success: function (data) {

        statuses = data;
        for(device in statuses){
          var dt = moment.duration(moment.now() - moment.unix(statuses[device].timestamp));
          statuses[device].timestamp = dt.asSeconds();
        }
        main.statuses = statuses;
      },
      error: function (error) {
          alert(JSON.stringify(error));
      }
  });
}

function init(){
  console.log("miam")
  main = new Vue({
    el: '#app',
    data: {
      statuses: {}
    },
  });
}

setTimeout(init, 0);
setTimeout(update_data, 0);
setInterval(update_data, 500);