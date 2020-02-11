$(document).ready(function () {
  // handle add button
  $('#add-profile').click(function (event){
    var error = true;
    $('.profile-list-top .scroll-container').children().each(function() {
      var checkbox = $(this).children().children();
      if(checkbox.prop('checked')) {
        var profile_id = checkbox.val();
        var parent = checkbox.parent().parent();
        var profile_class = parent.attr('class');
        var bottom_profile = $('.profile-list-bottom .scroll-container').find('.'+profile_class);
        var bom_index = $('#bom-index').val();
        var json_string = get_json_string(bom_index, profile_id, 'add');
        send(json_string, '/profile/processing');
        checkbox.prop('checked', false);
        parent.css('display','none');
        bottom_profile.css('display', 'block');
        error = false;
      }
    });
    if(error == true) {
      alert('Please choose a profile!');
    }
  });

  // handle remove button
});

function get_json_string(bom_index, profile_id, action) {
  var object = {
    bom_index: bom_index,
    profile_id: profile_id,
    action: action
  }
  return 'profile_data=' + JSON.stringify(object);
}

function send(data, url) {
  $.ajax({
    data: data,
    type: 'POST',
    url: url
  }).done(function(msg) {
    console.log(msg);
  });
}