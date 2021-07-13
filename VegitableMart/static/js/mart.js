
var cartdata=document.getElementsByClassName('item-cart')

for(var i=0;i < cartdata.length;i++){
cartdata[i].addEventListener('click', function(){
var item=this.dataset.item
var act=this.dataset.act
console.log('item:',item,'act:',act)

console.log('USER:',user)
if(user == 'AnonymousUser'){
CartCookieItem(item, act)
}else{
CartUserItem(item,act)
}
})
}


function CartCookieItem(item, act){
	console.log('User not logged in ..')

	if (act == 'add'){
		if (cart[item] == undefined){
		cart[item] = {'quantity':1}

		}else{
			cart[item]['quantity'] += 1
		}
	}

	if (act == 'remove'){
		cart[item]['quantity'] -= 1

		if (cart[item]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[item];
		}
	}

	if (act == 'delete'){

		if (cart[item]['quantity'] >= 0){
			console.log('Item should be deleted')
			delete cart[item];
		}
	}

	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

	location.reload()
}



function CartUserItem(item,act){
console.log('User is logged in, sending data ..')
var url='/update_item/'
fetch(url, {
method:'POST',
headers:{
'content-type':'application/json',
'X-CSRFToken':csrftoken,
},
body:JSON.stringify({'item':item,'act':act})
})
.then((response) =>{
return response.json()
})
.then((data) =>{
console.log('data:',data)
location.reload()
});
}





