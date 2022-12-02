<script type="text/javascript">


    function scrape(){
        let value = $("#msg_device_status").text();
    let splitted_value = value.split(",");
    let point1 = splitted_value[splitted_value.length - 2];
    let splitted_point1 = point1.split(" ");
    let location = `${splitted_point1[splitted_point1.length - 1]},${splitted_value[splitted_value.length - 1]}`;

    console.log(location);

    copyToClipboard(location);
    }

    function copyToClipboard(text) {
        var dummy = document.createElement("textarea");
    // to avoid breaking orgain page when copying more words
    // cant copy when adding below this code
    // dummy.style.display = 'none'
    document.body.appendChild(dummy);
    //Be careful if you use texarea. setAttribute('value', value), which works with "input" does not work with "textarea". – Eduard
    dummy.value = text;
    dummy.select();
    document.execCommand("copy");
    document.body.removeChild(dummy);
    }

    var intervalId = setInterval(function () {
        scrape();
    }, 10000);
</script>