from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Hotel, Room


@login_required(login_url="/accounts/login/")
def categories_list_view(request):
    context = {
        "active_icon": "products_categories",
        "categories": Hotel.objects.all()
    }
    return render(request, "products/categories.html", context=context)


@login_required(login_url="/accounts/login/")
def categories_add_view(request):
    context = {
        "active_icon": "products_categories",
        "category_status": Hotel.status.field.choices
    }

    if request.method == 'POST':
        # Save the POST arguments
        data = request.POST

        attributes = {
            "name": data['name'],
            "status": data['state'],
            "description": data['description']
        }

        # Check if a category with the same attributes exists
        if Hotel.objects.filter(**attributes).exists():
            messages.error(request, 'Category already exists!',
                           extra_tags="warning")
            return redirect('products:categories_add')

        try:
            # Create the category
            new_category = Hotel.objects.create(**attributes)

            # If it doesn't exist, save it
            new_category.save()

            messages.success(request, 'Category: ' +
                             attributes["name"] + ' created successfully!', extra_tags="success")
            return redirect('products:categories_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('products:categories_add')

    return render(request, "products/categories_add.html", context=context)


@login_required(login_url="/accounts/login/")
def categories_update_view(request, category_id):
    """
    Args:
        request:
        category_id : The category's ID that will be updated
    """

    # Get the category
    try:
        # Get the category to update
        category = Hotel.objects.get(id=category_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the category!', extra_tags="danger")
        print(e)
        return redirect('products:categories_list')

    context = {
        "active_icon": "products_categories",
        "category_status": Hotel.status.field.choices,
        "category": category
    }

    if request.method == 'POST':
        try:
            # Save the POST arguments
            data = request.POST

            attributes = {
                "name": data['name'],
                "status": data['state'],
                "description": data['description']
            }

            # Check if a category with the same attributes exists
            if Hotel.objects.filter(**attributes).exists():
                messages.error(request, 'Category already exists!',
                               extra_tags="warning")
                return redirect('products:categories_add')

            # Get the category to update
            category = Hotel.objects.filter(
                id=category_id).update(**attributes)

            category = Hotel.objects.get(id=category_id)

            messages.success(request, '¡Category: ' + category.name +
                             ' updated successfully!', extra_tags="success")
            return redirect('products:categories_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the elimination!', extra_tags="danger")
            print(e)
            return redirect('products:categories_list')

    return render(request, "products/categories_update.html", context=context)


@login_required(login_url="/accounts/login/")
def categories_delete_view(request, category_id):
    """
    Args:
        request:
        category_id : The category's ID that will be deleted
    """
    try:
        # Get the category to delete
        category = Hotel.objects.get(id=category_id)
        category.delete()
        messages.success(request, '¡Category: ' + category.name +
                         ' deleted!', extra_tags="success")
        return redirect('products:categories_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('products:categories_list')


@login_required(login_url="/accounts/login/")
def products_list_view(request):
    context = {
        "active_icon": "products",
        "products": Room.objects.all()
    }
    return render(request, "products/products.html", context=context)


@login_required(login_url="/accounts/login/")
def products_add_view(request):
    context = {
        "active_icon": "products_categories",
        "product_status": Room.status.field.choices,
        "categories": Hotel.objects.all().filter(status="ACTIVE")
    }

    if request.method == 'POST':
        # Save the POST arguments
        data = request.POST

        attributes = {
            "name": data['name'],
            "status": data['state'],
            "description": data['description'],
            "category": Hotel.objects.get(id=data['category']),
            "price": data['price']
        }

        # Check if a product with the same attributes exists
        if Room.objects.filter(**attributes).exists():
            messages.error(request, 'Product already exists!',
                           extra_tags="warning")
            return redirect('products:products_add')

        try:
            # Create the product
            new_product = Room.objects.create(**attributes)

            # If it doesn't exist, save it
            new_product.save()

            messages.success(request, 'Product: ' +
                             attributes["name"] + ' created successfully!', extra_tags="success")
            return redirect('products:products_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the creation!', extra_tags="danger")
            print(e)
            return redirect('products:products_add')

    return render(request, "products/products_add.html", context=context)


@login_required(login_url="/accounts/login/")
def products_update_view(request, product_id):
    """
    Args:
        request:
        product_id : The product's ID that will be updated
    """

    # Get the product
    try:
        # Get the product to update
        product = Room.objects.get(id=product_id)
    except Exception as e:
        messages.success(
            request, 'There was an error trying to get the product!', extra_tags="danger")
        print(e)
        return redirect('products:products_list')

    context = {
        "active_icon": "products",
        "product_status": Room.status.field.choices,
        "product": product,
        "categories": Hotel.objects.all()
    }

    if request.method == 'POST':
        try:
            # Save the POST arguments
            data = request.POST

            attributes = {
                "name": data['name'],
                "status": data['state'],
                "description": data['description'],
                "category": Hotel.objects.get(id=data['category']),
                "price": data['price']
            }

            # Check if a product with the same attributes exists
            if Room.objects.filter(**attributes).exists():
                messages.error(request, 'Product already exists!',
                               extra_tags="warning")
                return redirect('products:products_add')

            # Get the product to update
            product = Room.objects.filter(
                id=product_id).update(**attributes)

            product = Room.objects.get(id=product_id)

            messages.success(request, '¡Product: ' + product.name +
                             ' updated successfully!', extra_tags="success")
            return redirect('products:products_list')
        except Exception as e:
            messages.success(
                request, 'There was an error during the update!', extra_tags="danger")
            print(e)
            return redirect('products:products_list')

    return render(request, "products/products_update.html", context=context)


@login_required(login_url="/accounts/login/")
def products_delete_view(request, product_id):
    """
    Args:
        request:
        product_id : The product's ID that will be deleted
    """
    try:
        # Get the product to delete
        product = Room.objects.get(id=product_id)
        product.delete()
        messages.success(request, '¡Product: ' + product.name +
                         ' deleted!', extra_tags="success")
        return redirect('products:products_list')
    except Exception as e:
        messages.success(
            request, 'There was an error during the elimination!', extra_tags="danger")
        print(e)
        return redirect('products:products_list')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url="/accounts/login/")
def get_products_ajax_view(request):
    if request.method == 'POST':
        if is_ajax(request=request):
            data = []

            products = Room.objects.filter(
                name__icontains=request.POST['term'])
            for product in products[0:10]:
                item = product.to_json()
                data.append(item)

            return JsonResponse(data, safe=False)
