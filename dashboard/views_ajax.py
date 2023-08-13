from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from blog.models import Post, Image

import cloudinary.uploader

@require_POST
def update_is_Draft(request):
    post_id = request.POST.get('post_id')
    is_draft = request.POST.get('is_draft') == 'true'

    # Get the post with the specified post_id or return a 404 page if not found
    post = get_object_or_404(Post, pk=post_id)

    # Check if the current user is the author of the post
    if request.user != post.author:
        return JsonResponse({'status': 'error', 'message': 'Unauthorized'})

    try:
        post.is_draft = is_draft
        post.save()
        return JsonResponse({'status': 'success', 'is_draft': post.is_draft})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
@require_POST
def upload_image(request):
    images = request.FILES.getlist('upload')
    post_id = int(request.POST.get('post_id', 0))

    try:
        post = get_object_or_404(Post, pk=post_id)
    except:
        return JsonResponse({'message': f'post not found'}, status=404)

    if request.user != post.author:   # Check if the current user is the author of the post
        return JsonResponse({'message': 'Unauthorized'}, status=403)

    max_allowed_images = 15 # Only 15 photos are allowed for a post
    remaining_slots = max_allowed_images - post.images.count()
    if len(images) > remaining_slots:
        return JsonResponse({'message': f'Can only upload {remaining_slots} images each less than 2MB.'}, status=400)
    
    data = []
    for image in images:
        if image.size > 2 * 1024 * 1024: # Checking if all the images are less than 2MB
            return JsonResponse({'message': 'Each image should be less than 2MB in size.'}, status=400)

        folder_name = f'post_{post_id}'  
        
        try:
            result = cloudinary.uploader.upload(image, folder=folder_name)
        except Exception as e:
            return JsonResponse({'message': f'media server problem {e}'}, status=500)


        if 'public_id' in result:
            public_id = result['public_id']
            try:
                new_image = Image(post=post, public_id=public_id)
                new_image.save()
            except Exception as e:
                cloudinary.uploader.destroy(public_id)
                return JsonResponse({'message': f'server failed to upload image'}, status=500)

        uploaded_image_data = {
            'image_pk':new_image.pk,
            'post_pk':new_image.post.pk,
            'public_id': result['public_id'],
            'secure_url': result['secure_url'],
            'url': result['url']
        }
        data.append(uploaded_image_data)

    return JsonResponse({'message': 'Images uploaded and associated with the Post successfully.','uploaded_images_data':data})
    
@require_POST
def delete_image(request):
    image_id = request.POST.get('image_id')
    post_id = request.POST.get('post_id')

    try:
        image = get_object_or_404(Image, pk=image_id) #getting both objects
        post = get_object_or_404(Post, pk=post_id)  
    except:
        return JsonResponse({'message': f'post and image not found'}, status=404)

    if image.post != post: # Check if the image is related to the post
        return JsonResponse({'message': 'Image is not related to this post'}, status=404)

    # Check if the current user is the author of the post
    if request.user != post.author:
        return JsonResponse({'message': 'Unauthorized'}, status=403)
    
    try:
        # Delete the image from Cloudinary using the public_id
        response = cloudinary.uploader.destroy(image.public_id)

        if response.get('result') == 'ok':  # Check if the image was successfully deleted from Cloudinary
            image.delete()  # If the deletion is successful, also delete the Image model instance
            return JsonResponse({'message': f'Image deleted successfully.'}, status=200)
        else:
            return JsonResponse({'message': 'Image deletion failed.'}, status=500)
    except Exception as e:
        return JsonResponse({'message': 'Image deletion failed.'}, status=500)