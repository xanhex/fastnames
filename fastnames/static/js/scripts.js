function toClickbroard(el) {
    // Get the text field
    var copyText = document.getElementsByName(el);

     // Copy the text inside the text field
     navigator.clipboard.writeText(el.text);

    // Alert the copied text
    // alert("Copied the text: " + el.text);
  }
