from django.shortcuts import render,redirect
from django.http import HttpResponse  
from .models import Product ,Contact,Order ,OrderUpdate
from math import ceil  
import json

# Create your views here.  
def index(request):  
    allprod = [] 
    catsprod = Product.objects.values('category','id') 
    cats = {item['category'] for item in catsprod} 
    for cat in cats: 
        prod = Product.objects.filter(category=cat) 
        n = len(prod) 
        nSlides = n//4 + ceil((n/4)-(n//4)) 
        allprod.append([prod,range(1,nSlides),nSlides]) 

        params = {"allProd":allprod}

    return render(request,'shop/index.html',params)   

def about(request):   

    return render(request,'shop/about.html')

def contact(request):  
    if request.method == "POST": 
        name = request.POST.get('name', '') 
        email = request.POST.get('email', '') 
        phone = request.POST.get('phone', '') 
        desc = request.POST.get('desc', '')  
        contact = Contact(name=name,email=email,phone=phone,desc=desc) 
        contact.save() 
         
        Thanks = True
        return render(request,'shop/contact.html',{'Thanks':Thanks})
    return render(request,'shop/contact.html')

def tracker(request):   
    if request.method == "POST": 
        orderId = request.POST.get('orderId','') 
        email = request.POST.get('email','')  
        try: 
            order =  Order.objects.filter(order_id =orderId,email=email) 
            if len(order)>0:  
                update = OrderUpdate.objects.filter(order_id=orderId) 
                updates = [] 
                for item in update: 
                    updates.append({'text':item.update_desc,'time':item.timestamp}) 
                    response = json.dumps({"status":"success","updates":updates,"itemJson":order[0].items_json},default=str) 
                return HttpResponse(response)
            else: 
                 return HttpResponse('{"status":"noitem"}') 
        except Exception as e: 
                 return HttpResponse('{"status":"error"}')

    return render(request,'shop/tracker.html') 

def searchMatch(query,item):  
    ''' return true only if query matches the item''' 
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower(): 
      return True 
    else: 
        return False  
    

def search(request):   
    query = request.GET.get('search')
    allprod = [] 
    catsprod = Product.objects.values('category','id') 
    cats = {item['category'] for item in catsprod} 
    for cat in cats: 
        prodtemp = Product.objects.filter(category=cat) 
        prod = [item for item in prodtemp if searchMatch(query , item)] 
        n = len(prod) 
        nSlides = n//4 + ceil((n/4)-(n//4))  
        if len(prod)!=0:
            allprod.append([prod,range(1,nSlides),nSlides]) 

        params = {"allProd":allprod ,"msg": ""} 
        if len(allprod) == 0 or len(query)<4:  
            params = {'msg':"Please make sure to enter relevant search query."}


    return render(request,'shop/search.html',params)   

def productView(request,myid): 
    # fetch the product using id 
    product = Product.objects.filter(id=myid) 
    return render(request,'shop/products.html',{'product':product[0]}) 

def checkout(request):  
    if request.method == "POST": 
        items_Json = request.POST.get('itemJson','') 
        name = request.POST.get('name', '') 
        email = request.POST.get('email', '')  
        address=request.POST.get('address','') + " "+ request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','') 
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone', '') 
        order = Order(items_json=items_Json ,name=name, email=email,address=address, city=city, state=state,zip_code=zip_code,phone=phone) 
        order.save()  
        update = OrderUpdate(order_id = order.order_id, update_desc="The order has been placed.") 
        update.save()
        thank = True  
        id = order.order_id

        return render(request,'shop/checkout.html',{'thank' : thank, 'id':id})
    return render(request,'shop/checkout.html')

