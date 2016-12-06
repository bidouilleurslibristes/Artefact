var update_data = function(){
    $.ajax({
      url: '/data',
      method: 'GET',
      success: function (data) {
          main.led_strips_colors = data.led_strips_colors;
          main.button_colors = data.button_colors;
      },
      error: function (error) {
          alert(JSON.stringify(error));
      }
  });
}



var main = new Vue({
  el: '#app',
  data: {
    led_strips_colors: [],
    button_colors: []
  },
  methods: {
    select: function(event) {
      targetId = event.currentTarget.id;
      console.log(targetId); // returns 'foo'
      $.post("/update_state", {'button': targetId} );
    }
  }
})


setInterval(update_data, 1000);