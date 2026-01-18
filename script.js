function copyURL() 
{
    const copyText = document.getElementById("shortUrl");
    copyText.select();
    copyText.setSelectionRange(0, 99999);

    navigator.clipboard.writeText(copyText.value);

    document.getElementById("message").innerText = "Copied successfully!";
}