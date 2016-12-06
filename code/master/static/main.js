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

var audio = new Audio('/static/click.mp3');


var main = new Vue({
  el: '#app',
  data: {
    led_strips_colors: [],
    button_colors: []
  },
  methods: {
    button_pressed: function(event) {
      targetId = event.currentTarget.id;
      pressed = event.type=='mousedown';
      console.log(targetId, pressed); // returns 'foo'
      $.post(
        "/update_state",
        {'button': targetId, 'pressed': pressed},
        function(data){
          audio.play();
        }
      );
    }
  }
})


setInterval(update_data, 1000);