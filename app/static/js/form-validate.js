function validateFileOnSubmit() {
    var ext_a = getExtension('upload_bom_a');
    var ext_b = getExtension('upload_bom_b');
    
    if(ext_a.localeCompare('xlsx') == 0 && ext_b.localeCompare('xlsx') == 0) {
      return true;
    } else {
      alert('Please upload .xlsx document only!');
      event.preventDefault(); 
      return false;
    }
  }

function getExtension(id) {
  return document.getElementById(id).value.replace(/^.*[\\\/]/, '').split('.').pop();
}