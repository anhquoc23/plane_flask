function select_Chair(price_1, price_2)
{
     const VND = new Intl.NumberFormat('vi-VN', {
          style: 'currency',
          currency: 'VND',
     })
     var hangve = document.getElementById("hangve").value
     var ghe_hv1 = document.getElementById("ghe_1")
     var ghe_hv2 = document.getElementById("ghe_2")
     var price = document.getElementById("price")
     if (hangve == "1")
     {
          ghe_hv2.classList.remove('show')
          ghe_hv2.classList.add('none')
          ghe_hv1.classList.remove('none')
          ghe_hv1.classList.add('show')
          price.innerText = VND.format(price_1)
     }
     else if (hangve == "2")
     {
          ghe_hv1.classList.remove('show')
          ghe_hv1.classList.add('none')
          ghe_hv2.classList.remove('none')
          ghe_hv2.classList.add('show')
          price.innerText = VND.format(price_2)
     }
}

function datve_success()
{
    alert("Đặt vé thành công vui lòng tới sân bay truớc 1 tiếng để làm thủ tục")
}

function luulich_success(message)
{
    alert(message)
}