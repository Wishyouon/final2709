$(document).ready(function() {
    $('#run-button').click(function() {
      $.ajax({
        type: 'GET',
        url: '/run-python',
        success: function(response) {
          $('#output').text(response);
        },
        error: function(response) {
          console.log('Error:', response);
        }
      });
    });
  });
  