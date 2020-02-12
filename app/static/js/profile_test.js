function profile_test() {
	var test_data = {
		profile_name 	: 'Test',
		customer 		: 'Test',
		item_type 		: $('#item-type').val(),
		prefix 			: $('#prefix').val(),
		prefix_action 	: $('#prefix-action').val(),
		suffix 			: $('#suffix').val(),
		suffix_action 	: $('#suffix-action').val(),
		delimiter 		: $('#delimiter').val(),
		delimiter_action: $('#delimiter-action').val(),
		delimiter_sample: $('#delimiter-sample').val(),
		test_input		: $('#profile-test-input').val()
	}
	var test_data = 'test_data=' + JSON.stringify(test_data);
	$.ajax({
		data: test_data,
		type: 'POST',
		url : '/profile/test'
	}).done(function(result) {
		$('#profile-result').val(result);
	});
}